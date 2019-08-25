from django.shortcuts import render
from apps.news.models import News, NewsCategory
from django.conf import settings

from utils import restfuls
from .serializers import NewsSerializer


def index(request):
    categories = NewsCategory.objects.all()

    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.all().order_by('-pub_time')[0:count]
    context = {
        'categories': categories,
        'newses': newses
    }
    return render(request, 'news/index.html', context=context)


def news_list(request):
    # 通过查询字符串的方式获取当前是第几页
    p = int(request.GET.get('p', 1))
    start = (p - 1) * settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.all().order_by('-pub_time')[start:end]
    serializer = NewsSerializer(newses, many=True)
    return restfuls.success(data=serializer.data)


def news_detail(request, news_id):
    return render(request, 'news/news_detail.html')


def news_search(request):
    return render(request, 'search/search.html')
