#!/usr/bin/python3
# _*_ coding: utf-8 _*_
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.views import View

from apps.xfzauth.models import User
from utils import restfuls
from .forms import AddStaffForm
from apps.xfzauth.decorators import auth_superuser_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.urls import reverse


@auth_superuser_required
def staff_operate(request):
    staffs = get_user_model().objects.filter(is_staff=True)
    context = {
        "staffs": staffs
    }
    return render(request, 'cms/staff_operate.html', context)


@method_decorator(auth_superuser_required, name='dispatch')
class AddStaffView(View):
    def get(self, request):
        groups = Group.objects.all()
        context = {
            'groups': groups,
        }
        return render(request, 'cms/add_staff.html', context)

    def post(self, request):
        group_ids = request.POST.getlist('group[]', [])
        if group_ids is None:
            return restfuls.bad_request('请选择员工分组')

        form = AddStaffForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            try:
                user = User.objects.get(telephone=telephone)
                user.is_staff = True
                groups = Group.objects.filter(pk__in=group_ids)
                user.groups.set(groups)
                user.save()
                return restfuls.success()
            except User.DoesNotExist:
                # messages.error(request, '请用户先完成注册')
                # return redirect(reverse('cms:staff-add'))
                return restfuls.bad_request("请用户先完成注册")
        # messages.error(request, message=form.get_errors())
        # return redirect(reverse('cms:staff-add'))
        return restfuls.bad_request(form.get_errors())


def remove_staff(request):
    return restfuls.success()


def update_staff(request):
    return restfuls.success()
