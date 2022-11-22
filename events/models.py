from django.db import models

class Event(models.Model):
    Title = models.CharField(max_length = 100)
    Date = models.CharField(max_length=100)
    Notes = models.TextField()
# Create your models here.
