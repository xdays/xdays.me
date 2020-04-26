---
title: synergy一套鼠键管理多台机器
date: 2013-05-12
author: admin
category: tool
tags: ['software']
slug: synergy一套鼠键管理多台机器
---

# 背景

前段时间购得一[RaspberryPi](http://www.raspberrypi.org/),在一切初始化就绪后发现一个问题：同时操作笔记本和 Pi 的时候切换鼠标键盘非常不爽，不够简单（简单很重要）。所以就找到了[synergy](http://synergy-foss.org/zh/)这个小软件，解决了问题。

# 功能

- 用一套鼠标键盘同时操作多台电脑，鼠标触及屏幕边缘就切换到另一台电脑；
- 共享剪切板。

# 安装配置

# 安装

debian/ubuntu 下用如下命令安装：

    sudo apt-get install synergy

# 配置

样例配置如下：

    section: screens
            xdays-ThinkPad-E520:
            raspberrypi:
    end
    section: links
            xdays-ThinkPad-E520:
                 right = raspberrypi
            raspberrypi:
                 left = xdays-ThinkPad-E520
    end

具体配置相关解释可参考 manpage

# 运行

客户端:

    synergyc -f ipaddress:port

服务端

    synergys -f -c /path/to/configure

# 方案参考

由于 synergy 需要联网操作，目前我考虑网络方案如下：Pi 和笔记本用网线连接，Pi 作为 DHCP 服务器为笔记本分配固定地址，Pi 的默认网关指向该地址，笔记本做路由转发。这样一来，笔记本不需要做任何额外的操作(笔记本一直在为虚拟机做路由转发)，Pi 既和笔记本联网也可以有公网访问，所有问题都解决了。
