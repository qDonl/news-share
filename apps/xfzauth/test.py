#!/usr/bin/python3
# _*_ coding: utf-8 _*_
from django.contrib.auth.models import Group
from .models import User
from django.http import HttpResponse


def test_index(request):
    u = User.objects.get(telephone='17778889999')
    u.groups.remove(*list(u.groups.all()))
    u.save()
    return HttpResponse("test")