from django.urls import path

from . import views

urlpatterns = [
    path('', views.folders, name='folders'),
    path('<int:folder_id>', views.folder, name = 'folder'),
    path('<int:folder_id>/create', views.filecreate, name = 'create'),
    path('<int:folder_id>/view/<int:file_id>', views.textView, name = 'textview')
]