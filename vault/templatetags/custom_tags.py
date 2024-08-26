from django import template
from django.utils.http import urlencode


register = template.Library()

@register.simple_tag
def get_page_url(vault_list_rows_url_prefix, page_number: int = 1):
  return f"{vault_list_rows_url_prefix}&page={page_number}"


@register.simple_tag(takes_context=True)
def page_urlencode(context, page: int = None, delta: int = 0, order_by: str = '', order: str = '', **kwargs):
  resource_path = context.get('resource_path')
  query_parameters = dict()

  # order_by = kwargs.get('order_by')
  if order_by and isinstance(order_by, str):
    pass
  elif context.get('order_by'):
    order_by = context.get('order_by')
  else:
    pass
  
  # order = kwargs.get('order')
  if order and isinstance(order, str):
    pass
  elif context.get('order'):
    order = context.get('order')
  else:
    pass

  # page = kwargs.get('page')
  # if page and isinstance(page, int):
  #   pass
  # elif context.get('page_obj'):
  #   page_obj = context.get('page_obj')
  #   page = page_obj.number
  # else:
  #   page = 1

  if order_by:
    query_parameters.update({'order_by': order_by})
  if order:
    query_parameters.update({'order': order})

  # if page:
  #   query_parameters.update({'page': page + delta})

  return f'{resource_path}?{urlencode(query_parameters)}'


@register.simple_tag
def call_function(function_name, *args, **kwargs):
  function = template.Variable(function_name).resolve(None)
  if function is None:
    print(f'{function_name} not loaded')
  elif callable(function):
    return function(*args, **kwargs)
  else:
    return ""
