from django.urls import path

from . import views

urlpatterns = [
    path('', views.folders, name='folders'),
    path('<int:folder_id>', views.folder, name = 'folder'),
    path('<int:folder_id>/create', views.filecreate, name = 'create'),
    path('<int:folder_id>/edit/<int:file_id>', views.textFileEdit, name = 'textFileEdit'),
    path('<int:folder_id>/upload', views.fileUpload, name = 'fileUpload'),
    path('<int:folder_id>/view/<int:file_id>', views.textView, name = 'textview'),
    path('<int:folder_id>/view/file/<int:file_id>', views.externalFileView, name = 'externalFileView'),
    path('<int:folder_id>/delete/image/<int:file_id>', views.externalFileDelete, name = 'externalFileDelete'),
    path('<int:folder_id>/delete/text/<int:file_id>', views.textFileDelete, name = 'textFileDelete'),
]