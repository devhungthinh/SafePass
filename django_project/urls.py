from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('vault/', include('vault.urls', namespace='vault')),
    path('users/', include('users.urls', namespace='users')),
]

if settings.DEBUG:
    import debug_toolbar

    # urlpatterns = [
    #     path("__debug__/", include(debug_toolbar.urls)),
    # ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
