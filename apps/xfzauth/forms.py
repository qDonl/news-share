#!/usr/bin/python3
# _*_ coding: utf-8 _*_
from django import forms
from django.core import validators
from django.core.cache import cache

from apps.form import FormMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form, FormMixin):
    # 用户登录表单
    telephone = forms.CharField(max_length=11,
                                error_messages={"required": "手机号不能为空"},
                                validators=[validators.RegexValidator(regex=r'1[345678]\d{9}', message='请输入正确格式的手机号')])
    password = forms.CharField(min_length=6, max_length=16,
                               error_messages={"required": "密码不能为空",
                                               'min_length': "密码为6-16位",
                                               'max_length': "密码为6-16位"})
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form, FormMixin):
    # 用户注册表单
    telephone = forms.CharField(max_length=11,
                                error_messages={"required": "手机号不能为空"})
    username = forms.CharField(max_length=20,
                               error_messages={"required": "请输入用户名",
                                               'max_length': "用户名最大长度为20个字符"})
    password1 = forms.CharField(min_length=6, max_length=16,
                                error_messages={"required": "密码不能为空",
                                                'min_length': "密码为6-16位",
                                                'max_length': "密码为6-16位"})
    password2 = forms.CharField(min_length=6, max_length=16,
                                error_messages={"required": "确认密码不能为空",
                                                'min_length': "密码为6-16位",
                                                'max_length': "密码为6-16位"})
    img_captcha = forms.CharField(max_length=4, min_length=4,
                                  error_messages={"required": "请输入图形验证码",
                                                  'max_length': "请输入正确的图形验证码",
                                                  'min_length': "请输入正确的图形验证码"})
    sms_captcha = forms.CharField(max_length=4, min_length=4,
                                  error_messages={"required": "请输入短信验证码",
                                                  'max_length': "请输入正确的短信验证码",
                                                  'min_length': "请输入正确的短信验证码"})

    def clean(self):
        # 验证两次密码是否输入一致
        cleaned_data = super(RegisterForm, self).clean()

        # 验证两次输入的密码
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("练此密码不一致, 请重新输入")

        # 验证手机号是否已被注册
        telephone = cleaned_data.get('telephone')
        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            raise forms.ValidationError("该手机号已被注册")

        # 验证手机验证码
        sms_captcha = cleaned_data.get('sms_captcha')
        cache_sms_captcha = cache.get(telephone)
        if not cache_sms_captcha or cache_sms_captcha.lower() != sms_captcha.lower():
            raise forms.ValidationError("手机验证码错误")

        # 验证图形验证码
        img_captcha = cleaned_data.get('img_captcha')
        cache_img_captcha = cache.get(img_captcha.lower())
        if not cache_img_captcha or cache_img_captcha.lower() != img_captcha.lower():
            raise forms.ValidationError("图形验证码错误")

        return cleaned_data
