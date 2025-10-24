from . views import DashboardView, MembersListView, RegisterView, ProfileDetailView
from django.urls import path

app_name = 'accounts'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('<int:pk>/user/', ProfileDetailView.as_view(), name='user-profile'),
    path('members', MembersListView.as_view(), name='members-list'),
    path('register/',RegisterView,name='register')
]