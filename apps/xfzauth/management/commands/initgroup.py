#!/usr/bin/python3
# _*_ coding: utf-8 _*_

from django.contrib.auth.models import Permission, Group, ContentType
from django.core.management.base import BaseCommand

from apps.cms.models import Banner
from apps.course.models import Course, CourseCategory, Teacher
from apps.news.models import News, NewsCategory, Comment


# 使用命令创建默认分组
# 相当于 flask中的 command.add_command
class Command(BaseCommand):
    def handle(self, *args, **options):
        # 1. 编辑组 (新闻管管理/轮播图管理/课程管理)
        edit_content_type = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Comment),
            ContentType.objects.get_for_model(Banner),
        ]
        edit_permissions = Permission.objects.filter(content_type__in=edit_content_type)
        edit_group = Group.objects.create(name='编辑组')
        edit_group.permissions.set(edit_permissions)
        edit_group.save()
        self.stdout.write(self.style.SUCCESS("编辑组, 创建完成"), ending='')
        # 2. 管理员组 (课程相关管理)
        admin_content_type = [
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(Teacher),
        ]
        admin_permissions = Permission.objects.filter(content_type__in=admin_content_type).union(edit_permissions)
        admin_group = Group.objects.create(name='管理员组')
        admin_group.permissions.set(admin_permissions)
        admin_group.save()
        self.stdout.write(self.style.SUCCESS("管理员组, 创建完成"), ending='')
        # 3. 超级管理员
        self.stdout.write(self.style.SUCCESS("It's Success"), ending='')
