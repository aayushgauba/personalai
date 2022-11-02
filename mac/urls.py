from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('chat/', include('chat.urls')),
    path('files/', include('files.urls')),
    path('events/', include('events.urls')),
]
