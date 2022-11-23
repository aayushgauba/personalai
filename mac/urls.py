from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('chat/', include('chat.urls')),
    path('files/', include('files.urls')),
    path('events/', include('events.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
