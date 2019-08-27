#!/usr/bin/python3
# _*_ coding: utf-8 _*_

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("uid", 'username', 'is_active', 'is_staff')
