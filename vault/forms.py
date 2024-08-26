from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.password_validation import validate_password
from crispy_forms.helper import FormHelper
from django.shortcuts import render
from django.template.loader import render_to_string
from crispy_forms.layout import (
  LayoutObject,
  TEMPLATE_PACK,
  Layout, 
  Submit, 
  Row, 
  Column, 
  Field, 
  Fieldset, 
  Div, 
  HTML,
  Hidden
)


import re


from config.logging_config import logger
from .models import (
  Vault,
  PasswordEntry,
  PasswordHistory,
  Website,
)
from .custom_layout_object import Formset


class VaultForm(forms.ModelForm):
  class Meta:
    model = Vault
    fields = ['name', 'priority', 'description']

  def clean_name(self):
    name = self.cleaned_data.get('name')
    if Vault.objects.filter(name=name).exists():
      raise forms.ValidationError('This vault name already exists.')
    return name
  
  def clean_description(self):
    description = self.cleaned_data.get('description')
    name = self.cleaned_data.get('name')
    if type(description) == str and len(description) == 0:
      description = f'Draft description for {name} vault. You can change later.'
    return description
  
  def clean_priority(self):
    priority = self.cleaned_data.get('priority')
    if priority is None:
      return self.Meta.model.PRIORITY_CHOICES[0][0]
    return priority


class VaultCreateForm(VaultForm):
  class Meta:
    model = Vault
    fields = ['name', 'priority', 'description']

  name = forms.CharField(
    widget=forms.TextInput(attrs={
      'placeholder': 'Name of the vault'
    })
  )

  description = forms.CharField(
    widget=forms.Textarea(attrs={
      'rows': 5, 
      'placeholder': 'Description for your vault',
      'style': 'resize: none;',
    }),
    required=False,
  )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.layout = Layout(
      'name',
      Fieldset('Priority', 'priority'),
      'description',
    )
  

class VaultUpdateForm(VaultForm):
  class Meta:
    model = Vault
    fields = ['priority', 'description']

  description = forms.CharField(
    widget=forms.Textarea(attrs={
      'rows': 5, 
      'placeholder': 'Description for your vault',
      'style': 'resize: none;',
    }),
    required=False,
  )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.layout = Layout(
      Fieldset('Priority', 'priority'),
      'description',
    )


class WebsiteForm(forms.ModelForm):
  class Meta:
    model = Website
    fields = ['url']
    labels = {
      'name': '',
      'url': 'Website',
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.helper = FormHelper()
    self.helper.formtag = False


WebsiteFormset = inlineformset_factory(
  PasswordEntry, 
  Website,
  form=WebsiteForm,
  fields=['url'],
  can_delete=True,
  extra=1
)


class PasswordEntryCreateForm(forms.ModelForm):
  class Meta:
    model = PasswordEntry
    exclude = ['user', 'username', 'created_at', 'updated_at', 'is_trashed']
    labels = {
      'title': 'Title',
      'email': 'Email or username',
      'password': 'Password',
      'vault': 'Vault',
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.user = kwargs.pop('user', None)
    self.helper = FormHelper()
    self.helper.form_tag = True

    self.helper.layout = Layout(
      Field('title', label='', placeholder="Title"),
      Fieldset(
        'Login Details',
        Field('username', placeholder='Email or username'),
        Field('password', placeholder="Password")
      ),
      Fieldset(
        'Vault',
        Field('vault')
      ),
    )

  def clean_title(self):
    title = self.cleaned_data['title']
    if PasswordEntry.objects.filter(user=self.user, title__iexact=title).exists():
      raise forms.ValidationError('Password entry with this title already exists.')
    return title
    
  def clean_password(self):
    password = self.cleaned_data['password']
    return password
  
  def clean(self):
    cleaned_data = super().clean()
    return cleaned_data
  
    
class PasswordEntryUpdateForm(forms.ModelForm):
  class Meta:
    model = PasswordEntry
    exclude = ['user', 'created_at', 'updated_at', 'is_trashed']
    labels = {
      'title': 'Title',
      'email': 'Email or username',
      'password': 'Password',
      'vault': 'Vault',
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def clean(self):
    cleaned_data = super().clean()
    title = cleaned_data['title']
    return cleaned_data
  
  def save(self, commit=True):
    instance = super().save(commit=False)

    current_version = PasswordHistory.objects.filter(password_entry__pk=instance.pk, is_current=True).first()

    current_version.is_current = False
    current_version.save()

    PasswordHistory.objects.create(
      password_entry=instance,
      password=instance.password,
      is_current=True,
    )

    if commit:
      instance.save()
    
    return instance
