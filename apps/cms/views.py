import os

import qiniu
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.views.generic.base import View

from apps.cms.forms import PublishNewsForm
from apps.news.models import NewsCategory, News
from utils import restfuls
from .forms import EditNewsCategoryForm, AddBannerForm, EditBannerForm
from .models import Banner
from .serializers import BannerSerializer


@staff_member_required(login_url='index')
def index(request):
    return render(request, 'cms/index.html')


class PublishNewsView(View):
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
            News.objects.create(title=title, desc=desc, thumbnail=thumbnail,
                                content=content, category=category,
                                author=request.user)
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


@require_POST
def upload_file(request):
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL + name)
    return restfuls.success(data={'url': url})


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


def qntoken(request):
    access_key = settings.QINIU_ACCESS_KEY
    secret_key = settings.QINIU_SECRET_KEY
    q = qiniu.Auth(access_key, secret_key)

    bucket = settings.QINIU_BUCKET
    token = q.upload_token(bucket)
    return restfuls.result(token=token)
