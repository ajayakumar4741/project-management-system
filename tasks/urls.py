from django.urls import path
from .views import *

app_name = 'tasks'

urlpatterns = [
    path('update_task_status_ajax/<int:task_id>/', update_task_status_ajax, name='update_task_status_ajax'),
    path('create_task_ajax/', create_task_ajax, name='create_task_ajax'),
    path('<int:task_id>/get_task/', get_task, name='get_task'),
]