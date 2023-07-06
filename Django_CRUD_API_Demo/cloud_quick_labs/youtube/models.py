from django.db import models

# Create your models here.
class YouTube(models.Model):
    channelname = models.CharField(max_length=100)
    videoName = models.CharField(max_length=100)
    length = models.CharField(max_length=100)
