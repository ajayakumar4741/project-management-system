from . views import DashboardView, MembersListView, RegisterView
from django.urls import path

app_name = 'accounts'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('members', MembersListView.as_view(), name='members-list'),
    path('register/',RegisterView,name='register')
]