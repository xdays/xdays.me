---
title: ssh技巧汇总
date: 2011-08-12
author: admin
category: server
tags: ['linux']
slug: ssh技巧汇总
---

# 自动登录

## 简介

最近苦于 linux 下没有像 SecureCRT 这样便捷的虚拟终端软件，打算利用下这个 ssh 自动登录功能。流程说起来也简单，就是先把公钥和密钥分别保存到服务器和客户端，客户端登录只需要指定对应服务器的密钥就可以自动登录到服务器。

## 配置

这里只列举自动登录到多台服务器的配置过程，对于单台同样适用。

### 生成密钥

    $ ssh-keygen  -t rsa
    nter file in which to save the key
    (/home/lifeix/.ssh/id_rsa): /home/lifeix/.ssh/id_rsa_192.168.60.66
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:
    Your identification has been saved in /home/lifeix/.ssh/id_rsa_192.168.60.66.
    Your public key has been saved in /home/lifeix/.ssh/id_rsa_192.168.60.66.pub

### 添加公钥到服务器

执行命令

    ssh-copy-id root@remote-host

### 建立 alias 别名 在.bashrc 添加一行：

    alias c1='ssh -i /home/lifeix/.ssh/id_rsa_192.168.60.66 root@192.168.60.66'

# ubuntu 系统下 ssh 缓慢

编辑/etc/ssh/ssh_config 添加一行配置：

    GSSAPIAuthentication no
