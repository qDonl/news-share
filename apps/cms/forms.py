#!/usr/bin/python3
# _*_ coding: utf-8 _*_
from django import forms
from apps.form import FormMixin
from apps.news.models import News


class EditNewsCategoryForm(forms.Form, FormMixin):
    pk = forms.IntegerField(error_messages={"required": "请输入分类主键"})
    name = forms.CharField(error_messages={"required": "请输入分类名称"})


class PublishNewsForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField(error_messages={"required": "请选择新闻分类"})

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
