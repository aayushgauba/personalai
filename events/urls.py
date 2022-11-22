from django.urls import path

from . import views

urlpatterns = [
    path('', views.events, name='events'),
    path('<int:day>/<int:week>', views.event, name='event'),
    path('<int:day>/<int:week>/<int:event_id>', views.eventItem, name='eventItem'),
    path('<int:day>/<int:week>/<int:event_id>/edit', views.eventEdit, name='eventEdit'),
    path('delete/<int:event_id>', views.eventDelete, name = 'eventDelete'),
]