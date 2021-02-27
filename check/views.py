import os, sys
base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from django.shortcuts import render, redirect
from check import models as c_models
from infos import models as i_models
from utils import pagination
from utils.authentication import auth
from utils.transform import transform_img
from deepface.FR.recognition import contrast, save_feature
from datetime import datetime
import time
import cv2
# Create your views here.

@auth
def faceRecognition(request):
    return render(request, 'check/faceRecognition.html')


@auth
def recognize(request):
    clazz = request.POST.get('clazz')
    face_str = request.POST.get('face_str')
    face_img = transform_img(face_str)
    dir = "deepface/face_database/class%s" % clazz
    numbers, flags = contrast(face_img, os.path.join(dir, 'faces.csv'), 0.45)
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    day = datetime.now().isoweekday()

    for i, number in enumerate(numbers):
        try:
            name = i_models.Info.objects.get(number=number).name
            c_models.Check.objects.create(
                clazz=clazz,
                stu_number=number,
                stu_name=name,
                flag=flags[i],
                date=date,
                day=day
            )
        except:
            continue
    return render(request, 'check/faceRecognition.html')


@auth
def get_face_img(request):
    return render(request, 'check/get_face_img.html')


@auth
def save_face_img(request):
    clazz = request.POST.get('clazz')
    stu_number = request.POST.get('stu_number')
    face_str = request.POST.get('face_str')
    face_img = transform_img(face_str)
    dir = "deepface\\face_database\\class%s" % clazz
    img_path = os.path.join(dir, "img", stu_number + ".jpg")
    cv2.imwrite(img_path, face_img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    save_feature(img_path, os.path.join(dir, "faces.csv"))
    return render(request, 'check/get_face_img.html')


@auth
def check(request, currentPage):
    currentPage = int(currentPage)
    info = c_models.Check.objects.filter()
    page = pagination.Page(currentPage, len(info))
    part = c_models.Check.objects.filter()[page.start: page.end]
    return render(request, 'check/check.html', {'check': part, 'pageStr': page.page_str('/check'), 'currentPage': currentPage})


@auth
def modCheck(request, currentPage, flag):
    Ids = request.POST.getlist('id')
    c_models.Check.objects.filter(id__in=Ids).update(flag=flag)
    return redirect('/check/%s' % currentPage)


@auth
def checkModifyPage(request,currentPage):
    id = request.GET.get("id")
    detail = c_models.Check.objects.filter(id=id)
    return render(request, 'check/checkModify.html', {'detail': detail, 'currentPage': currentPage})


@auth
def checkModify(request, currentPage):
    id = request.POST.get('id')
    name = request.POST.get('name')
    number = request.POST.get('number')
    date = request.POST.get('date')
    section = request.POST.get('section')
    day = request.POST.get('day')
    remark = request.POST.get('remark')
    flag = request.POST.get('flag')
    c_models.Check.objects.filter(id=id).update(
        stu_number=number,
        stu_name=name,
        date=date,
        section=section,
        day=day,
        remark=remark,
        flag=flag
    )

    return redirect('/check/%s' % currentPage)
