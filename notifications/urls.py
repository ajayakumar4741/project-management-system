from . views import NotificationListView
from django.urls import path

app_name = 'notifications'
urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    
]