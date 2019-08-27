#!/usr/bin/python3
# _*_ coding: utf-8 _*_

from django import forms
from apps.form import FormMixin


class CommentForm(forms.Form, FormMixin):
    news_id = forms.IntegerField()
    content = forms.CharField()
