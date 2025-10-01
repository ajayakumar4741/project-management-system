from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from teams.models import Team
# Create your models here.

class ProjectQueryset(models.QuerySet):
    def active(self):
        return self.filter(active=True)
    
    def upcomming(self):
        return self.filter(due_date__gte=timezone.now())
    
class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQueryset(self.model, using=self._db)
    
    def all(self):
        return self.get_queryset().active().upcomming()

class Project(models.Model):
    owner = models.ForeignKey(User, models.CASCADE, related_name='projects')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=20)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('To Do','To Do'),('In Progress','In Progress'),('Completed','Completed')], default='To Do')
    priority = models.CharField(max_length=20, choices=[('Low','Low'),('Medium','Medium'),('High','High')], default='Medium')
    start_date = models.DateField()
    due_date = models.DateField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = ProjectManager()
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']
        
    def daya_until_due(self):
        if self.due_date:
            current_date = timezone.now().date()
            return (self.due_date - current_date).days
        return None
    
    @property
    def progress(self):
        progress_dict = {
            'To Do':0,
            'In Progress':50,
            'Completed':100
        }
        return progress_dict.get(self.status, 0)
    
    @property
    def status_color(self):
        status_value = self.progress
        if status_value == 100:
            color = 'success'
        elif status_value == 50:
            color = 'primary'
        else:
            color = ''
        return color
    
    @property
    def priority_color(self):
        if self.priority == 'Low':
            color = 'success'
        elif self.priority == 'Medium':
            color = 'warning'
        else:
            color = 'danger'
        return color