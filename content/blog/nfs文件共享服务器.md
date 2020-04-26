---
title: NFS文件共享服务器
date: 2012-08-21
author: admin
category: server
tags: ['nfs', 'server']
slug: nfs文件共享服务器
---

### 基础概念

#### 运行流程

NFS 主要用于 Linux 系统间的文件共享，其方便之处在于 client 只要权限足够可以直接通过挂载的方式使用 server 端的目录，通过网络读写数据。NFS 是通过几个独立的 daemons 来实现的，例如其中 rpc.nfsd 用于验证身份，rpc.mountd 负责管理文件系统，rpc.lockd 用于锁定文件防止写冲突，rpc.statd 用于检查一致性。他们启动后选取小于 1024 的随机端口来监听，这就造成客户端无法了解服务端监听哪些端口的问题？所以 NFS 的运行依赖于 portmap，portmap 启动后会监听 111 端口，NFS 各个服务器启动后需要向 portmap 注册自己的监听端口，这样当客户端要请求响应服务时先向 portmap 请求响应服务的端口，然后再去请求响应的服务

#### 权限问题

分以下几种情况讨论：

- 当 client 与 server 有完全相同的帐号和组（包括 UID），client 在 server 端拥有相应帐号的权限
- 当 client 与 server 的用户 UID 相同时，client 可以拥有以服务器端相同 UID 的权限，这可能会造成问题
- 当 server 上并不存在 client 的 UID，server 端会把 client 的用户看作是一个匿名帐号，如 Centos 用 nfsnobody
- 当 client 以 root 用户访问 server，默认 server 会把 root 用户改成匿名用户的权限

这样看来一个 client 用户要对 NFS 文件系统有些的权限要满足以下三个条件：

- 通过 NFS 本身的验证
- 在 NFS 配置中对文件系统有些的权限
- 实际文件系统对响应的用户有些的权限

### 安装

一般系统默认都会安装，用如下命令查询下是否安装

    rpm -q nfs-utils portmap

如果没有安装，yum 安装

    yum install -y nfs-utils portmap

### 配置

NFS 的配置文件在/etc/exports，其格式如下

    /full/path host1(option) host2(option)
     开放目录绝对路径 主机（选项） 主机（选项）

主机限定形式：

- 完整 ip 或网段
- hostname，并且 hostname 中可以加通配符，如\*或?

各选项及解释如下：

- rw 读写权限
- ro 只读权限
- async 异步写入，先存于内存中
- sync 同步写入，直接写盘
- root_squash 将 root 映射为普通用户
- no_root_squash 是 root 就拥有 root 的权限，不映射
- all_squash 映射所有用户到普通帐号
- anonuid/anongid 指定匿名用户的 UID 和 GID

### 客户端操作

查看一个主机开放的 NFS 文件系统:

    showmount -e hostip

像挂载普通文件系统一样挂载 NFS 文件系统：

    mount -t nfs -o *(options) hostip:/remote/path /local/path

**注：如果 server 挂了，client 无法直接用 umount 卸载掉相应的文件系统，这时候要给 umount 加-f 参数强制卸载。**

### 双击热备方案

#### 实现功能

两台 NFS
server，相互作同步备份（对一台 server 写入的文件会立刻同步到另一台上），如果一台 server 挂了，马上切换到另一台上，也就是可以在两台 server 之间切换

#### 设计思路

主要包括如下要素：

所有时间要有 timestamp  
通过 nmap 定期来判定 server 是不是已经宕机了，如果端口关闭就表示宕机  
脚本要能判断当前使用的是那台 sever，从而推断出下一台 server 是谁  
如果一台 server 宕机，马上切换到另一个  
循环不断的做这个检查，脚本运行时间保持大约 1 分钟（小于 1 分钟）  
将脚本写入 crontab，并且将 output 重定向到日志中

#### nfs_v1.sh

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

#### nfs_v2.sh

这个版本脚本对当前服务器的目录结构有要求，也就是挂载点必须以 NFS
sever 的 IP 地址命名，因为挂载点和软链接的 source 之间存在一定的关联性。

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
