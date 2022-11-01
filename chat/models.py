from enum import unique
from unittest.util import _MAX_LENGTH
from django.db import models
from django.db.models import Model

# Create your models here.
class KeyWords(Model):
    Key = models.CharField(max_length=10)

class Phrase(models.Model):
    Ques = models.TextField()
    Key = models.CharField(max_length=10)
    Ans = models.TextField()

class Conversation(models.Model):
    response = models.TextField()
    time = models.TimeField()
    sender= models.CharField(max_length = 10)

