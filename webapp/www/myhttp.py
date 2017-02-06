#!/usr/bin/env python3
# coding:utf-8

import asyncio
import functools
import logging;logging.basicConfig(level=logging.INFO)
import inspect
import os
from aiohttp import web
from myerror import APIError


# 定义url处理函数，添加请求方式标记;按RESTFULL规定，有四种请求GET,POST,PUT,DELETE
def re_method(path, *, method):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = method
        wrapper.__route__ = path
        return wrapper
    return decorator

get = functools.partial(re_method, method='GET')
post = functools.partial(re_method, method='POST')
put = functools.partial(re_method, method='PUT')
delete = functools.partial(re_method, method='DELETE')

def get_required_kw_args(fn):
    '检测参数是否都为合法的关键字参数，且无默认值；返回合法的关键字参数'
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            args.append(name)
    return tuple(args)

def get_named_kw_args(fn):
    '检查参数是否为关键字参数'
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            return True

def has_var_kw_arg(fn):
    '检查参数是否为可变关键字参数；是反为True'
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True

def has_request_arg(fn):
    sig = inspect.signature(fn)
    params = sig.parameters
    found = False
    for name, param in params.items():
        if name == 'request':
            found = True
            continue
        if found and (param.kind != inspect.Parameter.VAR_POSITIONAL and
                      param.kind != inspect.Parameter.KEYWORD_ONLY and
                      param.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError('request parameter must be the last named paremeter \
                             in function: %s%s' % (fn.__name__, str(sig)))
    return found

# RequestHandler目的就是从URL函数中分析其需要接收的参数，从request中获取必要的参数，
# URL函数不一定是一个coroutine，因此我们用RequestHandler()来封装一个URL处理函数。
# 调用URL函数，然后把结果转换为web.Response对象，这样，就完全符合aiohttp框架的要求：
class RequestHandler(object):
    '''
    RequestHandler：为view到controller的桥梁；处理request的参数和数据并解析为controller的参数
        获取Controller（路由）所需的参数列表
        把 request（请求）携带的数据解析成Controller（路由）的参数
        检查解析的参数是否正确
        最后把参数传送给Controller（路由）
    '''
    def __init__(self, app, fn):
        self._app = app
        self._func = asyncio.coroutine(fn)
        self._has_request_arg = has_request_arg(fn)
        self._has_var_kw_arg = has_var_kw_arg(fn)
        self._has_named_kw_args = has_named_kw_args(fn)
        self._required_kw_args = get_required_kw_args(fn)

    async def __call__(self, request):
        required_args = inspect.signature(self._fn).parameters
        logging.info('required args: %s' % required_args)
        kw = {arg: value for arg, value in request.__data__.items() if arg in required_args}
        # get match_info from request, such as '/blog/{id}'
        kw.update(request.match_info)
        # if has request then add it
        if 'request' in required_args:
            kw['request'] = request

        for key, arg in required_args.items():
            # request参数不能为可变长参数
            if key == 'request' and arg.kind in (inspect.Parameter.VAR_POSITIONAL,
                                                 inspect.Parameter.VAR_KEYWORD):
                return web.HTTPBadRequest(text='request parameter is invalid.')
            if arg.kind not in (inspect.Parameter.VAR_POSITIONAL,
                                inspect.Parameter.VAR_KEYWORD):
                if arg.default == inspect.Paramter.empty and arg.name not in kw:
                    return web.HTTPBadRequest(text='Missing argument: %s' % arg.name)
        logging.info('call with args: %s' % kw)
        try:
            return await self._fn(**kw)
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)

def add_static(app):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app.router.add_static('/static', path)
    logging.info('add static %s => %s' % ('static', path))

def add_route(app, fn):
    method = getattr(fn, '__method__', None)
    path = getattr(fn, '__route__', None)
    if path is None or method is None:
        raise ValueError('@get or @post not defined in %s' % str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    logging.info('add route %s %s => %s(%s)' % (method, path, fn.__name__,
                    ', '.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method, path, RequestHandler(app, fn))

def add_routes(app, module_name):
    n = module_name.rfind('.')
    if n == (-1):
        mod = __import__(module_name, globals(), locals())
    else:
        name = module_name[n+1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    # 遍历mod的方法和属性，主要是找处理方法
    # 方法需要经过@get或@post修饰
    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)
        if callable(fn):
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                logging.info('add route %s %s => %s(%s)' % (method, path, fn.__name__,
                                ', '.join(inspect.signature(fn).parameters.keys())))
                app.router.add_route(method, path, RequestHandler(app, fn))

# 添加middleware, jinja2模块和自注册支持
'''
response_factory: 将controller处理的结果转化成标准的HTTP请求的工厂函数;为controller到
    views之间的桥梁；
'''
'''
app = web.Application(loop=loop, middlewares=[
    logger_factory, response_factory
])
init_jinja2(app, filters=dict(datetime=datetime_filter))
add_routes(app, 'handlers')
add_static(app)
'''
