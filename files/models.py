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
    upload = models.ImageField(upload_to = 'file', blank = False)
    FolderName = models.CharField(max_length = 1000)
    FileType = models.CharField(choices=(("Document", "Document"), ("Image", "Image"), ("Audio", "Audio")), max_length=100)
