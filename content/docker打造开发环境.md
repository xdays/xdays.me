Title: Docker打造开发环境
Date: 2014-04-08 14:01
Author: admin
Category: container
Tags: docker
Slug: docker打造开发环境

背景
====

我一直想要打造这样一个干净且高效的开发环境：干净指与开发隔离，不污染物理机，我已经讨厌重装系统了；高效是指自动化，我需要每次都安装一对依赖，修改一些配置文件等等繁琐的操作，而且自动化过程要快。最开始自己用virtualbox新建虚拟机然后用其自带的克隆功能复制出来；后来用vagrant配合一些配置工具能达到不错的效果，一个文件即可生成开发环境，这应该是主流了，但是这种方式有个缺点就是太慢；现在我自己用docker+supervisor摸索了一个更快的方案。

组件
====

-   supervisor，管理所有进程
-   sshd，可以登陆到container里，修改代码调试代码
-   app，实际跑的项目

具体运行流程如下： ​

    docker -startup-> 运行supervisor ->管理(sshd，项目进程)
                      -> dump出环境变量供远程ssh使用

组件配置
========

supervisor
----------

supervisor的配置关键就是要让其前台运行，具体配置如下：

    [inet_http_server]
    port=0.0.0.0:9001
    username=root
    password=thinkin
    ​
    [supervisord]
    logfile=/tmp/supervisord.log
    logfile_maxbytes=50MB
    logfile_backups=2
    loglevel=info
    pidfile=/tmp/supervisord.pid
    nodaemon=true
    minfds=1024
    minprocs=200
    umask=022

    [rpcinterface:supervisor]
    supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

    [supervisorctl]
    serverurl=http://127.0.0.1:9001
    username=root
    password=thinkin
    history_file=~/.sc_history

    [include]
    files = /etc/supervisor.d/*.conf

sshd
----

ssh不需要额外配置，主要是添加上远程登陆需要的公钥信息：

    mv ssh /root/.ssh
    chmod 700 /root/.ssh && chmod 600 /root/.ssh/*
    chown -R root.root /root/.ssh

关于sshd有两点需要说明： 1.
启动container时要加上-t参数，不然无法远程登陆 2.
由于ssh无法获取远程的环境变量，这样docker依赖环境变量的link特性就无法使用，这样django的开发环境就没法在远程ssh后正常运行了。这里我的解决办法是在container启动的时候（封装启动脚本）dump一份当前的环境变量到文件，然后sshd登陆到机器上去时source该文件，这样ssh就拥有了和本地一样的环境变量了。

app
---

这部分工作主要是编写app对应的supervisor配置文件，然后将app交由supervisor管理

Docker配置
==========

Dockerfile
----------

    FROM ubuntu:china
    MAINTAINER xdays <easedays@gmail.com>

    ADD script /tmp/script
    RUN bash /tmp/script/setup.sh

    EXPOSE 80
    EXPOSE 9001
    CMD startup

初始化脚本setup.sh
------------------

    #!/bin/sh

    apt-get update
    apt-get install -y openssh-server python-pip wget libmysqlclient18 #安装一些包和依赖库

    #sshd相关配置
    mkdir /var/run/sshd
    cd /tmp/script
    mv ssh /root/.ssh
    chmod 700 /root/.ssh && chmod 600 /root/.ssh/*
    chown -R root.root /root/.ssh

    #supervisor相关配置
    cd /tmp/script
    mv supervisord.conf /etc/supervisord.conf
    mv supervisor.d/ /etc/supervisor.d/

    #封装下启动命令，脚本内容见下文
    mv startup /usr/local/bin/

    #下载项目依赖和项目代码
    mkdir /web
    wget -SO - http://url/to/upops-deps.tgz | tar xz -C /
    wget -SO - http://url/to/upops-core.tgz | tar xz -C /web/

启动脚本
--------

    #!/bin/sh

    /usr/bin/env > /root/.env
    supervisord -c /etc/supervisord.conf

启动命令
--------

目前docker还不能支持给虚拟机绑定公网地址，所以所有端口还需要通过docker的端口映射来实现：

    docker run -t -d -p 80:80 -p 2022:22 --link mysql:db -v /web/:/web/ upops
