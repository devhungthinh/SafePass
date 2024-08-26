from django.contrib import admin


from .models import (
  Profile,
  UserSettings,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  pass


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
  list_display = ('user', 'theme', 'language', 'email_notications_enabled')
