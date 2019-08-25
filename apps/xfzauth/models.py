#!/usr/bin/python3
# _*_ coding: utf-8 _*_
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager)
from django.db import models
from shortuuidfield import ShortUUIDField


class UserManager(BaseUserManager):
    """自定义用户模型中的 objects """

    def _create_user(self, username, telephone, password, **extra_fields):
        if not username:
            raise ValueError("请传入用户名")
        if not telephone:
            raise ValueError("请传入手机号码")
        if not password:
            raise ValueError("请传入密码")
        user = self.model(username=username, telephone=telephone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, telephone, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, telephone, password, **extra_fields)

    def create_superuser(self, username, telephone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("超级用户必须设置 `is_staff=True`")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('超级用户必须设置 `is_superuser=True`')

        return self._create_user(username, telephone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """用户数据模型"""
    uid = ShortUUIDField(primary_key=True)
    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True, null=True, blank=True)
    telephone = models.CharField(max_length=11, unique=True)
    date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
