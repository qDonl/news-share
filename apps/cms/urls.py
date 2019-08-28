#!/usr/bin/python3
# _*_ coding: utf-8 _*_

from . import views
from django.urls import path


app_name = 'cms'

urlpatterns = [
    path('', views.index, name='index'),
    path('news/publish/', views.PublishNewsView.as_view(), name='publish-news'),
    path('news/category/', views.news_category, name='news-category'),
    path("news/category/add/", views.add_news_category, name='add-news-category'),
    path("news/category/edit/", views.edit_news_category, name='edit-news-category'),
    path("news/category/delete/", views.delete_category_category, name='delete-news-category'),
    path("upload/", views.upload_file, name='upload'),  # 弃用
    path("banner/", views.banners, name='banner'),
    path('qntoken/', views.qntoken, name='qntoken'),
]