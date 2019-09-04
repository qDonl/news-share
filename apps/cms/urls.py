#!/usr/bin/python3
# _*_ coding: utf-8 _*_

from . import views, staff_view
from django.urls import path

app_name = 'cms'

urlpatterns = [
    path('', views.index, name='index'),
    # 新闻 映射
    path('news/publish/', views.PublishNewsView.as_view(), name='publish-news'),
    path('news/category/', views.news_category, name='news-category'),
    path("news/category/add/", views.add_news_category, name='add-news-category'),
    path("news/category/edit/", views.edit_news_category, name='edit-news-category'),
    path("news/category/delete/", views.delete_category_category, name='delete-news-category'),
    path("news/list/", views.NewsListView.as_view(), name='news-list'),
    path("news/edit/", views.edit_news, name='news-edit'),
    path("news/remove/", views.remove_news, name='news-remove'),
    # 轮播图 映射
    path("banner/", views.banner, name='banner'),
    path('banner/add/', views.add_banner, name="banner-add"),
    path('banner/edit/', views.edit_banner, name="banner-edit"),
    path('banner/load/', views.load_banner, name='banner-load'),
    path("banner/remove/", views.remove_banner, name='banner-remove'),
    path('qntoken/', views.qntoken, name='qntoken'),  # 上传文件到七牛云
    path("upload/", views.upload_file, name='upload'),  # 上传文件到本地
]

# 课程管理
urlpatterns += [
    path('course/publish/', views.PublishCourseView.as_view(), name='course-publish'),
]

# 员工管理
urlpatterns += [
    path("staff/", staff_view.staff_operate, name='staff-operate'),
    path('staff/add/', staff_view.AddStaffView.as_view(), name="staff-add"),
    path("staff/remove/", staff_view.remove_staff, name='staff-remove'),
    path("staff/update/", staff_view.update_staff, name='staff-update'),
]
