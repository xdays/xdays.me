Title: 搭建私有pypi仓库
Date: 2016-02-25 14:34
Author: admin
Category: python
Tags: python, pypi
Slug: 搭建私有pypi仓库
 
# 背景

为了对公司内部的Python库进行统一管理，但出于隐私考虑不能直接放到公共pypi服务器上，故考虑搭建私有pypi仓库。

# 服务端

# 安装

安装pypiserver

    pip install pypiserver passlib

安装supervisor

    apt-get install supervisor

# 配置

新建package存放目录

    mkdir -p /opt/pypi/packages

创建用于上传package的密码

    htpasswd -sc /opt/pypi/.htaccess user

新建supervisor配置文件，vim /etc/supervisor/conf.d/pypi.conf

```
[program:pypi]
directory=/opt/pypi/
command=pypi-server -p 8082 -P .htaccess /opt/pypi/packages
autostart=true
autorestart=true
redirect_stderr=true
stderr_logfile=NONE
```

配置nginx， vim /etc/nginx/site-enabled/pypi.conf

```
server {
    listen 80;
    server_name pypi.example.com;
    location / {
        proxy_pass http://127.0.0.1:8082;
    }
}
```

# 客户端

## setup.py

编辑~/.pypirc添加如下配置：

```
[distutils]
index-servers: example
[example]
repository: http://pypi.example.com
username: user
password: pass
```

## pip

编辑~/.pip/pip.conf

```
[global]
trusted-host = pypi.example.com
index-url = http://pypi.example.com/simple
```
