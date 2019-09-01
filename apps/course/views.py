#!/usr/bin/python3
# _*_ coding: utf-8 _*_
import hashlib
import hmac
import os
import time

from django.conf import settings
from django.shortcuts import render

from .models import Course
from utils import restfuls


def course_index(request):
    courses = Course.objects.select_related('teacher').all()
    context = {
        'courses': courses
    }
    return render(request, 'course/course_index.html', context)


def course_detail(request, course_id):
    course = Course.objects.prefetch_related('teacher').get(pk=course_id)
    context = {
        'course': course
    }
    return render(request, 'course/course_detail.html', context)


def course_token(request):
    """百度云播放视频"""
    file = request.GET.get('video')

    expiration_time = int(time.time()) + 2 * 60 * 60
    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY

    extension = os.path.splitext(file)[1]  # 获取扩展名
    media_id = file.split('/')[-1].replace(extension, '')

    key = USER_KEY.encode('utf-8')
    message = f"/{media_id}/{expiration_time}".encode('utf-8')
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = f"{signature}_{USER_ID}_{expiration_time}"
    return restfuls.success(data={"token": token})


def course_order(request, course_id):
    course = Course.objects.get(pk=course_id)
    context = {
        'course': course
    }
    return render(request, 'course/course_order.html', context)


