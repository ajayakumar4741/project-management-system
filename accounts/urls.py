from . views import DashboardView
from django.urls import path

app_name = 'accounts'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard')
]