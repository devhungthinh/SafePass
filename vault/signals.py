from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver


from config.logging_config import logger
from .models import (
  Vault, 
  PasswordEntry,
  PasswordHistory,
)


@receiver(pre_delete, sender=Vault)
def handle_password_entry_to_none(sender, instance, **kwargs):
  PasswordEntry.objects.filter(vault=instance).update(vault=None)
  

@receiver(post_save, sender=PasswordEntry)
def handle_password_entry_created(sender, instance, created, **kwargs):
  if created:
    logger.info('inside signal')
    PasswordHistory.objects.create(
      password_entry=instance,
      password=instance.password,
      is_current=True,
    )
