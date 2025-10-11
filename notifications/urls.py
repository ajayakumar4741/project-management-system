from . views import *
from django.urls import path

app_name = 'notifications'
urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:notification_id>/read/', MarkNotificationAsRead.as_view(),name='mark_as_read')
]