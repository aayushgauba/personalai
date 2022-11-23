from django.shortcuts import render, redirect
from .models import Folder, TextFile, ExternalFile
from .forms import TextFileForm, ExternalFileForm
import os
# Create your views here.
def folders(request):
    files = Folder.objects.all()
    return render(request, "folders.html", context = {"folders":files})

def folder(request, folder_id):
    folder = Folder.objects.get(id = folder_id)
    textfiles = TextFile.objects.filter(FolderName = folder_id)
    externalfiles = ExternalFile.objects.filter(FolderName = folder_id)
    return render(request, "folder.html", context={"textfiles":textfiles, "externalfiles":externalfiles, "folder":folder})

def textView(request, folder_id, file_id):
    textfile = TextFile.objects.get(id = file_id)
    return render(request, "fileview.html", context = {"textfile":textfile})

def filecreate(request, folder_id):
    folder = Folder.objects.get(id = folder_id)
    form = TextFileForm()
    if request.method == 'POST':
        name = request.POST.get("Name")
        text = request.POST.get("Text")
        TextFile.objects.create(Name = name, File = text, FolderName = folder_id)
    else:
        form = TextFileForm()
    context = {
            'form':form,
        }
    return render(request, 'filecreate.html', context)

def fileUpload(request, folder_id):
    initial = {'FolderName':folder_id}
    if request.method == 'POST':
        form = ExternalFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:

        form = ExternalFileForm(initial)
    context = {
            'form':form,
        }
    return render(request, 'fileUpload.html', context)

def textFileEdit(request, folder_id, file_id):
    folder = Folder.objects.get(id = folder_id)
    textfile = TextFile.objects.get(id = file_id)
    dict = {'Name':textfile.Name, 'File':textfile.File, 'Text':textfile.File, 'FolderName':folder_id}
    form = TextFileForm()
    if request.method == 'POST':
        name = request.POST.get("Name")
        text = request.POST.get("Text")
        TextFile.objects.create(Name = name, File = text, FolderName = folder_id)
        textfile.delete()
        return redirect('folder', folder_id)
    else:
        form = TextFileForm(dict)
    context = {
            'form':form,
        }
    return render(request, 'filecreate.html', context)

def externalFileDelete(request, folder_id, file_id):
    externalfile = ExternalFile.objects.get(id = file_id)
    if request.method == 'POST':
        if len(externalfile.upload) >0:
            string = "D:/mac/"
            os.remove(string+externalfile.upload.url)        
        externalfile.delete()
        return redirect('folder', folder_id)

def textFileDelete(request, folder_id, file_id):
    textfile = TextFile.objects.get(id = file_id)
    if request.method == 'POST':
        textfile.delete()
        return redirect('folder', folder_id)    

def externalFileView(request, folder_id, file_id):
    externalfile = ExternalFile.objects.get(id = file_id)
    return render(request, "file.html", context = {"externalfile":externalfile})
    

