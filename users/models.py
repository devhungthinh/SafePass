from django.db import models
from django.urls import reverse_lazy


from accounts.models import CustomUser


class Profile(models.Model):
  user = models.OneToOneField(CustomUser, related_name='profile', on_delete=models.CASCADE)
  bio = models.TextField(max_length=500, blank=True)
  avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

  def __str__(self):
    return f'{self.user.username} Profile'


class UserSettings(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='settings')
  theme = models.CharField(max_length=20, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')
  language = models.CharField(max_length=20, choices=[('en', 'English'), ('vi', 'Vietnamese')], default='en')
  email_notications_enabled = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.user.username}'s Settings"
  
  # def get_absolute_url(self):
  #   return reverse_lazy()
