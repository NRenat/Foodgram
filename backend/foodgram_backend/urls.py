from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from foodgram_backend import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('foodgram_api.urls')),
]
