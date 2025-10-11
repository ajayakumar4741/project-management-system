from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from . models import *
from . forms import *
from comment.forms import CommentForm
from comment.models import Comment
from django.core.paginator import Paginator
from notifications.tasks import create_notification
from django.contrib import messages

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_create.html'
    success_url = reverse_lazy('accounts:dashboard')
    
    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        context['latest_notifications'] = latest_notifications[:3]
        context['notification_count'] = latest_notifications.count()
        context['header_text'] = 'Project Add'
        context['title'] = 'Project Add'
        return context
    
    def form_valid(self,form):
        project = form.save(commit=False)
        project.owner = self.request.user
        project.save()
        actor_username = self.request.user.username
        verb = f'New project assigned, {project.name}'
        create_notification.delay(actor_username=actor_username, verb=verb,  object_id=project.id)
        return redirect(self.success_url)

class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/project_list.html'
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        context['latest_notifications'] = latest_notifications[:3]
        context['notification_count'] = latest_notifications.count()
        context['header_text'] = 'Projects'
        context['title'] = 'All Projects'
        return context
    

class ProjectNearDueDateListView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/project_list.html'
    paginate_by = 5
    
    def get_queryset(self):
        return Project.objects.all().due_in_two_days_or_less()
    
    def get_context_data(self, **kwargs):
        context = super(ProjectNearDueDateListView, self).get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        context['latest_notifications'] = latest_notifications[:3]
        context['notification_count'] = latest_notifications.count()
        context['header_text'] = 'Due Projects'
        context['title'] = 'Due Projects'
        return context
    
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    
    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        project = self.get_object()    
        # content_type = ContentType.objects.get_for_model(Project)
        comments = Comment.objects.filter_by_instance(project)  
        paginator = Paginator(comments,5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['latest_notifications'] = latest_notifications[:3]
        context['notification_count'] = latest_notifications.count()
        context['header_text'] = 'Project Details'
        context['title'] = 'Project Details'
        context['my_company'] = 'Projects Hub'
        context['page_obj'] = page_obj
        context['comments_count'] = comments.count()
        context['comment_form'] = CommentForm()
        context['my_company_desc'] = """
        Projects Hub is a results-driven project management firm specializing in delivering complex initiatives with precision, clarity, and measurable impact. 
        We partner with organizations across industries to plan, execute, and optimize projects — from concept to completion.

        """
        return context
    
    def post(self,request,*args,**kwargs):
        project = self.get_object()
        if request.user in project.team.members.all():
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.content_object = project
                comment.save()
                actor_username = self.request.user.username
                actor_full_name = self.request.user.profile.full_name
                verb = f'{actor_full_name} commented on {project.name}'
                create_notification.delay(actor_username=actor_username, verb=verb,  object_id=project.id)
                messages.success(request,'Comment Added Successfully...')
                return redirect('projects:project-detail',pk=project.pk)
            else:
                messages.warning(request, form.errors.get('comment',['An error occured...'])[0])
        else:
            messages.warning(request, 'You are not a member...')
        return self.get(request,*args,**kwargs)