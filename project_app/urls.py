from django.urls import path
from .views import *
app_name = 'projects'

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='create'),
    path('near-due-date', ProjectNearDueDateListView.as_view(), name='due-list'),
    path('', ProjectListView.as_view(), name='list'),
    path('<int:pk>', ProjectDetailView.as_view(), name='project-detail'),
    path('<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('<int:pk>/kanban-board', KanbanBoardView.as_view(), name='kanban-board')
]