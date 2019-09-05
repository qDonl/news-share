from datetime import datetime

from django import template
from django.utils.timezone import now as now_func

register = template.Library()


@register.filter('time_since')
def time_since(value):
    if not isinstance(value, datetime):
        return value
    now = now_func()
    timestamp = (now - value).total_seconds()

    if 0 < timestamp <= 60:
        return "刚刚"
    elif 60 < timestamp <= 60 * 60:
        since = timestamp // 60
        return f"{int(since)}分钟前"
    elif (60 * 60) < timestamp <= (60 * 60 * 24):
        since = timestamp // (60 * 60)
        return f"{int(since)}小时前"
    elif (60 * 60 * 24) < timestamp <= (60 * 60 * 24 * 30):
        since = timestamp // (60 * 60 * 24)
        return f"{int(since)}天前"
    else:
        return value.strftime("%Y-%m-%d %H:%M")


@register.filter('dict_or_str')
def dict_or_str(value):
    print(type(value), value)
    if isinstance(value, dict):
        for k, v in value.items():
            return v[0]
    else:
        return value
