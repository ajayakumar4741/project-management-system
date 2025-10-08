from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timesince import timesince
from django.utils import timezone
from datetime import timedelta
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='', blank=True, null=True)
    job_title = models.CharField(max_length=100,null=True)
    phone = PhoneNumberField(null=True,blank=True,unique=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    @property
    def full_name(self):
        name = self.user.get_full_name()
        if name:
            return name
        return self.user.get_username()
    
    @property
    def date_joined(self):
        time_diff = timezone.now() - self.user.date_joined
        if time_diff <= timedelta(days=2):
            return timesince(self.user.date_joined) + ' ago'
        else:
            return self.user.date_joined.strftime('%d %b')
    
    @property
    def profile_picture_url(self):
        try:
            image = self.profile_picture.url
        except:
            image = 'https://cdn.pixabay.com/photo/2020/06/30/10/23/icon-5355896_1280.png'
        return image
    


@receiver(post_save, sender=User)
def create_user_profile(sender, instance,  **kwargs):
    # if user exists but no profile then create it
        Profile.objects.get_or_create(user=instance)
        
