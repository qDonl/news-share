#!/usr/bin/python3
# _*_ coding: utf-8 _*_
from . import views
from django.urls import path


app_name = 'course'


urlpatterns = [
    path('', views.course_index, name='course-index'),
    path('<int:course_id>/', views.course_detail, name='course-detail'),
    path('order/<int:course_id>/', views.course_order, name='course-order'),
    path("token/", views.course_token, name='course-token'),
]

