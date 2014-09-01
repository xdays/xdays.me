Title: 硬盘安装流行linux发行版
Date: 2010-06-06 00:23
Author: admin
Category: linux
Tags: linux, 硬盘安装
Slug: 硬盘安装流行linux发行版

### 概述

比较流行的发行版本每隔一段时间都推出一个版本，不知不觉我也成了最求“时尚”的linux发烧友(虽然我最初的目的不在此))，每推出一个新版本总要试它一把。无奈没有刻录机还要花钱买空盘，刻盘无数消费也不低。于是最近突发总结硬盘安装linux通用方法的想法，特此记录......

### 硬盘安装方法

#### 硬盘安装fedora11

-   下载grub4dos文件（引导安装程序启动），将其中的grldr、grub和menu.lst
    复制到C盘
-   改变menu.lst的内容，在最后加上：

~~~~ {style="padding-left: 30px;"}
title Install Fedora11
root (hd0,4)
kernel (hd0,4)/LiveOS/vmlinuz0 root=/dev/sda5 ro liveimg rhgb
initrd (hd0,4)/LiveOS/initrd0.img
#注意这里的/dev/sda5和(hd0,4)是kernel对应的分区，最好是fat32，ntfs不清楚。
~~~~

-   解压livecd中的LiveOS文件夹到对应的根分区下，并且把vmlinuz0和initrd0.img文件放到LiveOS目录下。
-   打开BOOT.INI ，在末尾填上c:grldr="GRUB4DOS"
-   重启，安装。

#### 硬盘安装ubuntu9.10

-   下载grub4dos文件（引导安装程序启动），将其中的grldr、grub和menu.lst
    复制到C盘
-   改变menu.lst的内容，在最后加上

~~~~ {style="padding-left: 30px;"}
 title Install ubuntu9.10
 root (hd0,4)
 kernel (hd0,4)/vmlinuz boot=casper iso-scan/filename=/ubuntu-9.10-desktop-i386.iso ro quiet splash locale=zh_CN.UTF-8
 initrd (hd0,4)/initrd.lz
 #注意这里的(hd0,4)是kernel对应的分区，支持ntfs文件系统。
~~~~

-   解压出iso文件中的casper目录下的vmlinuz和initrd.lz文件并且将这三个文件一并放到对应的分区的根目录下。
-   打开BOOT.INI ，在末尾填上c:grldr="GRUB4DOS"
-   重启，安装。

### 总结

其实各个版本的安装过程没有太大差别，都是先安装grub4dos在用其去引导内核，然后向内核传递响应的参数，使内核引导起来系统安装程序，最后开始安装。而问题的关键也就在，该向内核传递什么参数，具体不懂希望学习。
