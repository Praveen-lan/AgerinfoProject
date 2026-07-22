from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.static import serve as static_serve
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('panel/', TemplateView.as_view(template_name='admin.html'), name='admin-panel'),
    path('admin.html', TemplateView.as_view(template_name='admin.html')),
    path('index.html', TemplateView.as_view(template_name='index.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    frontend = str(settings.FRONTEND_DIR)

    def serve_frontend(request, path=''):
        return static_serve(request, path, document_root=frontend)

    frontend_extensions = ('.js', '.css', '.png', '.jpeg', '.jpg', '.ico', '.svg', '.webp')
    urlpatterns += [
        re_path(r'^(?P<path>[\w\-\.]+\.(js|css|png|jpeg|jpg|ico|svg|webp))$', serve_frontend),
    ]
