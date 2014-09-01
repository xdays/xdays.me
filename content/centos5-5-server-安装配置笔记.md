Title: centos5.5-server 安装配置笔记
Date: 2010-10-07 17:55
Author: admin
Category: server
Tags: centos, lamp, proxy, server, vsftp
Slug: centos5-5-server-安装配置笔记

上学起用机房的机器搭了一台服务器，底层系统是rhel5.4，提供各种服务，其中包括ssh,nat,lamp,ftp,proxy等。由于是边学习边试验有很多不恰当的地方，系统也装了很多用不到的软件。一方面打算把系统管理的更有条理，另一方面更重要的是好好复习一下以前学的知识，这次打算用centos5.5最小化安装，然后配置各种服务，也记录一下这个过程希望于人于己都能有所帮助。

机器配置：

机房配置：  
处理器：Intel Pentium 4, 2377 MHz (18 x 132)  
内存：512M（SDRAM）  
显卡：GeForce4 MX 440 with AGP8X（64M）  
硬盘：2块40G  
网卡：2块RealTek8139  
主板：Epox EP-4PEA800(I)  
BIOS：Phoenix-Award BIOS v6.00PG

一、硬盘安装

​1.
由于原先安装了rhel由grub引导，第2块硬盘做ftp的数据盘，所以把原先的数据都备份到这块硬盘上了，主要包括一些套件源码包和配置文件。

​2. 拷贝出系统镜像下的isolinux目录到第二块硬盘，mount  -o loop
/var/ftp/xos/centos5.5.iso /mnt，cp -r /mnt/isolinux /var/ftp，umount
/mnt。

​3. 编辑grub配置文件/boot/grub/menu.ist，添加如下内容：

title CentOS  
kernel(hd0,0)/isolinux/vmlinuz  
initrd(hd0,0)/isolinux/initrd.img

4.重启引导。

5.分区，自定义安装包，安装gcc，automake和base
group下的部分软件包，也基本上是最小化安装了。

二、初始配置

1.查看安装了多少包，rpm -qa | wc -l，335个还可以。

​2. 配置网络

​1)
备份默认配置文件(以后的配置前都要执行这一步，只是本文省略不写了)，养成好习惯。cd
/etc/sysconfig/network-script/，mkdir backup ，cp ifcfg-eth0 backup/。

​2) 修改ifcfg-eth0如下：

﻿﻿DEVICE=eth0  
BOOTPROTO=static  
HWADDR=00:A1:B0:13:F0:D9  
ONBOOT=yes  
IPADDR=192.168.1.251  
NETMASK=255.255.255.0  
GATEWAY=192.168.1.1

​3) 添加DNS服务器地址，编辑/etc/resolv.conf添加如下两行：  
nameserver 210.44.176.1  
nameserver 202.102.152.3

三、配置ssh

系统默认安装并且启动了ssh服务，这里仅修改一下配置文件使root可以直接登录，去掉PermitRootLogin
yes这一行的注释。另外配置文件的详细介绍参考：ssh服务器一文<http://www.xdays.info/?p=99>

四、挂载centos镜像作为本地源。

​1) mkdir /media/Centos

​2) cd /etc/yum.repos.d/;mv ﻿﻿﻿CentOS-Base.repo CentOS-Base.repo.backup
; cp CentOS-Media.repo  CentOS-Media.repo.backup

3)编辑CentOS-Media.repo修改如下：

[c5-media]

<div id="_mcePaste">

name=CentOS-\$releasever - Media

</div>

<div id="_mcePaste">

baseurl=file:///media/CentOS/

</div>

<div id="_mcePaste">

\#        file:///media/cdrom/

</div>

<div id="_mcePaste">

\#        file:///media/cdrecorder/

</div>

<div id="_mcePaste">

gpgcheck=1

</div>

<div id="_mcePaste">

enabled=1

</div>

<div id="_mcePaste">

gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-5

</div>

[c5-media]name=CentOS-\$releasever -
Mediabaseurl=file:///media/CentOS/\#        file:///media/cdrom/\#      
 file:///media/cdrecorder/gpgcheck=1enabled=1gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-5

​4) 开机挂在硬盘，在/etc/fstab添加一行：

/dev/hdb1               /var/ftp                ext3    defaults      
 0 2

​5) 开机挂在光盘镜像，在/etc/rc.local中添加一行：

mount -o loop /var/ftp/centos5.5.iso /media/CentOS/

注意：下面的服务器套件的安装基本都是从源码安装，这里自己养成一个习惯：把下载下来的源码压缩包都放在/usr/local/src/目录下，解压后的源文件目录在安装后保留以便以后更新卸载使用。习惯程序安装载/usr/local/目录下，即给configure脚本添加选项--prefix=/usr/local.安装好测试时要关闭防火墙，否则请求就被拒之门外了。

五、架设ftp服务器

​1) 编辑builddefs.h文件，选择添加功能都添加上以便以后拓展。

​2) 参照INSTALL文件添加用户和目录。

​3) make install;cp vsftpd.conf /etc。

​4) 配置参考简易vsftp搭建一文<http://www.xdays.info/?p=101>

​5) 开机自动运行，在/etc/rc.local添加一行/usr/local/sbin/vsftpd
&（后台运行不要忘了，不然的话它一直占用前台就没办法登录了）

六、架设proxy服务器

​1) 安装参考INSTALL文件

​2) 配置参考proxy 服务器-squid一文<http://www.xdays.info/?p=192>

七、搭建lamp环境

安装配置参考lamp环境搭建一文<http://www.xdays.info/?p=290>
