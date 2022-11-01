from django.shortcuts import render, redirect
from .models import Folder, TextFile, ExternalFile
from .forms import TextFileForm, ExternalFileForm
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

