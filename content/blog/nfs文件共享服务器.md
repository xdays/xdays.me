---
title: NFS文件共享服务器
date: 2012-08-21
author: admin
category: server
tags: nfs, server
slug: nfs文件共享服务器
---

### 基础概念

#### 运行流程

NFS主要用于Linux系统间的文件共享，其方便之处在于client只要权限足够可以直接通过挂载的方式使用server端的目录，通过网络读写数据。NFS是通过几个独立的daemons来实现的，例如其中rpc.nfsd用于验证身份，rpc.mountd负责管理文件系统，rpc.lockd用于锁定文件防止写冲突，rpc.statd用于检查一致性。他们启动后选取小于1024的随机端口来监听，这就造成客户端无法了解服务端监听哪些端口的问题？所以NFS的运行依赖于portmap，portmap启动后会监听111端口，NFS各个服务器启动后需要向portmap注册自己的监听端口，这样当客户端要请求响应服务时先向portmap请求响应服务的端口，然后再去请求响应的服务

#### 权限问题

分以下几种情况讨论：

-   当client与server有完全相同的帐号和组（包括UID），client在server端拥有相应帐号的权限
-   当client与server的用户UID相同时，client可以拥有以服务器端相同UID的权限，这可能会造成问题
-   当server上并不存在client的UID，server端会把client的用户看作是一个匿名帐号，如Centos用nfsnobody
-   当client以root用户访问server，默认server会把root用户改成匿名用户的权限

这样看来一个client用户要对NFS文件系统有些的权限要满足以下三个条件：

-   通过NFS本身的验证
-   在NFS配置中对文件系统有些的权限
-   实际文件系统对响应的用户有些的权限

### 安装

一般系统默认都会安装，用如下命令查询下是否安装

    rpm -q nfs-utils portmap

如果没有安装，yum安装

    yum install -y nfs-utils portmap

### 配置

NFS的配置文件在/etc/exports，其格式如下

    /full/path host1(option) host2(option)
     开放目录绝对路径 主机（选项） 主机（选项）

主机限定形式：

-   完整ip或网段
-   hostname，并且hostname中可以加通配符，如\*或?

各选项及解释如下：

-   rw读写权限
-   ro只读权限
-   async异步写入，先存于内存中
-   sync同步写入，直接写盘
-   root\_squash将root映射为普通用户
-   no\_root\_squash是root就拥有root的权限，不映射
-   all\_squash映射所有用户到普通帐号
-   anonuid/anongid指定匿名用户的UID和GID

### 客户端操作

查看一个主机开放的NFS文件系统:

    showmount -e hostip

像挂载普通文件系统一样挂载NFS文件系统：

    mount -t nfs -o *(options) hostip:/remote/path /local/path

**注：如果server挂了，client无法直接用umount卸载掉相应的文件系统，这时候要给umount加-f参数强制卸载。**

### 双击热备方案

#### 实现功能

两台NFS
server，相互作同步备份（对一台server写入的文件会立刻同步到另一台上），如果一台server挂了，马上切换到另一台上，也就是可以在两台server之间切换

#### 设计思路

主要包括如下要素：

所有时间要有timestamp  
通过nmap定期来判定server是不是已经宕机了，如果端口关闭就表示宕机  
脚本要能判断当前使用的是那台sever，从而推断出下一台server是谁  
如果一台server宕机，马上切换到另一个  
循环不断的做这个检查，脚本运行时间保持大约1分钟（小于1分钟）  
将脚本写入crontab，并且将output重定向到日志中

#### nfs\_v1.sh

    #!/bin/sh
    #
    #date
    nfs1=192.168.60.66
    nfs2=192.168.60.88
    x=1
    sdir=/nfsdata #set the server path
    #cdir=/mnt #set the client path
    cdir=/var/www/html #set the client path
    if [ -z `mount | grep nfsdata | cut -d ":" -f1` ]
    then
        echo "no nfs file system mounted, just mount one!"
        [ -n "`nmap -p2049 $nfs1 | grep open`" ] && `mount -t nfs -o nolock $nfs1:$sdir $cdir` || `mount -t nfs -o nolock $nfs2:$sdir $cdir`
    else
        while [ $x -le 15 ]
        do
            current=`mount | grep nfsdata | cut -d ":" -f1` #get current nfs server for alter between two server
            #echo current nfs server is $current
            [ $nfs1 == $current ] && next=$nfs2 || next=$nfs1 #set next nfs server according to current
            #echo next nfs server is $next
            if [ -n "`nmap -p2049 $current | grep open`" ]
            then
                echo -n `date`
                echo " $current is ok!"
            elif [ -n "`nmap -p2049 $next | grep open`" ]
            then
                echo -n `date`
                echo " $current is down!"
                echo `date` stop http service
                #/sbin/service httpd stop > /root/service.log
                killall httpd
                umount -f $cdir
                echo -n `date`
                echo " umount nfs server successfully!"
                mount -t nfs -o nolock $next:$sdir $cdir
                echo `date` start http service
                #/sbin/service httpd start > /root/service.log
                /usr/sbin/httpd
                echo -n `date`
                echo " change nfs server successfully!"
            else
                echo -n `date`
                echo " server is down!!"
            fi
            #echo sleep 3 seconds!
            sleep 3
            x=$(( $x + 1 ))
        done
    fi
    #date

#### nfs\_v2.sh

这个版本脚本对当前服务器的目录结构有要求，也就是挂载点必须以NFS
sever的IP地址命名，因为挂载点和软链接的source之间存在一定的关联性。

    #!/bin/sh
    #
    #date
    nfs1=192.168.60.66
    nfs2=192.168.60.88
    x=1
    sdir=/nfsdata #set the server path
    #cdir=/mnt #set the client path
    cdir=/var/www/html #set the client path
    cdir1=/$nfs1 #set the client path
    cdir2=/$nfs2 #set the client path
    #if nfses are not mounted and nfs servers are alive just mount them
    [ -z `mount | grep $nfs1 | cut -d ":" -f1` ] && [ -n "`nmap -p2049 $nfs1 | grep open`" ] && `mount -t nfs -o nolock $nfs1:$sdir $cdi
    r1`
    [ -z `mount | grep $nfs2 | cut -d ":" -f1` ] && [ -n "`nmap -p2049 $nfs1 | grep open`" ] && `mount -t nfs -o nolock $nfs2:$sdir $cdi
    r2`
    while [ $x -le 150 ]
    do
        current=`ls -l /var/www/html | cut -d "/" -f5` #get current nfs server for alter between two server
        #echo current nfs server is $current
        [ $nfs1 == $current ] && next=$nfs2 || next=$nfs1 #set next nfs server according to current
        #echo next nfs server is $next
        if [ -n "`nmap -p2049 $current | grep open`" ]
        then
            echo -n `date`
            echo " $current is ok!"
        elif [ -n "`nmap -p2049 $next | grep open`" ]
        then
            echo -n `date`
            echo " $current is down!"
            unlink $cdir && echo -n `date` ; echo " umount nfs server successfully!"
            ln -s /$next $cdir && echo -n `date`; echo " change nfs server successfully!"
        else
            echo -n `date`
            echo " server is down!!"
        fi
        #echo sleep 3 seconds!
        sleep 3
        x=$(( $x + 1 ))
    done
    #date
