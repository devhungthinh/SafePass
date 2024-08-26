from django.db.models.signals import post_save
from django.dispatch import receiver


from accounts.models import CustomUser
from .models import (
  Profile,
  UserSettings,
)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
  instance.profile.save()
