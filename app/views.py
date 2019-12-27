from django.shortcuts import render, HttpResponse, redirect
from django.template import loader


# Create your views here.

def index(request):
    template = loader.get_template("index.html")
    response = HttpResponse(template.render())
    # 设置不加密的cookie
    response.set_cookie('username', "username_value")
    # 设置加密的cookie
    response.set_signed_cookie('password', "password_value", salt="long")
    return response


def read(request):
    # 获取不加密的cookie
    username = request.COOKIES.get("username")
    # 获取加密的cookie,注意：获取加密的cookie时要记得带上设置cookie时盐。
    # 比如我在设置的时候加的盐是long,在获取时得带上long才行。
    password = request.get_signed_cookie("password", salt="long")
    return HttpResponse("不加密的cookie:%s==加密的cookie:%s" % (username, password))


def reada(request):
    # 获取不加密的cookie
    username = request.COOKIES.get("username")
    # 获取加密的cookie,注意：获取加密的cookie时要记得带上设置cookie时盐。
    # 比如我在设置的时候加的盐是long,在获取时得带上long才行。
    return HttpResponse("不加密的cookie:%s" % (username))


def delete(request):
    response = HttpResponse('清除成功')
    response.delete_cookie('username')
    response.delete_cookie('password')
    return response


def add_session(request):
    request.session['session_username'] = 'amdin'
    # 上面这一句代码完成了以下事情：
    # 1、生成随机字符串
    # 2、将随机字符串写到用户浏览器cookie
    # 3、将随机字符串保存到服务器session
    # 4、在服务器随机字符串对应的字典中设置相关内容
    request.session['session_password'] = '123456789'
    return HttpResponse('设置session')


def read_session(request):
    username = request.session.get('session_username')  # 没有获取到就返回None
    # password = request.session.get('session_password')
    # 下面这种获取session时，如果没有取到就会报错
    # username = request.session['session_username']
    return HttpResponse(username)


def del_session(request):
    # request.session.flush()  # 删除所有session
    # 删除key为session_username的session,如果没有该session的话就会报错
    del request.session['session_username']
    return HttpResponse('清除session成功')
