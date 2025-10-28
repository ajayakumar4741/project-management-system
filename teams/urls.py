from django.urls import path
from .views import *

app_name = 'teams'

urlpatterns = [
    path('create/',TeamCreateView.as_view(),name='team_create'),
    path('<int:pk>/update/',TeamUpdateView.as_view(),name='team_update'),
    path('<int:pk>/delete/',TeamDeleteView.as_view(),name='team_delete'),
    path('',TeamListView.as_view(),name='team_list')
]