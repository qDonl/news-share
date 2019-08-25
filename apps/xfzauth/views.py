#!/usr/bin/python3
# _*_ coding: utf-8 _*_

from io import BytesIO

from django.contrib.auth import login, authenticate, logout, get_user_model
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from django.views.decorators.http import require_POST

from apps.xfzauth.forms import RegisterForm
from utils import restfuls
from utils.captcha.xfzcaptcha import Captcha
from .forms import LoginForm

User = get_user_model()


@require_POST
def register_view(request):
    # 用户注册
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.objects.create_user(telephone=telephone, username=username, password=password)
        login(request, user)  # 用户注册成功, 将会自动登录
        return restfuls.success()
    return restfuls.bad_request(msg=form.get_errors())


@require_POST
def login_view(request):
    # 用户登录
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get("telephone")
        password = form.cleaned_data.get("password")
        remember = form.cleaned_data.get("remember")

        user = authenticate(request, username=telephone, password=password)
        if user and user.is_active:
            if remember:
                request.session.set_expiry(None)  # 不记住密码
            else:
                request.session.set_expiry(0)

            login(request, user)
            return restfuls.success()  # 登录成功
        else:
            return restfuls.forbidden(msg="账号或密码错误")  # 登录失败
    else:
        return restfuls.bad_request(msg=form.get_errors(), data=form.get_errors())  # 表单验证失败


def logout_view(request):
    # 用户 注销
    logout(request)
    return redirect(reverse('index'))


def img_captcha(request):
    # 图片验证码 视图函数
    text, image = Captcha.gene_code()
    cache.set(text.lower(), text.lower(), 5 * 60)
    print(f"图形验证码: {text}")
    # BytesIO 相当于一个管道, 用于存储图片
    out = BytesIO()
    image.save(out, 'png')
    # 设置数据流的读取方式为: 从一开始开始读(默认情况下, 读取数据后seek会往后跑)
    out.seek(0)
    response = HttpResponse(content_type='image/png')
    # 从数据流中读取图片数据
    response.write(out.read())
    # 文件长度 = 当前数据流从开始到 读取完后的位置(也就是数据流的长度)
    response['Content-length'] = out.tell()
    return response


def sms_captcha(request):
    # 短信验证码视图函数
    telephone = request.GET.get("telephone")
    exists = User.objects.filter(telephone=telephone).exists()
    if exists:
        return restfuls.bad_request(msg="该手机号已被注册!")

    captcha = Captcha.gene_text()
    cache.set(telephone, captcha.lower(), 5 * 60)
    print(f"""
    手机号码: {telephone}
    验证码: {captcha}
    """)
    return restfuls.success()


