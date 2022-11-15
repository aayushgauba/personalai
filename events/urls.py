from django.urls import path

from . import views

urlpatterns = [
    path('', views.events, name='events'),
    path('<int:day>/<int:week>', views.event, name='event'),
]