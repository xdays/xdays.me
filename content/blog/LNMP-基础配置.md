---
title: LNMP 基础配置
date: 2010-11-28
author: admin
category: server
tags: ['lnmp', 'server']
slug: lnmp-基础配置
---

注：本文知识搭建了基本环境，仅供测试用，具体详细的安装配置见参考链接。

# 简介

lnmp 是 linux+nginx+mysql+{php |
python}的缩写，是堪比 lamp 的另一种 web 服务器平台。nginx 相比 apache 的优点有：小巧，速度快，占用内存小。据介绍 nginx 和 apache 的工作方式的类比如下：你要去大学宿舍找个同学，nginx 阿姨那里有个名单她只告诉你你同学在那个房间，而 apache 阿姨要带着你去找你那个同学，效率高低显而易见。

# 安装

一开始我已经强调这只是一个搭建一个测试环境，所以我用 debian 系统的 apt 系统自动安装所需要的程序。安装过程很简单，但是让 nginx 和 php5-cgi 协同起来工作花了我两天时间。

安装命令：  
apt-get install nginx php5-cgi mysql-server

下图所示整个环境的运作:

[![nginx-fastcgi](/wp-content/uploads/2010/11/nginx-fastcgi.jpg 'nginx-fastcgi')](/wp-content/uploads/2010/11/nginx-fastcgi.jpg)

后端的 PHP 程序根据用户请求来读写 mysql 数据库，配置的过程一个主要任务是连接 nginx 和 php5-cgi。这里我碰到了两个问题如下：

- nginx 和 fastcgi 无法连接？在 nginx 的默认站点配置文件中要指定一个 fastcgi 变量 SCRIPT_FILENAME，这个变量的值是“网站的根目录\$fastcgi_script_name”这样才能传递正确的需要解析的 php 脚本给 fastcgi，进而让 PHP 解析。
- 总是无法自动执行目录下的 index.php 文件，这个问题需要在 location 块里的 index 指令后添加 index.php，这样才能识别默认的 index.php 文件。

# 配置

## 配置 nginx.conf

关于 nginx 的配置目前还真没有太系统的资料可参考，前几天在百度文库中发现了《nginx
http
server》，粗略的看了一下算是比较系统详尽的文档了。下面还是简单的说一下我对 nginx 配置文件的理解，配置文件是由一系列的按照一定结构组织的指令组成的，这种结构叫块（block），主要的块包括 event，http，server 和 location 他们分别控制着不同的方面，event 控制与连接相关，http 控制与 http 协议相关以及日志相关等。

[![nginx-config](/wp-content/uploads/2010/11/nginx.jpg 'nginx-config')](/wp-content/uploads/2010/11/nginx.jpg)

还有一个比较重要的指令是 include，它可以把其他文件的内容包含进来，由这些文件共同组成整个配置文件，debian 对配置文件的组织就很好，条理清晰。下面就对 apt 安装的 nginx 的配置文件简单介绍，更详尽的指令用法参考《nginx
http server》（见参考链接）

xdays:\~\# cat /etc/nginx/nginx.conf

    user www-data; #用来处理请求进程的执行者
    worker_processes 1; #处理请求的进程数
    error_log /var/log/nginx/error.log; #错误日志文件位置
    pid /var/run/nginx.pid; #进程号文件位置
    events {
        worker_connections 1024; #最大连接数
    }
    http {
        include /etc/nginx/mime.types; #后缀与类型对应关系
        default_type application/octet-stream; #默认类型
        access_log /var/log/nginx/access.log; #访问日志记录位置
        sendfile on; #sendfile系统调用
        #tcp_nopush on;
        #keepalive_timeout 0;
        keepalive_timeout 65; #连接失效时间
        tcp_nodelay on; #开启socket选项
        gzip on; #压缩
        #include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*; #包含对应目录下所有文件，注意这的通配符*
    }

再者就是 sites-available 目录下的文件，每个 server 块都是一个虚拟机，可以为其制定不同的域名，像 apache 一样。默认的 default 文件接下来讨论。

下面是采用 apt 安装的/etc/nginx/sites-available/default 文件：

    server {
        listen 80; #监听端口
        server_name localhost; #主机名
        access_log /var/log/nginx/localhost.access.log; #访问日志位置
        location / {  #定义一个虚拟目录
        root /var/www/; #指定对应这个目录的实际文件系统目录
        index index.html index.htm index.php; #指定自动查找的文件，这里需要注意要添加index.php！
    }
    location /doc {
        root /usr/share;
        autoindex on; #自动索引
        allow 127.0.0.1; #访问权限
        deny all;
    }
    location ~ .php$ {
    fastcgi_pass 127.0.0.1:9000; #将对应的请求传送给fastcgi
    fastcgi_index index.php; #指定fastcgi的自动查找文件
    fastcgi_param SCRIPT_FILENAME /var/www/$fastcgi_script_name; #定义发送给fastcgi的环境变量，**脚本名**，这里需要特别注意！
    #fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name; #这样更通用
    include fastcgi_params; #包含fastcgi_params文件，主要就是写环境变量
    }

# 启动

下面启动依次启动 mysql，php5-cgi 和 nginx

    /etc/init.d/mysql start;
    php5-cgi -q -b 127.0.0.1:9000 &; #也有人把php5-cgi写成init脚本形式的，可以google下。
    /etc/init.d/nginx start;

这样基本的环境就是完成了。

# 关于 php-fpm

我没有研究过这个东西，但是从目前（201307）的环境搭建来看这个东西已经成为主流，我的理解比较浅显：php-fpm 将 php 进行 daemon 化了。

安装命令如下：  
apt-get install php5-fpm

其他与 nginx 连接的注意点大同小异。

# 参考链接

- [目前发现的最详尽的源码架设 lnmp 的教程《Nginx 0.8.x + PHP
  5.2.13（FastCGI）搭建胜过 Apache 十倍的 Web 服务器》‍](http://blog.s135.com/nginx_php_v6/)
- [针对 debian 环境的教程《‍‍‍
  Debian+Nginx+PHP(FastCGI)+MySQL 搭建 LNMP 服务器》‍](http://iambin.blogbus.com/logs/62584905.html)
- [nginx 的官方 wiki](http://wiki.nginx.org/Chs)
- [《nginx http
  server》](http://wenku.baidu.com/view/1106f46427d3240c8447ef71.html)
- [方便的集成的 lnmp 一键安装包](http://lnmp.org/)
