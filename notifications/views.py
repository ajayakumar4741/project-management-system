from django.shortcuts import render
from django.views.generic import ListView
from .models import *
# Create your views here.
   
class NotificationListView(ListView):
    model = Notification
    context_object_name = 'notifications'
    template_name = 'notification_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        return self.request.user.notifications.unread()
    
    def get_context_data(self, **kwargs):
        context = super(NotificationListView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread()            
        context['latest_notifications'] = latest_notifications[:3]
        context['notification_count'] = latest_notifications.count()
        context['header_text'] = 'Notifications'
        context['title'] = 'All Notifications'
        return context