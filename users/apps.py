from django.apps import AppConfig
from django.db.models.signals import post_save


class UsersConfig(AppConfig):
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'users'

  def ready(self):
    from accounts.models import CustomUser
    from .signals import save_user_profile

    post_save.connect(save_user_profile, sender=CustomUser)
