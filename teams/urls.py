from django.urls import path
from .views import *

app_name = 'teams'

urlpatterns = [
    path('create/',TeamCreateView.as_view(),name='create'),
    path('',TeamListView.as_view(),name='team_list')
]