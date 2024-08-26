from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import (
  LoginView,
  LogoutView,
  PasswordChangeView,
  PasswordChangeDoneView,
)


from .views import SignUpView


app_name = 'accounts'

urlpatterns = [
  path('login/', LoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
  path('signup/', SignUpView.as_view(), name='signup'),
  path('accounts/password/change/', 
       PasswordChangeView.as_view(
         template_name='registration/password_change_form.html',
         success_url=reverse_lazy('accounts:password_change_done')
       ),
       name='password_change'
  ),
  path('accounts/password/change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
]
