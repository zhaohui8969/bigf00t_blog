# 自己的Django博客的一个备份


我的博客地址 <http://blog.bigf00t.net>

## 配置过程

### 环境准备

我自己是在Python2.7下写的这个博客

下载项目，配置Python virtualenv，并安装所需的库

```
git clone https://github.com/zhaohui8969/bigf00t_blog.git
cd bigf00t_blog
virtualenv .
source ./bin/activate
pip install -r ./requirements.txt
```

### 复制配置文件及数据库

将配置文件复制一份，并在`bigf00t_blog/bigf00t_blog/secret_key.py`中填入一个`SECRET_KEY`

```
cp bigf00t_blog/blog/blog_conf.py.example bigf00t_blog/blog/blog_conf.py
cp bigf00t_blog/bigf00t_blog/secret_key.py.example bigf00t_blog/bigf00t_blog/secret_key.py
```

### 初始化数据库

```
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
```

### 运行UWSGI测试

```
./manage.py collectstatic
uwsgi --http :8000 --wsgi-file bigf00t_blog/wsgi.py
```

这样会本地的8000响应HTTP报文，测试没有问题的话可以修改`uwsgi.ini`使用sock模式配合nginx做前端启用

```
uwsgi uwsgi.ini
```

安全起见记得修改`bigf00t_blog/settings.py`中的`DEBUG`值为`False`