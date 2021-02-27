from django.db import models

# Create your models here.
class Info(models.Model):
    number = models.CharField(max_length=50)
    claz = models.CharField(max_length=100)  # 对于学生而言只能属于一个班级,对于老师而言可以教授多个班级
    name = models.CharField(max_length=50)
    sex = models.CharField(max_length=30)
    tel = models.CharField(max_length=20, default="")
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    flag = models.IntegerField() # 0为学生,1为老师,2为修理工,3为主任,4为校长
    state = models.IntegerField(default=1)# 表示是否在校/在职
    subject = models.IntegerField(default=9)
    remarks = models.CharField(max_length=100)# 备注
    img = models.CharField(max_length=100)