Title: ubuntu系统管理集锦
Date: 2012-11-10 00:05
Author: admin
Category: linux
Tags: linux, ubuntu
Slug: ubuntu系统管理集锦

简介
====

这是一片持续更新的博客，旨在收集我使用ubuntu过程中遇到的一些命令和规则，记录在这里以免遗忘。

终端软件
========

右键打开
--------

    sudo apt-get install nautilus-open-terminal
    nautilus -q

安装32位包
==========

<http://askubuntu.com/questions/127848/wine-cant-find-gnome-keyring-pkcs11-so>

包管理系统
==========

dpkg
----

-   -i 安装
-   -r 删除（不包括配置文件）
-   -P 删除（包括配置文件）
-   -b 编译
-   -c 查看内容
-   -I 查看包信息
-   -l 查询包
-   -s 查询包状态
-   -L 查看包的文件列表
-   -S 查询文件的所属包

virtualbox中安装server版驱动
----------------------------

    sudo mount /dev/cdrom /media/cdrom
    sudo apt-get install -y dkms build-essential linux-headers-generic linux-headers-$(uname -r)
    sudo /media/cdrom/VBoxLinuxAdditions.run

有“Installing the Window System drivers ...fail!”的错误提示可忽略不计。

<http://en.ig.ma/notebook/2012/virtualbox-guest-additions-on-ubuntu-server>

<http://blog.brettalton.com/2010/04/28/installing-guest-additions-in-virtualbox-for-an-ubuntu-server-guest/>
