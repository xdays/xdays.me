---
title: VPN-基于pptp的编译安装
date: 2012-08-20
author: admin
category: server
tags: ['vpn']
slug: vpn-基于pptp的编译安装
---

### 安装依赖

#### 安装 ppp

    yum install ppp -y

### 下载源码

#### 下载 pptpd

    wget -SO /usr/local/src/pptpd-1.3.4.tar.gz http://sourceforge.net/projects/poptop/files/pptpd/pptpd-1.3.4/pptpd-1.3.4.tar.gz/download

### 编译安装

#### 解压

    cd /usr/local/src;tar xzf pptpd-1.3.4.tar.gz

修改头文件 vim /usr/local/src/pptpd-1.3.4/plugins/patchlevel.h，将
\#define VERSION "2.4.3" 改为 \#define VERSION "2.4.5"

**注意：此处如果不修改，pptpd 的插件会报错，版本不一致**

#### 配置编译安装

    cd pptpd-1.3.4;./configure --prefix=/usr/local/pptpd && make && make install

### 配置

#### 下载配置文件 sample

    wget -SO /etc/pptpd.conf http://poptop.sourceforge.net/dox/pptpd.conf.txt
    wget -SO /etc/ppp/options.pptpd http://poptop.sourceforge.net/dox/options.pptpd.txt
    wget -SO /etc/ppp/chap-secrets http://poptop.sourceforge.net/dox/chap-secrets.txt

#### 修改配置文件 vim /etc/pptpd.conf

    localip 192.168.1.1 #本地接口ip地址
    remoteip 192.168.1.234-238,192.168.1.245 #分配给远端接口的ip地址

vim /etc/ppp/options.pptpd

    ms-dns 8.8.8.8 #DNS地址
    ms-dns 8.8.4.4

vim /etc/ppp/chap-secrets

    xdays pptpd %%%%% * #验证密码

#### 启动服务

    /usr/local/pptpd/sbin/pptpd
