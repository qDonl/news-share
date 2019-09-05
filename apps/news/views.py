from django.conf import settings
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render

from apps.cms.models import Banner
from apps.news.models import News, NewsCategory
from apps.xfzauth.decorators import auth_login_required
from utils import restfuls
from .forms import CommentForm
from .models import Comment
from .serializers import NewsSerializer, CommentSerializer


def index(request):
    # 首页新闻列表信息
    categories = NewsCategory.objects.all()

    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.prefetch_related('category', 'author').all()[0:count]

    banners = Banner.objects.all()
    context = {
        'categories': categories,
        'newses': newses,
        'banners': banners,
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
        news = News.objects.select_related('category', 'author').get(pk=news_id)
        # 在后台查询数据库 comment, 相对于 news.comments 将会执行更少的sql查询
        # 只展示最新的10条新闻
        comments = Comment.objects.select_related('author').filter(news_id=news_id)[:10]
        context = {
            'news': news,
            'comments': comments,
        }
        return render(request, 'news/news_detail.html', context=context)
    except News.DoesNotExist:
        raise Http404


@auth_login_required
def publish_comment(request):
    # 发布评论
    form = CommentForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get('news_id')
        content = form.cleaned_data.get("content")
        comment = Comment.objects.create(news_id=news_id, content=content, author=request.user)
        serializer = CommentSerializer(comment)
        return restfuls.success(data=serializer.data)
    return restfuls.bad_request(msg=form.get_errors())


def news_search(request):
    q = request.GET.get("q")
    context = {}
    if q:
        newses = News.objects.select_related('category', 'author') \
            .filter(Q(title__icontains=q) | Q(content__icontains=q))
        context = {
            "q": q,
            'newses': newses
        }
    return render(request, 'search/search.html', context)
