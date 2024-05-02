
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from rsmapp import views as app_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('rsmapp.url')),
    path('accounts/', include('django.contrib.auth.urls')),
]




urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
