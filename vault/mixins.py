from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.db.models import Q


from typing import List, Tuple


from .models import Vault


def check_for_none(func):
  def wrapper(*args, **kwargs):
    for arg in args:
      if arg is None:
        return None
    for key, value in kwargs.items():
      if value is None:
        return None
    return func(*args, **kwargs)
  return wrapper

  
class VaultListQueryMixin:
  @check_for_none
  def get_user_authored(self, qs):
    return qs.filter(user=self.request.user).annotate(num_password_entries=Count('password_entries'))
  
  @check_for_none
  def get_searched(self, qs):
    query = self.request.GET.get('query')
    if query:
      return qs.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
      )
    return qs

  @check_for_none
  def get_ordered(self, qs):
    order_by = self.request.GET.get('order_by', 'name')
    order = self.request.GET.get('order', 'asc')

    if order_by == 'password_entries':
      order_by = 'num_password_entries'

    ordering = f'{order_by}'
    if order == 'desc':
      ordering = f'-{order_by}'

    return qs.order_by(ordering)
  
  @check_for_none
  def get_queryset_unified(self, qs):
    qs = self.get_user_authored(qs)
    qs = self.get_searched(qs)
    qs = self.get_ordered(qs)
    return qs


class PaginateMixin:
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    page = self.request.GET.get('page', 1)
    paginator = Paginator(context['object_list'], self.paginate_by)

    try:
      context['object_list'] = paginator.get_page(page)
    except PageNotAnInteger:
      context['object_list'] = paginator.get_page(1)
    except EmptyPage:
      context['object_list'] = paginator.get_page(paginator.num_pages)

    context['paginator'] = paginator
    context['page_obj'] = context['object_list']
    return context
  

class PasswordEntryQueryMixin:
  @check_for_none
  def get_user_authored(self, qs):
    return qs.filter(user=self.request.user)
  
  @check_for_none
  def get_searched(self, qs):
    query = self.request.GET.get('q')
    if query:
      return qs.filter(
        Q(title__icontains=query)
      )
    return qs
    
  @check_for_none
  def get_ordered(self, qs):
    attribute_to_order = self.request.GET.get('order_by', 'title')
    order = self.request.GET.get('order', 'asc')

    if order == 'asc':
      ordering = f'{attribute_to_order}'
    else:
      ordering = f'-{attribute_to_order}'
      
    return qs.order_by(ordering)

  @check_for_none
  def get_queryset_unified(self, qs):
    qs = self.get_user_authored(qs)
    qs = self.get_searched(qs)
    qs = self.get_ordered(qs)
    return qs
