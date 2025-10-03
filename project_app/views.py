from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from . models import *
from . forms import *
from notifications.models import *

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_create.html'
    success_url = reverse_lazy('accounts:dashboard')
    
    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            latest_notifications = Notification.objects.unread(self.request.user)
            context = super(ProjectCreateView, self).get_context_data(**kwargs)
            context['latest_notifications'] = latest_notifications[:3]
            context['notification_count'] = latest_notifications.count()
            return context
    
    def form_valid(self,form):
        project = form.save(commit=False)
        project.owner = self.request.user
        project.save()
        return redirect(self.success_url)
