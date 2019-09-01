#!/usr/bin/python3
# _*_ coding: utf-8 _*_
from django.db import models
from apps.models import ModelMixin


class CourseCategory(models.Model):
    name = models.CharField(max_length=200)


class Teacher(models.Model):
    nickname = models.CharField(max_length=20)
    avatar = models.URLField()
    position = models.CharField(max_length=200)
    profile = models.TextField()


class Course(ModelMixin):
    name = models.CharField(max_length=200)
    category = models.ForeignKey('CourseCategory', on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING)
    video_link = models.URLField()
    cover_link = models.URLField()
    price = models.FloatField()
    duration = models.IntegerField()
    desc = models.TextField(default="暂无描述信息")
    pub_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"(<Course>: {self.name}, {self.id})"

