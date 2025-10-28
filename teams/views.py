from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import *
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.

class TeamCreateView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'create_team.html'
    success_url = reverse_lazy('teams:create')
    
    def get_context_data(self, **kwargs):
        context = super(TeamCreateView, self).get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        context['latest_notifications'] = latest_notifications[:3]
        context['notification_count'] = latest_notifications.count()
        context['header_text'] = 'Team Add'
        context['title'] = 'Team Add'
        context['button_text'] = 'Create Team'
        context['card_title'] = 'Create Teams'
        return context
    
    def form_valid(self,form):
        form.instance.created_by = self.request.user
        # if team lead not set
        if not form.cleaned_data['team_lead']:
            form.instance.team_lead = self.request.user
        messages.success(self.request,'Team created successfully...')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'There was an error creating team please try again later...')
        return super().form_invalid(form)
    
class TeamListView(ListView):
    model = Team
    template_name = 'team_list.html'
    context_object_name = 'teams'
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        context['latest_notifications'] = latest_notifications[:3]
        context['notification_count'] = latest_notifications.count()
        context['header_text'] = 'Team List'
        context['title'] = 'Team List'
        return context
    
    def get_queryset(self):
        # user created teams
        user = self.request.user
        if user.is_superuser:
            user_teams = Team.objects.all()
        else:
            user_created_teams = Team.objects.filter(created_by=user)
            user_belonged_teams = Team.objects.filter(members=user)            
            teams = user_created_teams | user_belonged_teams
            user_teams = teams.distinct()
        
        return user_teams
    
class TeamUpdateView(UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'create_team.html'
    
    # check the user permission to update team
    def get_object(self,queryset=None):
        team = get_object_or_404(Team, pk=self.kwargs['pk'])
        if team.created_by != self.request.user:
            raise Http404("Owner can only be update this team...")
        return team
    
    def get_context_data(self, **kwargs):
        context = super(TeamUpdateView, self).get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        context['latest_notifications'] = latest_notifications[:3]
        context['notification_count'] = latest_notifications.count()
        context['header_text'] = 'Team Update'
        context['title'] = 'Team Update'
        context['button_text'] = 'Update Team'
        context['card_title'] = 'Update Teams'
        return context
    
    def form_valid(self,form):
        messages.success(self.request,'Team updated successfully...')
        return super().form_valid(form)
    
    def form_invalid(self,form):
        messages.error(self.request,'Team does not updated...')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('teams:team_list')
    
class TeamDeleteView(DeleteView):
    model = Team
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('teams:team_list') 
    
    # check the user permission to delete team
    def get_object(self,queryset=None):
        team = get_object_or_404(Team, pk=self.kwargs['pk'])
        if team.created_by != self.request.user:
            raise Http404("Owner can only be delete this team...")
        return team 
    
    def get_context_data(self, **kwargs):
        context = super(TeamDeleteView, self).get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        context['latest_notifications'] = latest_notifications[:3]
        context['notification_count'] = latest_notifications.count()
        context['header_text'] = 'Delete Teams'
        context['title'] = 'Delete Teams'
        return context 
    
    # to delete
    def post(self,request,*args,**kwargs):
        team = self.get_object()
        
        messages.success(request,f'{team.name} was deleted successfully...')
        return super().post(request,*args,**kwargs)


    
    
