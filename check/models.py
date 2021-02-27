from django.db import models

# Create your models here.

class Check(models.Model):
    clazz = models. CharField(max_length=50)
    stu_number = models.CharField(max_length=50)
    stu_name = models.CharField(max_length=50)
    flag = models.IntegerField(default=0)
    date = models.CharField(max_length=50)
    day = models.IntegerField(null=True)
    section = models.IntegerField(null=True)
    lesson = models.CharField(max_length=50)
    remark = models. CharField(max_length=200, null=True)