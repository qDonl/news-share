#!/usr/bin/python3
# _*_ coding: utf-8 _*_
from . import views
from django.urls import path


app_name = 'course'


urlpatterns = [
    path('', views.course_index, name='index'),
    path('<course_id>/', views.course_detail, name='detail'),
]

