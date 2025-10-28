from . views import *
from django.urls import path

app_name = 'accounts'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('<int:pk>/user/', ProfileDetailView.as_view(), name='user-profile'),
    path('members', MembersListView.as_view(), name='members-list'),
    path('password-change', PasswordChangeView.as_view(), name='change_password'),
    path('<int:pk>/profile_update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('<int:pk>/profile_delete/', ProfileDeleteView.as_view(), name='profile_delete'),
    path('register/',RegisterView,name='register')
]