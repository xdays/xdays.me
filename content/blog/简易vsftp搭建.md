---
title: 简易vsftp搭建
date: 2010-06-06
author: admin
category: server
tags: server, vsftp
slug: 简易vsftp搭建
---

<div id="blog_text">

一直以来都想总结一下关于vsftp搭建ftp的相关内容，今天历尽辛苦终于算是完成了一些基本的配置，在此记下以留作以后参考。

首先，讨论一下ftp协议的主动模式和被动模式：

下面的内容主要参考一篇洋文：<http://slacksite.com/other/ftp.html>

主动模式：  

1）客户端随即开启一个大于1024的端口连接服务器端的21号端口建立连接1，连接成功就可以下达命令。  
2）当需要传送数据时，客户端通过连接1告诉服务器，客户端在端口N上监听。  
3）服务器通过20号端口与端口N连接建立连接2。  
4）客户端与服务器用这两个连接传送命令和数据。

被动模式：  

1）客户端随即开启一个大于1024的端口连接服务器端的21号端口建立连接1，连接成功就可以下达命令。  

2）当需要传送数据时，客户端通过连接1告诉服务器要通过被动模式建立连接2。  
3）服务器启动特定范围内的一个端口S监听并告知客户端。  
4）客户端通过大于1024的随进端口，连接服务器的端口S，从而建立连接2。  
5）客户端与服务器用这两个连接传送命令和数据。

为什么有主动没动模式之分？

问题的关键就在防火墙上，防火墙一般是阻止外部端口主动连接的。所以可以看出主动模式基本上都被客户端的防火墙做掉了，而被动连接会被服务器的防火墙解决
掉（如果不采取措施）。但是在服务器上下手总比在客户端上下手合理，它本来就是为客户端服务的嘛。所以就采用被动模式，服务器端的解决办法，就是让防火墙
允许连接向特定端口的数据包通过。

接下来把重点放在vsftp上，我这里搭建的一个很小的环境内的ftp服务器，只有基础设置的一些特别需要注意的地方，更为复杂的设置暂时用不到也就不去学习了，学以致用嘛。

组件安装？

（1）安装：＃sudo apt-get install vsftpd  
（2）软件主要组成:/etc/vsftpd.conf /usr/sbin/vsftpd  
/etc/pam.d/vsftpd   /etc/init.d/vsftpd start|stop|restart|reload}

匿名登录，支持下载上传的配置文件？

anonymous\_enable=YES  
write\_enable=YES  
anon\_umask=022  
anon\_upload\_enable=YES  
anon\_mkdir\_write\_enable=YES  
anon\_other\_write\_enable=YES  
dirmessage\_enable=YES  
xferlog\_enable=YES  
connect\_from\_port\_20=YES  
xferlog\_std\_format=YES  
listen=YES

pam\_service\_name=vsftpd  
userlist\_enable=YES  
tcp\_wrappers=YES

关于目录权限？

默认vsftpd是不允许根目录有写的权限的，所以要自己建立一个对ftp（匿名用户的权限用户）有写的权限的目录。如下所示：

drwxr-xr-x 2 ftp ftp 4096 Apr 11 11:26 pub-writable

注意：关于配置匿名上传和下载的几个注意点：1)ftp的匿名用户在linux系统内是ftp用户；2)匿名用户的默认umask是077，这说明
如果你要上传一个目录上去，连你自己都看不到你自己上传的东西，所以必须将它改成022；3)selinux策略也会影响到匿名用户的上传功能（/etc/selinux/config中把enforcing修改成disabled）。总之，权
限方面的设置是一个很关键的问题，包括selinux规则，系统用户权限和vsftpd配置，必须仔细考虑才能成功。

本地用户登录配置文件？

local\_enable=YES  
write\_enable=YES  
local\_umask=022  
dirmessage\_enable=YES  
xferlog\_enable=YES  
connect\_from\_port\_20=YES  
xferlog\_std\_format=YES  
chroot\_local\_user=YES   //限制本地用户根目录  
local\_root=/var/ftp/pub    //限制本地用户根目录到特定目录  
chroot\_list\_enable=YES  
chroot\_list\_file=/etc/vsftpd/chroot\_list  
//这两项设置不再限制范围内的用户  
listen=YES

pam\_service\_name=vsftpd  
userlist\_enable=YES  
tcp\_wrappers=YES

注意：本地用户需要设置的很少，为了安全需要把本地用户限制在其家里或者特定目录下，chroot\_list\_enable,local\_root,chroot\_list\_enable三个设置项相当重要。

Selinux的权限设置

发现vsftpd和系统权限设置均没有问题，但是无法列举目录下的内容，google了一下有了思路，selinux的默认权限不允许ftp传输，这里直接修改/etc/selinux/config文件内容如下：

SELINUX=disabled

参考文档：<http://bbs.chinaunix.net/thread-561183-1-1.html#> （很全面）

</div>
