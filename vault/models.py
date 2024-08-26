from django.urls import reverse, reverse_lazy
from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
from django.contrib import messages


from urllib.parse import urlparse


class Vault(models.Model):
  PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('critical', 'Critical'),
  ]

  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=255, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  priority = models.CharField(
    max_length=15,
    choices=PRIORITY_CHOICES,
    null=True, 
    blank=True,
    default='low',
  )

  def __str__(self):
    return f"{self.name}"
  
  def get_absolute_url(self):
    return reverse_lazy('vault:vault_detail', kwargs={'pk': self.pk})

  def get_password_entry_count(self):
    return self.password_entries.count()


class PasswordEntry(models.Model):
  PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('critical', 'Critical'),
  ]

  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
  vault = models.ForeignKey(Vault, related_name='password_entries', on_delete=models.SET_NULL, blank=True, null=True)
  title = models.CharField(max_length=100, unique=True)
  username = models.CharField(max_length=100, blank=True, null=True)
  email = models.CharField(max_length=100)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)
  is_trashed = models.BooleanField(default=False)
  last_used = models.DateTimeField(auto_now=True)
  priority = models.CharField(
    max_length=15,
    choices=PRIORITY_CHOICES,
    null=True, 
    blank=True,
    default='low',
  )

  def save(self, *args, **kwargs):
    if not self.username:
      self.username = self.email

    if not self.email:
      self.email = self.username

    super().save(*args, **kwargs)

  def __str__(self):
    return f"{self.title}"

  def get_absolute_url(self):
    return reverse("vault:password_detail", kwargs={"pk": self.pk})
  

class PasswordHistory(models.Model):
  password_entry = models.ForeignKey(PasswordEntry, related_name='history', on_delete=models.CASCADE)
  password = models.CharField(max_length=128)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)
  is_current = models.BooleanField(default=False)

  def save(self, *args, **kwargs):
    return super(PasswordHistory, self).save(*args, **kwargs)

  def __str__(self):
    return f'{self.password_entry.title} {self.password}'

  def get_absolute_url(self):
    return reverse_lazy('vault:password_history_list', kwargs={"pk": self.password_entry.pk})
  

class WebsiteManager(models.Manager):
  def create(self, url, **kwargs):
    hostname = urlparse(url).netloc
    kwargs['name'] = hostname
    return super().create(**kwargs)
  

class Website(models.Model):
  name = models.CharField(max_length=255, blank=True)
  password_entry = models.ForeignKey(
    PasswordEntry, 
    related_name='websites', 
    on_delete=models.CASCADE,
  )
  url = models.URLField(blank=False, null=False, unique=True)

  objects = WebsiteManager

  def __str__(self):
    return self.name
