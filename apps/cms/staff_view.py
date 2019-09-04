#!/usr/bin/python3
# _*_ coding: utf-8 _*_
from django.contrib.auth import get_user_model
from django.shortcuts import render
from utils import restfuls
from django.views import View
from django.contrib.auth.models import Group
from apps.xfzauth.models import User
from django.http import HttpResponse
from .forms import AddStaffForm


def staff_operate(request):
    staffs = get_user_model().objects.filter(is_staff=True)
    context = {
        "staffs": staffs
    }
    return render(request, 'cms/staff_operate.html', context)


class AddStaffView(View):
    def get(self, request):
        groups = Group.objects.all()
        context = {
            'groups': groups,
        }
        return render(request, 'cms/add_staff.html', context)

    def post(self, request):
        form = AddStaffForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            groups = form.cleaned_data.get("group")
            return restfuls.success()
        return restfuls.bad_request(msg=form.get_errors())


def remove_staff(request):
    return restfuls.success()


def update_staff(request):
    return restfuls.success()
