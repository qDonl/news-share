#!/usr/bin/python3
# _*_ coding: utf-8 _*_
from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('img_captcha/', views.img_captcha, name='img_captcha'),
    path('sms_captcha/', views.sms_captcha, name='sms_captcha'),
]


# 测试数据
from . import test
urlpatterns += [
    path('test/', test.test_index, name='test-index'),
]
