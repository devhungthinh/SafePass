from django.db.models.signals import post_save
from django.dispatch import receiver


from users.models import (
  Profile,
  UserSettings,
)


from .models import (
  CustomUser,
)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)
    UserSettings.objects.create(user=instance)
