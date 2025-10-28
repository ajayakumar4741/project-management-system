from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from . models import *
from . forms import *
from comment.forms import CommentForm
from comment.models import Comment
from django.core.paginator import Paginator
from notifications.tasks import create_notification
from django.contrib import messages
from tasks.forms import *

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
        create_notification.delay(actor_username=actor_username, verb=verb,  object_id=project.id, content_type_model='project', content_type_app_label='project_app')
        return redirect(self.success_url)
    
class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'projects/project_update.html'
    form_class = ProjectForm
    
    
    # check the user permission to update project
    def get_object(self,queryset=None):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        if project.owner != self.request.user:
            raise Http404("Owner can only be update this project...")
        return project
    
    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        context['latest_notifications'] = latest_notifications[:3]
        context['notification_count'] = latest_notifications.count()
        context['header_text'] = 'Project Update'
        context['title'] = 'Project Update'
        return context
    
    def form_valid(self,form):
        messages.success(self.request,'Project updated successfully...')
        return super().form_valid(form)
    
    def form_invalid(self,form):
        messages.error(self.request,'Project does not updated...')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('projects:project-detail', kwargs={'pk':self.object.pk})

class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/project_list.html'
    paginate_by = 5
    
    def get_queryset(self):
        return Project.objects.for_user(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        context['latest_notifications'] = latest_notifications[:3]
        context['notification_count'] = latest_notifications.count()
        context['header_text'] = 'Projects'
        context['title'] = 'All Projects'
        return context

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'projects/confirm_delete.html' 
    success_url = reverse_lazy('projects:list')  
    
    def get_context_data(self, **kwargs):
        context = super(ProjectDeleteView, self).get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        context['latest_notifications'] = latest_notifications[:3]
        context['notification_count'] = latest_notifications.count()
        context['header_text'] = 'Delete Projects'
        context['title'] = 'Delete Projects'
        return context 
    
    # check the user has delete permission
    def post(self,request,*args,**kwargs):
        project = self.get_object()
        if request.user != project.owner:
            messages.warning(request,'Only owner can delete this project...')
            return redirect('projects:project-detail',pk=project.pk)
        messages.success(request,f'{project.name} was deleted successfully...')
        return super().post(request,*args,**kwargs)

class ProjectNearDueDateListView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/project_list.html'
    paginate_by = 5
    
    def get_queryset(self):
        return Project.objects.for_user(self.request.user).due_in_two_days_or_less()
    
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
        context['attachment_form'] = AttachmentForm()
        context['my_company_desc'] = """
        Projects Hub is a results-driven project management firm specializing in delivering complex initiatives with precision, clarity, and measurable impact. 
        We partner with organizations across industries to plan, execute, and optimize projects — from concept to completion.

        """
        return context
    
    def post(self,request,*args,**kwargs):
        project = self.get_object()
        if request.user not in project.team.members.all():
            messages.warning(request, 'You are not a member...')
            return self.get(request,*args,**kwargs)
        
        if 'comment_submit' in request.POST:
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
        if 'attachment_submit' in request.POST:
            attachment_form = AttachmentForm(request.POST,request.FILES)
            if attachment_form.is_valid():
                attachment=attachment_form.save(commit=False)
                attachment.project = project
                attachment.user = request.user
                attachment.save()
                messages.success(request,'File Uploaded Successfully...')
                return redirect('projects:project-detail',pk=project.pk)
            else:
                messages.error(request,'An error occured, please try again later...')
        return self.get(request,*args,**kwargs)
    
class KanbanBoardView(DetailView):
    model = Project
    template_name = 'projects/kanban-board.html'
    context_object_name = 'project'
    
    def get_context_data(self, **kwargs):
        context = super(KanbanBoardView, self).get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        project = self.get_object()    
        
        context['latest_notifications'] = latest_notifications[:3]
        context['notification_count'] = latest_notifications.count()
        context['header_text'] = 'Kanban Board'
        context['title'] = f"{project.name}'s Kanban Board"
        context['is_kanban'] = True
        # sepreate tasks based on status
        context['backlog_tasks'] = project.tasks.filter(status='Backlog').upcomming()
        context['todo_tasks'] = project.tasks.filter(status='To Do').upcomming()
        context['inprogress_tasks'] = project.tasks.filter(status='In Progress').upcomming()
        context['completed_tasks'] = project.tasks.filter(status='Completed').upcomming()
        context['form'] = TaskUpdateForm()
        # context['task_form'] = TaskAssignForm()
        return context