from django.db import models

# Create your models here.
class Add(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField( max_length=15 ,blank=True ,null=True)
    email = models.EmailField()