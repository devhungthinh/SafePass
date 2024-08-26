from django.urls import path


from .views import (
  ProfileDetailView,
  ProfileUpdateView,
  UserSettingsDetailView,
)


app_name = 'users'

urlpatterns = [
  path('<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
  path('update/<int:pk>', ProfileUpdateView.as_view(), name='profile_update'),
  path('settings/', UserSettingsDetailView.as_view(), name='settings_detail'),
]
