from django.urls import path
from .views import ProjectCreateView
app_name = 'project_app'

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='create')
]