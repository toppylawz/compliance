from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

from django.contrib import admin

admin.site.site_header = 'Compliance Application'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('standards/', include('compliance.urls')),
    path('', views.home, name='home'),
    path('__debug__/', include('debug_toolbar.urls')),
    # path('grappelli/', include('grappelli.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)