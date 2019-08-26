from django.shortcuts import render
from apps.news.models import News, NewsCategory
from django.conf import settings
from django.http import Http404

from utils import restfuls
from .serializers import NewsSerializer


def index(request):
    # 首页新闻列表信息
    categories = NewsCategory.objects.all()

    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.prefetch_related('category', 'author').all()[0:count]
    context = {
        'categories': categories,
        'newses': newses
    }
    return render(request, 'news/index.html', context=context)


def news_list(request):
    # 通过查询字符串的方式获取当前是第几页
    page = int(request.GET.get('p', 1))
    start = (page - 1) * settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT

    # 获取新闻分类, 默认0为, 新闻内容倒叙排序"最新咨询"
    category_id = int(request.GET.get("category_id", 0))

    if category_id == 0:
        newses = News.objects.prefetch_related('author', 'category').all()[start:end]
    else:
        newses = News.objects.prefetch_related('category', 'author').filter(category=category_id)[start:end]

    serializer = NewsSerializer(newses, many=True)
    return restfuls.success(data=serializer.data)


def news_detail(request, news_id):
    # 新闻详情
    try:
        news = News.objects.prefetch_related('category', 'author').get(pk=news_id)
        context = {
            'news': news
        }
        return render(request, 'news/news_detail.html', context=context)
    except:
        raise Http404


def news_search(request):
    return render(request, 'search/search.html')
