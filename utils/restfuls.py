#!/usr/bin/python3
# _*_ coding: utf-8 _*_
from django.http import JsonResponse


class _HttpCode:
    SUCCESS = 200
    BADE_REQUEST = 400  # 1. 参数有误; 2. 发送内容服务器无法理解
    UNAUTHORIZED = 401  # 用户认证错误
    FORBIDDEN = 403  # 服务器理解请求, 但是拒绝执行
    NOT_FOUND = 404
    SERVER_ERROR = 500  # 服务器出错


def _restful(code, msg, data, **kwargs):
    json_dict = {'code': code, 'msg': msg, 'data': data}

    if kwargs and kwargs.keys():
        json_dict.update(**kwargs)
    return JsonResponse(json_dict)


def result(msg='', data=None, **kwargs):
    # 用于关键字参数的处理
    return _restful(code=_HttpCode.SUCCESS, msg=msg, data=data, **kwargs)


def success(msg='', data=None):
    return _restful(_HttpCode.SUCCESS, msg=msg, data=data)


def bad_request(msg='', data=None):
    return _restful(_HttpCode.BADE_REQUEST, msg=msg, data=data)


def unauthorized(msg='', data=None):
    return _restful(_HttpCode.UNAUTHORIZED, msg=msg, data=data)


def forbidden(msg='', data=None):
    return _restful(_HttpCode.FORBIDDEN, msg=msg, data=data)


def not_found(msg='404: 网页突然就失踪了', data=None):
    return _restful(_HttpCode.NOT_FOUND, msg=msg, data=data)


def server_error(msg='服务器出了点小毛病', data=None):
    return _restful(_HttpCode.SERVER_ERROR, msg=msg, data=data)
