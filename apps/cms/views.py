import os
from datetime import datetime
from urllib import parse

import qiniu
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import make_aware
from django.views.decorators.http import require_POST, require_GET
from django.views.generic.base import View

from apps.cms.forms import PublishNewsForm
from apps.course.models import Course, CourseCategory, Teacher
from apps.news.models import NewsCategory, News
from utils import restfuls
from .forms import (
    EditNewsCategoryForm,
    AddBannerForm,
    EditBannerForm,
    PublishCourseForm
)
from .models import Banner
from .serializers import BannerSerializer


@staff_member_required(login_url='index')
def index(request):
    return render(request, 'cms/index.html')


class PublishNewsView(View):
    """发布/编辑新闻"""

    def get(self, request):
        categories = NewsCategory.objects.all()
        context = {
            "categories": categories
        }
        return render(request, 'cms/publish_news.html', context=context)

    def post(self, request):
        form = PublishNewsForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            cid = form.cleaned_data.get('category')
            category = NewsCategory.objects.get(pk=cid)

            news_id = form.cleaned_data.get('news_id') or None
            News.objects.update_or_create(id=news_id, defaults={
                "title": title,
                "desc": desc,
                "thumbnail": thumbnail,
                "content": content,
                "category": category,
                "author": request.user
            })
            return restfuls.success()
        return restfuls.bad_request(msg=form.get_errors())


@require_GET
def news_category(request):
    categories = NewsCategory.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, 'cms/news_category.html', context=context)


@require_POST
def add_news_category(request):
    name = request.POST.get('name')
    exists = NewsCategory.objects.filter(name=name).exists()
    if not exists:
        NewsCategory.objects.create(name=name)
        return restfuls.success(msg="添加成功")
    return restfuls.bad_request(msg="该分类已经存在")


@require_POST
def edit_news_category(request):
    form = EditNewsCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            NewsCategory.objects.filter(pk=pk).update(name=name)
            return restfuls.success()
        except ValueError:
            return restfuls.bad_request(msg="该分类已不存在")
    return restfuls.bad_request(form.get_errors())


@require_POST
def delete_category_category(request):
    pk = request.POST.get("pk")
    if pk:
        NewsCategory.objects.filter(pk=pk).delete()
        return restfuls.success()
    return restfuls.bad_request(msg="当前分类已不存在")


class NewsListView(View):
    # 新闻列表
    def get(self, request):
        p = request.GET.get("p", 1)  # 获取当前是第几页
        start_time = request.GET.get('start', '')
        end_time = request.GET.get('end', '')
        title = request.GET.get("title", '')
        category_id = int(request.GET.get("category", 0))

        categories = NewsCategory.objects.all()
        newses = News.objects.select_related('author', 'category')

        # 按照新闻时间进行过滤
        if start_time or end_time:
            start_time = start_time[:10]
            end_time = end_time[:10]
            if start_time:
                try:
                    start_time = datetime.strptime(start_time, '%Y/%m/%d')
                except ValueError:
                    start_time = datetime.strptime(start_time, '%Y-%m-%d')
            else:
                start_time = datetime(year=2019, month=6, day=1)

            if end_time:
                try:
                    end_time = datetime.strptime(end_time, '%Y/%m/%d')
                except ValueError:
                    end_time = datetime.strptime(end_time, '%Y-%m-%d')
            else:
                end_time = datetime.today()
            newses = newses.filter(pub_time__range=(make_aware(start_time), make_aware(end_time)))

        # 按照标题进行过滤
        if title:
            newses = newses.filter(title__icontains=title)

        # 按照分类进行过滤
        if category_id != 0:
            newses = newses.filter(category=category_id)

        paginator = Paginator(newses, 6)  # 每页显示多少条数据
        page_obj = paginator.get_page(p)
        rt_pages = self.get_paginator_page(paginator, page_obj)
        context = {
            'newses': page_obj.object_list,
            "categories": categories,
            'url_query': "&" + parse.urlencode({
                'start': start_time,
                'end': end_time,
                'title': title,
                'category': category_id or 0,
            }),
            'start': start_time,
            'end': end_time,
            'title': title,
            'category_id': category_id or 0,
        }
        context.update(**rt_pages)
        return render(request, 'cms/news_list.html', context=context)

    def get_paginator_page(self, paginator, page_obj, around_num=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        # current_page=around_num+2时, (1, current_page)
        if current_page <= around_num + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_num, current_page)  # 左列表页

        # current_page=num_page-around_num-1时就要(current_page, num_pages)
        if current_page >= num_pages - around_num - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_num + 1)  # 右列表页

        rt_pages = {
            'current_page': current_page,
            "left_pages": left_pages,
            'right_pages': right_pages,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            "num_pages": num_pages,
            "page_obj": page_obj,
            'paginator': paginator,
        }
        return rt_pages


def edit_news(request):
    news_id = request.GET.get("news")
    try:
        news = News.objects.get(pk=news_id)
    except News.DoesNotExist:
        return restfuls.bad_request(msg="该新闻已不存在")
    categories = NewsCategory.objects.all()
    context = {
        "news": news,
        'categories': categories,
    }
    return render(request, 'cms/publish_news.html', context=context)


@require_POST
def remove_news(request):
    news_id = request.POST.get('news')
    try:
        News.objects.get(pk=news_id).delete()
        return restfuls.success()
    except News.DoesNotExist:
        return restfuls.bad_request(msg="该新闻已不存在")


# 轮播图管理
def banner(request):
    # 管理轮播图
    return render(request, 'cms/banner.html')


def load_banner(request):
    # ajax 加载轮播图
    banners = Banner.objects.all()
    serializer = BannerSerializer(banners, many=True)
    return restfuls.success(data=serializer.data)


@require_POST
def add_banner(request):
    # 添加轮播图
    form = AddBannerForm(request.POST)
    if form.is_valid():
        priority = form.cleaned_data.get('priority')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        banner = Banner.objects.create(priority=priority, image_url=image_url, link_to=link_to)
        return restfuls.success(data={"banner_id": banner.pk})
    return restfuls.bad_request(form.get_errors())


@require_POST
def edit_banner(request):
    # 修改轮播图
    form = EditBannerForm(request.POST)
    if form.is_valid():
        banner_id = form.cleaned_data.get('pk')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        priority = form.cleaned_data.get('priority')
        try:
            Banner.objects.filter(pk=banner_id).update(image_url=image_url,
                                                       link_to=link_to,
                                                       priority=priority)
            return restfuls.success()
        except Banner.DoesNotExist:
            return restfuls.bad_request(msg="当前轮播图已不存在")
    return restfuls.bad_request(msg=form.get_errors())


def remove_banner(request):
    bid = request.GET.get('bid')
    banner = get_object_or_404(Banner, pk=bid)
    banner.delete()
    return restfuls.success()


# 课程管理
class PublishCourseView(View):
    def get(self, request):
        categories = CourseCategory.objects.all()
        teachers = Teacher.objects.all()
        context = {
            "categories": categories,
            "teachers": teachers
        }
        return render(request, 'cms/publish_course.html', context)

    def post(self, request):
        form = PublishCourseForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data.get("name")
            # category_id = form.cleaned_data.get("category_id")
            # teacher_id = form.cleaned_data.get("teacher_id")
            # video_link = form.cleaned_data.get("video_link")
            # cover_link = form.cleaned_data.get("cover_link")
            # price = form.cleaned_data.get("price")
            # duration = form.cleaned_data.get("duration")
            #
            # Course.objects.create(name=name, category_id=category_id,
            #                       teacher_id=teacher_id, video_link=video_link,
            #                       cover_link=cover_link, price=price,
            #                       duration=duration)
            for k, v in form.cleaned_data.items():
                print(f"{k}: {v}")
            course = Course()
            course.set_attr(form.cleaned_data)
            course.save()
            return restfuls.success()
        return restfuls.bad_request(form.get_errors())


def qntoken(request):
    # 获取七牛云 token
    access_key = settings.QINIU_ACCESS_KEY
    secret_key = settings.QINIU_SECRET_KEY
    q = qiniu.Auth(access_key, secret_key)

    bucket = settings.QINIU_BUCKET
    token = q.upload_token(bucket)
    return restfuls.result(token=token)


@require_POST
def upload_file(request):
    # 上传文件到本地
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL + name)
    return restfuls.success(data={'url': url})
