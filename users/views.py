from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


from accounts.models import CustomUser
from accounts.forms import CustomUserChangeForm
from .models import (
  Profile,
  UserSettings,
)
from .forms import (
  ProfileForm,
  ProfileFormset,
)

class ProfileDetailView(LoginRequiredMixin, DetailView):
  model = Profile
  template_name = 'users/profile_detail.html'
  context_object_name = 'profile'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return context
  

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
  model = CustomUser
  # form_class = CustomUserChangeForm
  fields = ['email']
  template_name = 'users/profile_update.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    if self.request.method == 'POST':
      context['profile_formset'] = ProfileFormset(self.request.POST, instance=self.object)
    else:
      context['profile_formset'] = ProfileFormset(instance=self.object)
    return context
  
  def form_valid(self, form):
    context = self.get_context_data()
    profile_formset = context['profile_formset']
    if profile_formset.is_valid():
      self.object = form.save()
      profile_formset.save()
      return super().form_valid(form)
    else:
      return self.form_invalid(form, profile_formset)

  def get_success_url(self):
    return reverse_lazy('users:profile_detail', kwargs={'pk': self.object.profile.pk })
  

class UserSettingsDetailView(LoginRequiredMixin, DetailView):
  model = UserSettings
  template_name = 'users/settings_detail.html'
  context_object_name = 'settings'

  def get_object(self):
    return self.model.objects.get(user=self.request.user)
