from django.db import models

class Event(models.Model):
    Title = models.CharField(max_length = 100)
    Date = models.DateField()
    Notes = models.TextField()
# Create your models here.
