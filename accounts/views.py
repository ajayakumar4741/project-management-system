from django.shortcuts import render, redirect
from django.views.generic import View, ListView
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
        latest_projects = Project.objects.for_user(request.user)
        latest_tasks = Task.objects.all()
        latest_members = Profile.objects.all()
        
        context = {}
        # if request.user.is_authenticated:
        latest_notifications = request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:3]
        context['notification_count'] = latest_notifications.count()
        context['latest_projects'] = latest_projects[:5]
        context['latest_project_count'] = latest_projects.count()
        context['projects_near_due_date'] = latest_projects.due_in_two_days_or_less()[:5]
        context["latest_task_count"] = latest_tasks.count()
        context['latest_members'] = latest_members[:8]
        context['latest_member_count'] = latest_members.count()
        context['team_count'] = Team.objects.count()
        context['header_text'] = 'Dashboard'
        context['title'] = 'Dashboard'
        return render(request, 'dashboard.html',context)
    
class MembersListView(ListView):
    model = Profile
    context_object_name = 'members'
    template_name = 'profile_list.html'
    paginate_by = 8
    
    def get_queryset(self):
        return Profile.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(MembersListView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        context['latest_notifications'] = latest_notifications[:3]
        context['notification_count'] = latest_notifications.count()
        context['header_text'] = 'Members'
        context['title'] = 'All Members'
        return context