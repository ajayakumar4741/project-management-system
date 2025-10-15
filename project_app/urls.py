from django.urls import path
from .views import *
app_name = 'projects'

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='create'),
    path('near-due-date', ProjectNearDueDateListView.as_view(), name='due-list'),
    path('', ProjectListView.as_view(), name='list'),
    path('<int:pk>', ProjectDetailView.as_view(), name='project-detail'),
    path('<int:pk>/kanban-board', KanbanBoardView.as_view(), name='kanban-board')
]