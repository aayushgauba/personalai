from email.policy import default
from django.db import models

# Create your models here.
class Folder(models.Model):
    Name= models.CharField(max_length = 100)
    Type = models.BooleanField(default = False)

class TextFile(models.Model):
    Name = models.CharField(max_length = 20)
    File = models.TextField()
    FolderName = models.CharField(max_length = 100)

class ExternalFile(models.Model):
    Name = models.CharField(max_length = 20)
    upload = models.FileField(upload_to = 'files', blank = False)
    FolderName = models.ForeignKey(Folder, on_delete = models.CASCADE)
    FileType = models.CharField(max_length = 20)
