#!/usr/bin/python3
# _*_ coding: utf-8 _*_

from . import views
from django.urls import path

app_nam = 'news'

urlpatterns = [
    path('<int:news_id>/', views.news_detail, name='detail'),
    path("list/", views.news_list, name='news-list'),
]
