#!/usr/bin/python3
# _*_ coding: utf-8 _*_

from functools import wraps
from utils import restfuls
from django.shortcuts import redirect
from django.urls import reverse


# 用户认证自定义装饰器(ajax)
def auth_login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)

        if request.is_ajax():
            return restfuls.unauthorized(msg="请先登录")
        return redirect('/')

    return wrapper


def auth_superuser_required(viewfunc):
    @wraps(viewfunc)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return viewfunc(request, *args, **kwargs)
        return redirect(reverse('cms:index'))

    return wrapper
