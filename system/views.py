from django.shortcuts import render, HttpResponse, redirect
from system import models as s_models
from infos import models as i_models
from check import models as c_models
import json
from utils import pagination
from utils import sidebar
from utils.authentication import auth

# Create your views here.
def login(request):
    error_msg = ""
    if request.method == "POST":
        user = request.POST.get('username', None)
        pwd = request.POST.get('password', None)
        flag = int(request.POST.get('type', None))
        userInfo = s_models.User.objects.filter(username=user, password=pwd, flag=flag)
        for item in userInfo:
            if item is not None:
                if flag == 3:# 为其他权限界面留下可扩展的可能
                    res = redirect('/index_1/')
                    res.set_cookie('flag', flag)
                    res.set_cookie('username', user)
                    res.set_cookie('is_login', True)
                    return res
                else:
                    return redirect('/login/')
        else:
            error_msg = "用户类型、用户名或密码错误"
    return render(request, 'system/login.html', {'error_msg': error_msg})


@auth
def index_1(request):
    flag = int(request.COOKIES.get('flag'))
    username = request.COOKIES.get('username')
    logger = s_models.System.objects.filter(flag=flag)
    bar = sidebar.Sidebar(logger, username, flag)
    sidebar_str = bar.sidebar_str()
    request.session['sidebarStr'] = sidebar_str
    return render(request, 'system/index_1.html')


@auth
def delete(request, currentPage, id):
    sign = request.GET.get('sign')
    if sign == '0':
        i_models.Info.objects.filter(id=id).delete()
        return redirect('/stuInfo/%s' % currentPage)
    elif sign == '1':
        i_models.Info.objects.filter(id=id).delete()
        return redirect('/teachersInfo/%s' % currentPage)
    elif sign == '2':
        c_models.Check.objects.filter(id=id).delete()
        return redirect('/check/%s' % currentPage)


@auth
def deletes(request, currentPage):
    sign = request.GET.get('sign')
    Ids = request.POST.getlist('id')
    if sign == '0':
        i_models.Info.objects.filter(id__in=Ids).delete()
        return redirect('/stuInfo/%s' % currentPage)
    elif sign == '1':
        i_models.Info.objects.filter(id__in=Ids).delete()
        return redirect('/teachersInfo/%s' % currentPage)
    elif sign == '2':
        c_models.Check.objects.filter(id__in=Ids).delete()
        return redirect('/check/%s' % currentPage)
