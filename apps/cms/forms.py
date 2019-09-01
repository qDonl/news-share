#!/usr/bin/python3
# _*_ coding: utf-8 _*_
from django import forms

from apps.course.models import Course
from apps.form import FormMixin
from apps.news.models import News
from .models import Banner


class EditNewsCategoryForm(forms.Form, FormMixin):
    pk = forms.IntegerField(error_messages={"required": "请输入分类主键"})
    name = forms.CharField(error_messages={"required": "请输入分类名称"})


class PublishNewsForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField(error_messages={"required": "请选择新闻分类"})
    news_id = forms.IntegerField(required=False)

    class Meta:
        model = News
        exclude = ['pub_time', 'category', 'author']
        error_messages = {
            'title': {
                'required': "请输入新闻标题",
                "max_length": "新闻标题不能超过255个字符",
            },
            'content': {
                "required": "请输入新闻内容"
            },
            'desc': {
                'required': "请输入新闻简述",
                'max_length': "新闻简述不能超过255个字符"
            },
            'thumbnail': {
                'required': "请插入新闻缩略图"
            }
        }


class AddBannerForm(forms.ModelForm, FormMixin):
    """添加轮播图表单验证"""

    class Meta:
        model = Banner
        fields = ('image_url', 'link_to', 'priority')
        error_messages = {
            'image_url': {
                'required': '请上传轮播图',
                'invalid': "轮播图链接格式错误"
            },
            'link_to': {
                'required': "请设置跳转链接",
                'invalid': "请设置正确的跳转链接格式",
            },
            'priority': {
                'required': "请设置轮播图优先级",
                'invalid': "请设置正确格式的优先级(整形)"
            }
        }


class EditBannerForm(AddBannerForm):
    # 修改轮播图
    pk = forms.IntegerField()


class PublishCourseForm(forms.ModelForm, FormMixin):
    """发布课程"""
    category_id = forms.IntegerField()
    teacher_id = forms.IntegerField()

    class Meta:
        model = Course
        exclude = ('pub_time', 'teacher', 'category')
        error_messages = {
            "name": {"required": "请输入课程标题"},
            "category_id": {'required': "请选择课程分类"},
            'teacher_id': {"required": "请选择讲师"},
            "video_link": {"required": "请上传授课视频", 'invalid': "请输入有效的视频连接"},
            'cover_link': {"required": "请上传课程封面", 'invalid': "请输入有效的封面连接"},
            'price': {'required': "请标注价格"},
            'duration': {"required": "请添加课程时长"},
            'desc': {"required": "请添加描述信息"}
        }
