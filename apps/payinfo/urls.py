#!/usr/bin/python3
# _*_ coding: utf-8 _*_

from . import views
from django.urls import path

app_name = 'payinfo'

urlpatterns = [
    path('', views.index, name='index'),
]
