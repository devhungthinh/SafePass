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

class Formset(LayoutObject):
  template = 'vault/formset.html'

  def __init__(self, formset_name_in_context, template=None):
    self.formset_name_in_context = formset_name_in_context
    self.fields = []
    if template:
      self.template = template

  def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
    formset = context[self.formset_name_in_context]
    return render_to_string(self.template, {
      'formset': formset
    })