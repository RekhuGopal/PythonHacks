from django.db import models

# Create your models here.
class Cars(models.Model):
    care_name = models.CharField(max_length=100)
    car_version = models.CharField(max_length=3)
    car_model = models.CharField(max_length=30)