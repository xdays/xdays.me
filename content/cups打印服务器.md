Title: cups打印服务器
Date: 2010-12-03 19:31
Author: admin
Category: server
Tags: cups, server
Slug: cups打印服务器

机房里有一台老师淘汰下来的打印机，虽然旧了些但是打印质量没什么问题。近日有一想法，建立共享打印机，也就是机房内所有主机（windows和linux）都能通过这台打印机打印。现有的条件是一台奔四主机做服务器（debian5.0系统），一台USB接口打印机，windows客户机。

什么是CUPS？

通用UNIX打印系统，它能支持IPP，LPD和SMB协议，同时提供友好的管理界面，在windows下添加网络打印机也十分方便；同时，CUPS还提供了验证管理功能，控制共享打印机的使用范围（来源IP和验证等）

安装CUPS？

debian系统得益于apt，安装十分简单，命令如下：

\#apt-get instll cups
 安装过程可能提示设置samba域名默认即可，以及是否需要通过dhcp提供wins信息这里选否。

配置CUPS？

配置文件格式非常类似于apache的配置文件风格。

监听端口默认是只监听localhost，而我的debian没有图形界面，虽然可以用links但是还是不如图形界面友好。这里可以将将监听该做如下行：

Listen \*.631

下面是针对特定目录的设置，主要就是权限方面的设置，在各个段内添加如下行以允许本地主机通过web管理：

Allow your.ip.address.here

这样基本的CUPS就完成了。

windows如何添加网络共享打印机？

网上邻居-\>打印机和传真-\>添加打印机-\>网络打印机或连接到其他计算机的打印机-\>填写URL（注意这里的url格式是http://ip:port/printers/printer-name）-\>选择驱动程序-\>完成

参考链接

官方文档：<http://www.cups.org/index.php>

debianwiki：<http://wiki.debian.org/SystemPrinting>
