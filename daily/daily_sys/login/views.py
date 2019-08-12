#coding=utf-8
from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from daily.models import Employees
from .form import UserForm,RegisterForm


def index(request):
    pass
    return render(request, 'login/index.html')

def login(request):
    if request.session.get('is_login',None):
        return HttpResponseRedirect(reverse('daily:index'))

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            try:
                user = auth.authenticate(username=username, password=password)
                try:
                    em = Employees.objects.get(user=user)
                    request.session['company_id'] = em.company.id
                except:
                    print('公司写入失败')
                if user:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.username
                    return HttpResponseRedirect(reverse('daily:index'))
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return HttpResponseRedirect(reverse('daily:index'))
    
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = Employees.objects.filter(user__username=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = Employees.objects.filter(user__email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = User.objects.create()
                new_user.username = username
                new_user.password = make_password(password1)
                new_user.email = email

                new_user.save()
                return HttpResponseRedirect(reverse('login:login'))  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login',None):
        return HttpResponseRedirect(reverse('login:login'))
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return HttpResponseRedirect(reverse('login:login'))
