## cookie的使用
### 设置cookie
```python
from django.shortcuts import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template("index.html")
    response = HttpResponse(template.render())
    # 设置不加密的cookie
    response.set_cookie('username',"username")
    # 设置加密的cookie,这个是加了盐(long)
    response.set_signed_cookie('password', "password",salt="long")
    return response
```
### 获取cookie
```python
from django.shortcuts import HttpResponse

def read(request):
    # 获取不加密的cookie
    username = request.COOKIES.get("username")
    # 获取加密的cookie,注意：获取加密的cookie时要记得带上设置cookie时盐。
    # 比如我在设置的时候加的盐是long,在获取时得带上long才行。
    password = request.get_signed_cookie("password",salt="long")
    return HttpResponse("不加密的cookie:%s==加密的cookie:%s"%(username,password))
```

如果在获取加密时没有带上盐出现如下错误：
![](https://user-gold-cdn.xitu.io/2019/12/27/16f456fa169c1bf5?w=739&h=101&f=png&s=11830)

### 删除cookie
```python
from django.shortcuts import HttpResponse

def delete(request):
    response = HttpResponse('清除cookie成功')
    response.delete_cookie('username')
    response.delete_cookie('password')
    return response
```
**注意**:
- 在删除cookie时，如果是加密的cookie的话,如果你再次想获取这个加密的cookie的话会报错，比如说：`delete`方法中删除了加密的password这个cookie，当我再次想获取这个加密的cookie时出现：
![](https://user-gold-cdn.xitu.io/2019/12/27/16f4577783d0bdfd?w=849&h=96&f=png&s=6569)

- 获取不加密的cookie就不会有影响。(没有值就返回None)

<span style="color:red;font-size:20px;">如果不设置cookie过期时间的话,系统会默认关闭浏览器就失效（过期）</span>


## session的使用
- 在django中，session的默认过期时间是两周
- 在django中，session默认是存储在数据库中的。

### 设置session
```python
from django.shortcuts import HttpResponse

def add_session(request):
    request.session['session_username'] = 'amdin'
    # 上面这一句代码完成了以下事情：
    # 1、生成随机字符串
    # 2、将随机字符串写到用户浏览器cookie
    # 3、将随机字符串保存到服务器session
    # 4、在服务器随机字符串对应的字典中设置相关内容
    request.session['session_password'] = '123456789'
    return HttpResponse('设置session')
```

#### 如果出现报错如下：
![](https://user-gold-cdn.xitu.io/2019/12/27/16f4583eb7ca808e?w=651&h=91&f=png&s=8977)
上面截图的报错是因为在使用session时没有生成迁移文件和创建数据表造成的。
解决办法:
```
python manage.py makemigrations
```
```
python manage.py migrate
```

### 获取session
```python
from django.shortcuts import HttpResponse

def read_session(request):
    username = request.session.get('session_username') # 没有获取到就返回None
    # password = request.session.get('session_password')
    # 下面这种获取session时，如果没有取到就会报错
    # username = request.session['session_username']
    return HttpResponse(username)
```


### 删除session
```python
from django.shortcuts import HttpResponse

def del_session(request):
    # request.session.flush()  # 删除所有session
    # 删除key为session_username的session,如果没有该session的话就会报错
    del request.session['session_username']
    return HttpResponse('清除session成功')
```

## 修改session缓存方式
session中的默认缓存方式是数据库缓存:
```python
# 默认是数据库缓存（引擎默认）
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
```

下面我们设置成文件缓存
### 修改settings.py文件
```python
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
# SESSION_FILE_PATH = None # 缓存文件路径，如果为None，则使用tempfile模块获取一个临时地址tempfile.gettempdir()
SESSION_FILE_PATH = os.path.join(BASE_DIR, 'templates') # 设置session保存在templates下
```

**文件缓存加上数据库**
```python
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
```

还有另外一种缓存是redis或memcache
```python
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # 引擎
# 使用的缓存别名（默认内存缓存，也可以是memcache），此处别名依赖缓存的设置
SESSION_CACHE_ALIAS = 'default'
```

**通用配置**
```python
# 配置文件中设置默认操作（通用配置）：
SESSION_COOKIE_NAME = "sessionid"   # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串（默认）
SESSION_COOKIE_PATH = "/"           # Session的cookie保存的路径（默认）
SESSION_COOKIE_DOMAIN = None        # Session的cookie保存的域名（默认）
SESSION_COOKIE_SECURE = False       # 是否Https传输cookie（默认）
SESSION_COOKIE_HTTPONLY = True      # 是否Session的cookie只支持http传输（默认）
SESSION_COOKIE_AGE = 1209600        # Session的cookie失效日期（2周）（默认）
SESSION_EXPIRE_AT_BROWSER_CLOSE = False     # 是否关闭浏览器使得Session过期（默认）
SESSION_SAVE_EVERY_REQUEST = False          # 是否每次请求都保存Session，默认修改之后才保存（默认）
```

[gitHub地扯](https://github.com/yu258/django-cookie-and-session)