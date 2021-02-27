from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    flag = models.IntegerField()
    email = models.CharField(max_length=50)
    tel = models.CharField(max_length=20, default="")


class System(models.Model):
    column = models.CharField(max_length=50)
    item1 = models.CharField(max_length=50, blank=True)
    item2 = models.CharField(max_length=50, blank=True)
    item3 = models.CharField(max_length=50, blank=True)
    url1 = models.CharField(max_length=50, blank=True)
    url2 = models.CharField(max_length=50, blank=True)
    url3 = models.CharField(max_length=50, blank=True)
    flag = models.IntegerField(default=4)
