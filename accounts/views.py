from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from django.core.paginator import Paginator
from django.contrib.contenttypes.models  import ContentType
from comment.models import Comment
from project_app.models import Project
from tasks.models import Task
from .forms import *
from . models import Profile
from teams.models import Team
from django.contrib import messages
from django.contrib.auth.decorators import login_not_required

@login_not_required
def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registered Successfully...')
            return redirect('login')
        else:
            messages.error(request,'Please correct the errors...')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html',{'form':form})

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        user = request.user    
        
        if user.is_superuser:
            latest_projects = Project.objects.all()
            latest_tasks = Task.objects.all()
            latest_members = Profile.objects.all()
            team_count=Team.objects.all().count()
        else:
            latest_projects = Project.objects.for_user(user)
            latest_tasks = Task.objects.for_user(user)
            latest_members = Profile.objects.filter(
                user__teams__in=user.teams.all()
            ).distinct()
            team_count = user.teams.all().count()
        
        context = {}        
        latest_notifications = user.notifications.unread(user)
        context['latest_notifications'] = latest_notifications[:3]
        context['notification_count'] = latest_notifications.count()
        context['latest_projects'] = latest_projects[:5]
        context['latest_project_count'] = latest_projects.count()
        context['projects_near_due_date'] = latest_projects.due_in_two_days_or_less()[:5]
        context["latest_task_count"] = latest_tasks.count()
        context['latest_members'] = latest_members[:8]
        context['latest_member_count'] = latest_members.count()
        context['team_count'] = team_count
        context['header_text'] = 'Dashboard'
        context['title'] = 'Dashboard'
        return render(request, 'dashboard.html',context)
    
class MembersListView(ListView):
    model = Profile
    context_object_name = 'members'
    template_name = 'profile_list.html'
    paginate_by = 8
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            latest_members = Profile.objects.all()
            return latest_members
        else:
            latest_members = Profile.objects.filter(
                user__teams__in=user.teams.all()
            ).distinct()
            return latest_members
    
    def get_context_data(self, **kwargs):
        context = super(MembersListView, self).get_context_data(**kwargs)
        
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        context['latest_notifications'] = latest_notifications[:3]
        context['notification_count'] = latest_notifications.count()
        context['header_text'] = 'Members'
        context['title'] = 'All Members'
        return context
    
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'user_profile.html'
    context_object_name = 'profile'
    
    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        profile = self.get_object()
        user_projects = Project.objects.for_user(profile.user)
        latest_notifications = self.request.user.notifications.unread(self.request.user)           
        context['latest_notifications'] = latest_notifications[:3]
        context['notification_count'] = latest_notifications.count()
        context['header_text'] = 'Profile'
        context['title'] = f"{profile.full_name}'s Profile"
        # pagination for user projects
        paginator = Paginator(user_projects,5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # setting up users comment
        user_comments = profile.user.comments.all()
        project_content_type = ContentType.objects.get_for_model(Project)
        project_comments = Comment.objects.filter(
            content_type = project_content_type,
            object_id__in = [str(id) for id in user_projects.values_list('id',flat=True)]
        )
        # combining comments
        all_user_comments = (user_comments | project_comments).distinct()
        # pagination for user comments
        comment_paginator = Paginator(all_user_comments,5)
        comment_page_number = self.request.GET.get('comment_page')
        comments = comment_paginator.get_page(comment_page_number)
        # user tasks
        user_tasks = Task.objects.for_user(profile.user)
        # pagination for user tasks
        task_paginator = Paginator(user_tasks,1)
        task_page_number = self.request.GET.get('task_page')
        tasks = task_paginator.get_page(task_page_number)
        
        context['comments'] = comments
        context['all_user_comments_count'] = all_user_comments.count()
        # user tasks and project count
        context['user_tasks_count'] = user_tasks.count()
        context['tasks'] = tasks
        context['user_projects_count'] = user_projects.count()
        context['page_obj'] = page_obj
        return context