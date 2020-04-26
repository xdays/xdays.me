---
title: 搭建私有pypi仓库
date: 2016-02-25
author: admin
category: python
tags: ['python', 'pypi']
slug: 搭建私有pypi仓库
---

# 背景

为了对公司内部的 Python 库进行统一管理，但出于隐私考虑不能直接放到公共 pypi 服务器上，故考虑搭建私有 pypi 仓库。

# 服务端

# 安装

安装 pypiserver

    pip install pypiserver passlib

安装 supervisor

    apt-get install supervisor

# 配置

新建 package 存放目录

    mkdir -p /opt/pypi/packages

创建用于上传 package 的密码

    htpasswd -sc /opt/pypi/.htaccess user

新建 supervisor 配置文件，vim /etc/supervisor/conf.d/pypi.conf

```
[program:pypi]
directory=/opt/pypi/
command=pypi-server -p 8082 -P .htaccess /opt/pypi/packages
autostart=true
autorestart=true
redirect_stderr=true
stderr_logfile=NONE
```

配置 nginx， vim /etc/nginx/site-enabled/pypi.conf

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

编辑~/.pypirc 添加如下配置：

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
