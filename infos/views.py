from django.shortcuts import render, HttpResponse, redirect
from infos import models
import json
from utils import pagination
from utils import sidebar
from utils.authentication import auth
# Create your views here.


@auth
def stuInfo(request, currentPage):
    currentPage = int(currentPage)
    if request.method == 'POST':
        request.session['clazz'] = int(request.POST.get('clazz', '9'))
    clazz = int(request.session.get('clazz', '9'))
    if clazz == 9:
        clazz_list = [1, 2, 3]
    else:
        clazz_list = [clazz]
    info = models.Info.objects.filter(claz__in=clazz_list)
    page = pagination.Page(currentPage, len(info))
    part = models.Info.objects.filter(claz__in=clazz_list)[page.start: page.end]
    return render(request, 'infos/stuInfo.html', {'Info': part, 'pageStr': page.page_str('/stuInfo'),
                                            'currentPage': currentPage})

                                        
@auth
def teachersInfo(request, currentPage):
    currentPage = int(currentPage)
    if request.method == 'POST':
        request.session['flag'] = int(request.POST.get('flag', '9'))
    flag = int(request.session.get('flag', '9'))
    if flag == 9:
        flag_list = [1, 2, 3]
    else:
        flag_list = [type]
    info = models.Info.objects.filter(flag__in=flag_list)
    page = pagination.Page(currentPage, len(info))
    part = models.Info.objects.filter(flag__in=flag_list)[page.start: page.end]
    return render(request, 'infos/teachersInfo.html', {'Info': part, 'pageStr': page.page_str('/teachersInfo'),
                                                 'currentPage': currentPage})


@auth
def copy(request, currentPage, id):
    sign = request.GET.get('sign', '1')
    if sign == '3':
        Schedule = models.Schedule.objects.filter(id=id)
        for item in Schedule:
            models.Schedule.objects.create(
                teacher_number=item.teacher_number,
                teacher_name=item.teacher_name,
                subject=item.subject,
                free_time1=item.free_time1,
                free_time2=item.free_time2,
                free_time3=item.free_time3,
                free_time4=item.free_time4,
                free_time5=item.free_time5,
                free_time6=item.free_time6,
                free_time7=item.free_time7,
                free_time8=item.free_time8
            )
        return redirect('/schedule/%s' % currentPage)
    else:
        Info = models.Info.objects.filter(id=id)
        for item in Info:
            models.Info.objects.create(number=str(eval(item.number+'+1')), claz=item.claz, name=item.name, sex=item.sex,
                                       tel=item.tel, email=item.email, address=item.address, type=item.type,
                                       flag=item.flag, remarks=item.remarks, img=item.img)
        if sign == '1':
            return redirect('/teachersInfo/%s' % currentPage)
        else:
            return redirect('/stuInfo/%s' % currentPage)


@auth
def modFlag(request, currentPage, flag):
    sign = request.GET.get('sign', '1')
    Ids = request.POST.getlist('id')
    models.Info.objects.filter(id__in=Ids).update(flag=flag)
    if sign == '1':
        return redirect('/teachersInfo/%s' % currentPage)
    else:
        return redirect('/stuInfo/%s' % currentPage)





@auth
def details(request, currentPage, id, method):
    sign = request.GET.get('sign')
    detail = models.Info.objects.filter(id=id)
    method = int(method)
    if method == 0:
        return render(request, 'infos/details.html', {'detail': detail, 'currentPage': currentPage, 'sign': sign})
    else:
        return render(request, 'infos/modify.html', {'detail': detail, 'currentPage': currentPage, 'sign': sign})


@auth
def modify(request, currentPage):
    sign = request.GET.get('sign')
    id = request.POST.get('id')
    number = request.POST.get('number')
    name = request.POST.get('name')
    sex = request.POST.get('sex')
    claz = request.POST.get('claz')
    tel = request.POST.get('tel')
    email = request.POST.get('email')
    address = request.POST.get('address')
    type = request.POST.get('type')
    flag = request.POST.get('flag')
    remarks = request.POST.get('remarks')
    file = request.FILES.get('img')
    try:
        img = 'static/img/%s' % file.name
        with open(img, mode="wb") as f:
            for line in file.chunks():
                f.write(line)
        img = '/%s' % img
    except AttributeError:
        img = models.Info.objects.filter(id=id)[0].img
    models.Info.objects.filter(id=id).update(number=number, claz=claz, name=name, sex=sex,
                               tel=tel, email=email, address=address, type=type,
                               flag=flag, remarks=remarks, img=img)
    if sign == '0':
        return redirect('/stuInfo/%s' % currentPage)
    else:
        return redirect('/teachersInfo/%s' % currentPage)


@auth
def addInfo(request):
    res = {'status': True, 'error': None, 'data': None}
    number = request.POST.get('number', None)
    name = request.POST.get('name', None)
    sex = request.POST.get('sex', None)
    claz = request.POST.get('claz', None)
    tel = request.POST.get('tel', None)
    email = request.POST.get('email', None)
    address = request.POST.get('address', None)
    type_ = request.POST.get('type', None)
    flag = request.POST.get('flag', None)
    remarks = request.POST.get('remarks', None)
    file = request.FILES.get('img')
    try:
        img = 'static/img/%s' % file.name
        with open(img, mode="wb") as f:
            for line in file.chunks():
                f.write(line)
        img = '/%s' % img
    except AttributeError:
        img = '/'
    if name != "" and number != "":
        models.Info.objects.create(
            number=number,
            claz=claz,
            name=name,
            sex=sex,
            tel=tel,
            email=email,
            address=address,
            type=type_,
            flag=flag,
            remarks=remarks,
            img=img
        )
    else:
        res['status'] = False
        res['error'] = 'name或number不能为空'
    return HttpResponse(json.dumps(res))