"""ECMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
import system.views
import infos.views
import check.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'login/', system.views.login),
    path(r'index_1/', system.views.index_1),
    re_path(r'delete/(\d+)/(\d+)', system.views.delete),
    re_path(r'deletes/(\d+)', system.views.deletes),

    re_path(r'teachersInfo/(\d+)', infos.views.teachersInfo),
    re_path(r'stuInfo/(\d+)', infos.views.stuInfo),
    re_path(r'copy/(\d+)/(\d+)', infos.views.copy),
    re_path(r'modFlag/(\d+)/(\d+)', infos.views.modFlag),
    re_path(r'details/(\d+)/(\d+)/(\d+)', infos.views.details),
    re_path(r'modify/(\d+)', infos.views.modify),
    re_path(r'addInfo/', infos.views.addInfo),

    re_path(r'check/(\d+)', check.views.check),
    re_path(r'modCheck/(\d+)/(\d+)', check.views.modCheck),
    re_path(r'checkModifyPage/(\d+)', check.views.checkModifyPage),
    re_path(r'checkModify/(\d+)', check.views.checkModify),

    path(r'faceRecognition/', check.views.faceRecognition),
    path(r'recognize/', check.views.recognize),
    path(r'get_face_img/', check.views.get_face_img),
    path(r'save_face_img/', check.views.save_face_img),

    # re_path(r'schedule/(\d+)', views.schedule),
    # re_path(r'schedule_dls/(\d+)/(\d+)/(\d+)', views.schedule_dls),
    # re_path(r'scheduleModify/(\d+)', views.mod_schedule),
    # re_path(r'time_tables/(\d+)', views.time_tables),
    # re_path(r'tea_timetable/(\d+)', views.tea_timetable),
    # path(r'arrange/', views.arrange),
    # path(r'arrangeRes/', views.arrangeRes),
    # path(r'vague/', views.vague),
]
