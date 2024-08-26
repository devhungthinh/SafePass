from django import forms
from django.forms.models import inlineformset_factory


from .models import Profile
from accounts.models import CustomUser


class CustomUserUpdateForm(forms.ModelForm):

  class Meta:
    model = CustomUser
    fields = ('email', 'username',)


class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['bio', 'avatar']
    widgets = {
      'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
    }

ProfileFormset = inlineformset_factory(
  CustomUser,
  Profile,
  form=ProfileForm,
  can_delete=False,
  extra=0,
)
