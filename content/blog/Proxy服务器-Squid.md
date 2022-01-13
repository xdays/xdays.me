---
title: Proxy 服务器-Squid
date: 2010-07-22
author: admin
category: server
tags: ['proxy', 'server']
slug: proxy-服务器-squid
---

什么是代理服务器?

代理服务器是介于客户端和 Web 服务器之间的另一台服务器，有了它之后，浏览器不是直接到 web 服务器去取回网页而是向代理服务器发出请
求，请求会先送到代理服务器，由代理服务器来请求浏览器所需要的信息并传送给你的浏览器。大部分代理服务器都具有缓冲的功能，就好像一个大的 Cache，它有很大的存储空间，它不断将新取得数据储存到它本机的存储器上，如果浏览器所请求的数据
在它本机的存储器上已经存在而且是最新的，那么它就不重新从 Web 服务器取数据，而直接将存储器上的数据传送给用户的浏览器，这样就能显著提高浏览速度和
效率。总之：代理服务器是
Internet 链路级网关(Gateway)所提供的一种重要的安全功能，它的工作主要在开放系统互联
(OSI) 模型的对话层，从而起到防火墙的作用。

安装及其配置？

1.安装：apt-get intall squid 或者按照源码包中的 INSTALL 文件说明源码安装

2.启动停止脚本：/etc/init.d/squid start | stop | restart

3.配置文件：/etc/squd/squid.conf
此配置文件相当于一份手册，配置时可以参考，这里仅讨论基本配置项。

(1)管理配置  
http_port 192.168.0.1:3128  //监听端口  
cache_mgr  webmaster //管理员联系方式  
cache_dir ufs /var/squid   //缓存目录  
cache_mem 32MB   //缓存大小  
cache_access_log /var/squid/access.log   //访问记录，重要！

(2)访问控制  
格式为：  
acl  acl-name  type  arguement  
http_access deny | allow acl-name  
示例：  
acl  mynet ip src 10.110.12.0/24  
http_access allow mynet  
注意：

1）访问控制表的末尾要有拒绝所有的语句，否则按照 allow-deny 的规则可能会允许一些网络访问外网。

2）访问控制除了 ip 以外还有 MAC 地址，域名，域名后缀（正则表达式），时间，并发连接数，通过认证等，具体可以参考配置文件编写。

3）访问控制表采用的是或逻辑，也就是如果有一条规则匹配那么就匹配这条控制表；施加到访问控制表上的规则采用的与逻辑，也就是只有多个规则同时匹配了才执行相应的规则，否则继续匹配。

(3)认证访问

认证访问就是客户端要必须经过输入用户名和密码后验证通过后才能使用代理服务。squid 有很多验证身份的方式，大类上分为基本的，Digest 和 NTLM，这里使用 Digest 方式。其原理也比较好理解，squid 将客户端的用户名和密码（加密的）传递给辅助进程，然后辅助进程通过保存在本地的验证文件来验证客户端，如果通过验证则可以代理，否则显示拒绝信息。基本配置就是加上如下两行：

auth_param digest program /usr/lib/squid/digest_pw_auth
/path/to/authfile 定义采用什么样的认证方式，这里也指定了验证文件

auth_param digest realm Authentication Required 定义显示给客户端的信息

acl login proxy_auth REQUIRED 定义访问控制表

http_access allow login 定义匹配访问控制表的规则

监控以及排错？

监控也主要有三种方式：基本的 squidclient 与 squid 交互获得信息；squid 的 cachemgr.cgi 库；snmp（不提倡的方式）。最基本的方式执行命令如下：

squidclient mgr:info

另外 squid 的日志文件 access.log，cache.log，store.log 分别对应访问日志，缓存日志，本地存储日志，通常位于/var/log/squid/目录下。

参考链接：《Squid 中文权威指南》<http://home.arcor.de/jeffpang/squid/index.html>
