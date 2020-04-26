---
title: 简易vsftp搭建
date: 2010-06-06
author: admin
category: server
tags: ['server', 'vsftp']
slug: 简易vsftp搭建
---

<div id="blog_text">

一直以来都想总结一下关于 vsftp 搭建 ftp 的相关内容，今天历尽辛苦终于算是完成了一些基本的配置，在此记下以留作以后参考。

首先，讨论一下 ftp 协议的主动模式和被动模式：

下面的内容主要参考一篇洋文：<http://slacksite.com/other/ftp.html>

主动模式：

1）客户端随即开启一个大于 1024 的端口连接服务器端的 21 号端口建立连接 1，连接成功就可以下达命令。  
2）当需要传送数据时，客户端通过连接 1 告诉服务器，客户端在端口 N 上监听。  
3）服务器通过 20 号端口与端口 N 连接建立连接 2。  
4）客户端与服务器用这两个连接传送命令和数据。

被动模式：

1）客户端随即开启一个大于 1024 的端口连接服务器端的 21 号端口建立连接 1，连接成功就可以下达命令。

2）当需要传送数据时，客户端通过连接 1 告诉服务器要通过被动模式建立连接 2。  
3）服务器启动特定范围内的一个端口 S 监听并告知客户端。  
4）客户端通过大于 1024 的随进端口，连接服务器的端口 S，从而建立连接 2。  
5）客户端与服务器用这两个连接传送命令和数据。

为什么有主动没动模式之分？

问题的关键就在防火墙上，防火墙一般是阻止外部端口主动连接的。所以可以看出主动模式基本上都被客户端的防火墙做掉了，而被动连接会被服务器的防火墙解决
掉（如果不采取措施）。但是在服务器上下手总比在客户端上下手合理，它本来就是为客户端服务的嘛。所以就采用被动模式，服务器端的解决办法，就是让防火墙
允许连接向特定端口的数据包通过。

接下来把重点放在 vsftp 上，我这里搭建的一个很小的环境内的 ftp 服务器，只有基础设置的一些特别需要注意的地方，更为复杂的设置暂时用不到也就不去学习了，学以致用嘛。

组件安装？

（1）安装：＃sudo apt-get install vsftpd  
（2）软件主要组成:/etc/vsftpd.conf /usr/sbin/vsftpd  
/etc/pam.d/vsftpd   /etc/init.d/vsftpd start|stop|restart|reload}

匿名登录，支持下载上传的配置文件？

anonymous_enable=YES  
write_enable=YES  
anon_umask=022  
anon_upload_enable=YES  
anon_mkdir_write_enable=YES  
anon_other_write_enable=YES  
dirmessage_enable=YES  
xferlog_enable=YES  
connect_from_port_20=YES  
xferlog_std_format=YES  
listen=YES

pam_service_name=vsftpd  
userlist_enable=YES  
tcp_wrappers=YES

关于目录权限？

默认 vsftpd 是不允许根目录有写的权限的，所以要自己建立一个对 ftp（匿名用户的权限用户）有写的权限的目录。如下所示：

drwxr-xr-x 2 ftp ftp 4096 Apr 11 11:26 pub-writable

注意：关于配置匿名上传和下载的几个注意点：1)ftp 的匿名用户在 linux 系统内是 ftp 用户；2)匿名用户的默认 umask 是 077，这说明
如果你要上传一个目录上去，连你自己都看不到你自己上传的东西，所以必须将它改成 022；3)selinux 策略也会影响到匿名用户的上传功能（/etc/selinux/config 中把 enforcing 修改成 disabled）。总之，权
限方面的设置是一个很关键的问题，包括 selinux 规则，系统用户权限和 vsftpd 配置，必须仔细考虑才能成功。

本地用户登录配置文件？

local_enable=YES  
write_enable=YES  
local_umask=022  
dirmessage_enable=YES  
xferlog_enable=YES  
connect_from_port_20=YES  
xferlog_std_format=YES  
chroot_local_user=YES   //限制本地用户根目录  
local_root=/var/ftp/pub    //限制本地用户根目录到特定目录  
chroot_list_enable=YES  
chroot_list_file=/etc/vsftpd/chroot_list  
//这两项设置不再限制范围内的用户  
listen=YES

pam_service_name=vsftpd  
userlist_enable=YES  
tcp_wrappers=YES

注意：本地用户需要设置的很少，为了安全需要把本地用户限制在其家里或者特定目录下，chroot_list_enable,local_root,chroot_list_enable 三个设置项相当重要。

Selinux 的权限设置

发现 vsftpd 和系统权限设置均没有问题，但是无法列举目录下的内容，google 了一下有了思路，selinux 的默认权限不允许 ftp 传输，这里直接修改/etc/selinux/config 文件内容如下：

SELINUX=disabled

参考文档：<http://bbs.chinaunix.net/thread-561183-1-1.html#> （很全面）

</div>
