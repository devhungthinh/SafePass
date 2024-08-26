from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.http import urlencode
from django.db.models import Count
from django.http import (
  HttpResponse,
  HttpResponseNotAllowed,
  JsonResponse,
)
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import transaction


from config.logging_config import logger
from .models import (
  Vault,
  PasswordEntry,
  PasswordHistory,
)
from .forms import (
  VaultCreateForm,
  VaultUpdateForm,
  PasswordEntryCreateForm,
  PasswordEntryUpdateForm,
  WebsiteFormset
)
from .mixins import (
  VaultListQueryMixin,
  PasswordEntryQueryMixin,
)


class VaultListView(LoginRequiredMixin, TemplateView):
  template_name = 'vault/vault_list.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    created = self.request.GET.get('created', False)
    updated = self.request.GET.get('updated', False)

    if created or updated:
      context['show_recent_updated_vault'] = True
      most_recent_modified_vault = Vault.objects.filter(user=self.request.user).order_by('-updated_at').first()
      recent_modified_vault_url = f"{reverse('vault:vault_detail_partial',kwargs={'pk': most_recent_modified_vault.pk})}"
      if created:
        context['created'] = True
        recent_modified_vault_url += f"?created=True"
      elif updated:
        context['updated'] = True
        recent_modified_vault_url += f"?updated=True"
      context['recent_modified_vault_url'] = recent_modified_vault_url

    context['resource_path'] = reverse('vault:vault_list_rows')
    return context
  

class VaultRowsListView(LoginRequiredMixin, VaultListQueryMixin, ListView):
  model = Vault
  template_name = 'vault/vault_rows.html'

  def get_queryset(self):
    qs = super().get_queryset()
    return self.get_queryset_unified(qs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    order_by = self.request.GET.get('order_by', 'name')
    order = self.request.GET.get('order', 'asc')
    vault_list_rows_path = reverse('vault:vault_list_rows')
    context.update({
      'resource_path': f"{vault_list_rows_path}",
      'order_by': order_by,
      'order': order,
    }) 
    return context
  

class VaultDetailView(LoginRequiredMixin, DetailView):
  model = Vault
  template_name = 'vault/vault_detail.html'
  context_object_name = 'vault'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    vault = context['vault']

    if vault.password_entries.count() == 0:
      context['not_contain_any_entires'] = True
      return context
    
    all_entries_trashed = not vault.password_entries.filter(is_trashed=False).exists()
    if all_entries_trashed:
      context['all_entries_trashed'] = True
      return context
    
    return context
  

@login_required
def vault_detail_partial(request, pk):
  if request.method == 'GET':
    created = request.GET.get('created', False)
    updated = request.GET.get('updated', False)
    vault = get_object_or_404(Vault, pk=pk, user=request.user)

    context = {'vault': vault}
    if created:
      context.update({'created': True})
    elif updated:
      context.update({'updated': True})

    return render(request, 'vault/vault_detail_partial.html', context)
  else:
    return HttpResponseNotAllowed(['GET'])


class VaultCreateView(LoginRequiredMixin, CreateView):
  model = Vault
  form_class = VaultCreateForm
  template_name = 'vault/vault_create.html'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  
  def get_success_url(self):
    return f"{reverse('vault:vault_list')}?created=True"
  

class VaultUpdateView(LoginRequiredMixin, UpdateView):
  model = Vault
  form_class = VaultUpdateForm
  template_name = 'vault/vault_update.html'
  context_object_name = 'vault'

  def form_valid(self, form):
    messages.success(self.request, 'Vault was updated successfully.')
    return super().form_valid(form)
                             
  def get_success_url(self):
    return f"{reverse('vault:vault_list')}?updated=True"
  
  
class VaultDeleteView(LoginRequiredMixin, DeleteView):
  model = Vault
  template_name = 'vault/vault_delete.html'
  context_object_name = 'vault'

  def get_success_url(self) -> str:
    return reverse_lazy('vault:vault_list')

@login_required
def delete_vault(request, pk):
  if request.method == 'DELETE':
    logger.info('executed inside delete_vault')
    response_data = dict()
    try:
      vault = get_object_or_404(Vault, pk=pk, user=request.user)
      vault.delete()
      response_data.update({
        'success': True,
        'message': 'You have successfully deleted this vault.'
      })
      return JsonResponse(status=200, data=response_data)
    except Vault.DoesNotExist:
      response_data = {
        'success': False,
        'message': "You can not delete vault because it does not exists!."
      }
      return JsonResponse(status=404, data=response_data)
  else:
    allowed_methods = ['DELETE']
    return HttpResponseNotAllowed(allowed_methods)
  

@login_required
def delete_multiple_vault(request, *args, **kwargs):
  if request.method == 'POST':
    pks = request.POST.getlist('pks');
    Vault.objects.filter(user=request.user, pk__in=pks).delete();

    response_data = {
      'success': True,
      'message': "You have successfully deleted all selected vaults.",
    }
    return JsonResponse(status=200, data=response_data)
  else:
    return HttpResponseNotAllowed(['POST'])
  

@login_required
def move_multiple_password_entry_to_trash(request, *args, **kwargs):
  if request.method == 'POST':
    pks = request.POST.getlist('pks')
    filtered_entries = PasswordEntry.objects.filter(user=request.user, pk__in=pks)
    if filtered_entries.exists():
      for password_entry in filtered_entries:
        password_entry.is_trashed = True
        password_entry.save()
      response_data = {
        'success': True,
        'message': 'You have successfully moved the password list to trash.',
      }
      return JsonResponse(status=200, data=response_data)
    else:
      response_data = {
        'success': False,
        'message': 'Password list does not exist.',
      }
      return JsonResponse(status=404, data=response_data)
  else:
    return HttpResponseNotAllowed(['POST'])
  

class VaultListRowsSearchView(LoginRequiredMixin, ListView):
  model = Vault
  template_name = 'vault/vault_list_rows.html'
  paginate_by = 6

  def get_queryset(self):
    queryset = super().get_queryset()
    query = self.request.GET.get('query')
    if query is not None:
      return queryset.filter(name__icontains=query)
    

class PasswordEntryListView(LoginRequiredMixin, ListView):
  model = PasswordEntry
  paginate_by = 5
  template_name = 'vault/password_entry_list.html'

  def get_queryset(self):
    sorting_order = self.request.GET.get('sort', 'title')
    queryset = super().get_queryset()
    return queryset.order_by(sorting_order)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    created = self.request.GET.get('created', False)
    updated = self.request.GET.get('updated', False)

    if created or updated:
      context['show_recent_updated'] = True
      most_recent_modified_password_entry = PasswordEntry.objects.filter(user=self.request.user).order_by('-updated_at').first()
      recent_modified_password_entry_url = f"{reverse('vault:password_detail_partial', kwargs={'pk': most_recent_modified_password_entry.pk})}"
      if created:
        context['created'] = True
      if updated:
        context['updated'] = True
      context['recent_modified_password_entry_url'] = recent_modified_password_entry_url

    password_entry_list = context['object_list']
    for password_entry in password_entry_list:
      first_website = password_entry.websites.first()
      if first_website is not None:
        password_entry.website_url = first_website.url
    return context
  

class PasswordEntryRowsListView(LoginRequiredMixin, PasswordEntryQueryMixin, ListView):
  model = PasswordEntry
  template_name = 'vault/password_entry_rows.html'

  def get_queryset(self):
    qs = super().get_queryset()
    return self.get_queryset_unified(qs)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    order_by = self.request.GET.get('order_by', 'title')
    order = self.request.GET.get('order', 'asc')
    password_entry_list_rows_path = reverse('vault:password_list_rows')
    context.update({
      'resource_path': f'{password_entry_list_rows_path}',
      'order_by': order_by,
      'order': order,
    })
    return context


class PasswordEntryDetailView(LoginRequiredMixin, DetailView):
  model = PasswordEntry
  template_name = 'vault/password_entry_detail.html'
  context_object_name = 'password_entry'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return context
  

@login_required
def password_entry_detail_partial(request, pk):
  if request.method == 'GET':
    password_entry = get_object_or_404(PasswordEntry, user=request.user, pk=pk)
    context = {'password_entry': password_entry}
    return render(request, 'vault/password_entry_detail_partial.html', context)
  else:
    return HttpResponseNotAllowed(['GET'])
  

class PasswordEntryCreateView(LoginRequiredMixin, CreateView):

  model = PasswordEntry
  form_class = PasswordEntryCreateForm
  template_name = 'vault/password_entry_create.html'

  def get_form(self, form_kwargs=None):
    form = super().get_form(form_kwargs)
    form.user = self.request.user
    return form

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    if self.request.method == 'POST':
      context['formset'] = WebsiteFormset(self.request.POST, instance=self.object)
    else:
      context['formset'] = WebsiteFormset(instance=self.object)
    return context
  
  def post(self, request, *args, **kwargs):
    self.object = None
    form = self.get_form()
    formset = WebsiteFormset(request.POST, request.FILES, instance=self.object)
    if form.is_valid() and formset.is_valid():
      logger.info('valid')
      return self.form_valid(form, formset)
    else:
      logger.info('invalid')
      return self.form_invalid(form, formset)
    
  def form_valid(self, form, formset):
    with transaction.atomic():
      form.instance.user = self.request.user
      self.object = form.save(commit=True)
      formset.instance = self.object
      formset.save()
    return super().form_valid(form)
  
  def form_invalid(self, form, formset):
    for field, errors in form.errors.items():
      for error in errors:
        messages.error(self.request, f'{field}: {error}')

    context = {'form': form, 'formset': formset}
    return self.render_to_response(context)

  def get_success_url(self):
    return f"{reverse('vault:password_list')}?created=True"
  

class PasswordEntryUpdateView(LoginRequiredMixin, UpdateView):
  model = PasswordEntry
  form_class = PasswordEntryUpdateForm
  template_name = 'vault/password_entry_update.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    if self.request.method == 'POST':
      context['website_formset'] = WebsiteFormset(self.request.POST, instance=self.object)
    else:
      context['website_formset'] = WebsiteFormset(instance=self.object)
    return context
  
  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    form = self.get_form()
    formset = WebsiteFormset(request.POST, request.FILES, instance=self.object)
    if form.is_valid() and formset.is_valid():
      return self.form_valid(form, formset)
    else:
      return self.form_invalid(form, formset)
    
  def form_valid(self, form, formset):
    messages.info(self.request, 'Password Entry updated successfully.')
    formset.save()
    return super().form_valid(form)
  
  def form_invalid(self, form, formset):
    messages.info(self.request, 'Password Entry updated failed.')
    context = {'form': form, 'website_formset': formset}
    return self.render_to_response(context)

  def get_success_url(self):
    return f"{reverse('vault:password_list')}?updated=True"
  

class PasswodEntryDeleteView(LoginRequiredMixin, DeleteView):
  model = PasswordEntry
  template_name = 'vault/password_entry_delete.html'
  context_object_name = 'password_entry'
  success_url = reverse_lazy('vault:trashed_password_entries')


@login_required
def delete_password_entry(request, pk, *args, **kwargs):
  if request.method == 'DELETE':
    data = dict()
    password_entry = PasswordEntry.objects.filter(user=request.user, pk=pk).first()
    if password_entry:
      password_entry.delete()
      data.update({
        'success': True,
        'message': 'You have successfully deleted the password.'
      })
      return JsonResponse(status=200, data=data)
    else:
      data.update({
        'success': False,
        'message': 'This password is not found.'
      })
  else:
    return HttpResponseNotAllowed(['DELETE'])
  

class RemovePasswordEntryFromVaultView(LoginRequiredMixin, View):
  def post(self, request, *args, **kwargs):
    pk = self.kwargs.get('pk')
    password_entry = get_object_or_404(PasswordEntry, pk=pk)
    stored_vault_pk = password_entry.vault.pk
    password_entry.vault = None
    password_entry.save()
    return redirect('vault:vault_detail', pk=stored_vault_pk)


@login_required
def remove_password_entry_from_vault(request, pk: int):
  if request.method == 'DELETE':
    password_entry = get_object_or_404(PasswordEntry, user=request.user, pk=pk)
    vault_name = password_entry.vault.name
    password_entry.vault = None
    password_entry.save()
    response_data = {
      'success': True,
      'message': f'You have successfully removed {password_entry.title} from {vault_name}.',
    }
    return JsonResponse(status=200, data=response_data)
  else:
    return HttpResponseNotAllowed(['DELETE'])


class MovePasswordEntryToTrashView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    pk = self.kwargs.get('pk')
    password_entry = get_object_or_404(PasswordEntry, pk=pk)
    password_entry.is_trashed = True
    password_entry.save()
    return redirect('vault:password_list')
  

@login_required
def move_password_entry_to_trash(request, pk, *args, **kwargs):
  if request.method == 'GET':
    try:
      password_entry = get_object_or_404(PasswordEntry, user=request.user, pk=pk)
      password_entry.is_trashed = True
      password_entry.save()
      response_data = {
        'success': True,
        'message': "You have successfully put the password into the trash."
      }
      return JsonResponse(status=200, data=response_data)
    except PasswordEntry.DoesNotExist:
      response_data = {
        'success': False,
        'message': "Instance not found on system."
      }
      return JsonResponse(status=404, data=response_data)
  else:
    return HttpResponseNotAllowed(['GET'])
  

@login_required
def restore_password_entry(request, pk, *args, **kwargs):
  if request.method == 'GET':
    response_data = dict()
    password_entry = PasswordEntry.objects.filter(user=request.user, pk=pk).first()
    if password_entry:
      password_entry.is_trashed = False
      password_entry.save()
      response_data.update({
        'success': True,
        'message': 'You have successfully recovered your password.'
      })
      return JsonResponse(status=200, data=response_data)
    else:
      response_data.update({
        'success': False,
        'message': 'This password is not found.'
      })
      return JsonResponse(status=404, data=response_data)
  else:
    return HttpResponseNotAllowed(['GET'])


class TrashedPasswordEntryListView(LoginRequiredMixin, ListView):
  model = PasswordEntry
  template_name = 'vault/trashed_password_entry_list.html'

  def get_queryset(self):
    return super().get_queryset().filter(is_trashed=True).order_by('title')

class TrashedPasswordEntryRowsView(LoginRequiredMixin, ListView):
  model = PasswordEntry
  template_name = 'vault/trashed_password_entry_rows.html'

  def get_queryset(self):
    return super().get_queryset().filter(is_trashed=True).order_by('title')
  
  
class PasswordHistoryListView(LoginRequiredMixin, ListView):
  model = PasswordHistory
  paginate_by = 5
  template_name = 'vault/password_history_list.html'

  def get_queryset(self):
    password_entry_id = self.kwargs.get('pk')
    return PasswordHistory.objects.filter(password_entry_id=password_entry_id).order_by('-updated_at')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['password_entry_id'] = self.kwargs.get('pk')
    return context
  

class PasswordHistoryDetailView(LoginRequiredMixin, DetailView):
  model = PasswordHistory
  template_name = 'vault/password_history_detail.html'
  # context_object_name = 'password_history'


class PasswordHistoryDeleteView(DeleteView):
  model = PasswordHistory
  template_name = 'vault/passwod_history_delete.html'

  def get_context_data(self, **kwargs):
    return super().get_context_data(**kwargs)

  def form_valid(self, form):
    object = self.get_object()
    self.password_entry_pk = object.password_entry.pk

    if object.is_current:
      messages.error(self.request, 'You cannot delete this record because this is the current password.')
      return redirect('vault:password_history_list', pk=self.password_entry_pk)
    else:
      return super().form_valid(form)

  def get_success_url(self) -> str: 
    return reverse_lazy('vault:password_history_list', kwargs={'pk': self.password_entry_pk})


class ReuseMostRecentOldPasswordView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    password_entry_pk = kwargs.get('pk')
    
    if password_entry_pk is None:
      messages.info(request, 'Password Entry Not Found')
      return render(request, '404.html', status=404)
    
    try:
      password_entry = PasswordEntry.objects.get(pk=password_entry_pk)
      password_history = password_entry.history.order_by('-updated_at')
      if password_history is not None:
        if len(password_history) >= 2:
          current_version = password_history[0]
          recent_old_version = password_history[1]

          password_entry.password = recent_old_version.password
          password_entry.save()

          current_version.is_current = False
          current_version.save()

          recent_old_version.is_current = True
          recent_old_version.save()

          messages.info(request, f'Reuse the most recent old password successfully. Current password is: {password_entry.password}')
          return redirect('vault:password_history_list', pk=password_entry_pk)
        elif len(password_history) == 1:
          messages.info(request, f'Current password has never been changed.')
          return redirect('vault:password_history_list', pk=password_entry_pk)
        else:
          messages.info(request, 'Current password has no password history.')
          return redirect('vault:password_history_list', pk=password_entry_pk)
      else:
        messages.info(request, 'Current password has no password history.')
        return redirect('vault:password_history_list', pk=password_entry_pk)
    except PasswordEntry.DoesNotExist:
      messages.info(request, 'Password Entry Not Found')
      return render(request, '404.html', status=404)
    

class PasswordHistorySetView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    password_history_pk = self.kwargs.get('pk')
    try:
      password_history = PasswordHistory.objects.get(pk=password_history_pk)
      password_entry = password_history.password_entry
      if password_entry is not None:
        current_version = PasswordHistory.objects.filter(password_entry__pk=password_entry.pk, is_current=True).first()
        current_version.is_current = False
        current_version.save()

        password_entry.password = password_history.password
        password_entry.save()

        password_history.is_current = True
        password_history.save()

        messages.success(request, 'You have successfully set this password as your account password.')
        return redirect('vault:password_history_list', pk=password_entry.pk)
      else:
        messages(request, 'Password history accessed is not associated with any password.')
        return render(request, '404', status=404)
    except PasswordHistory.DoesNotExist:
      messages(request, 'Current password does not contain any password history.')
      return render(request, '404.tml', status=404)
