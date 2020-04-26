---
title: VPN-基于OpenVPN构建
date: 2011-07-14
author: admin
category: server
tags: ['vpn']
slug: openvpn构建vpn
---

### 简介

openvpn 是一种 ssl
vpn。它最大的优势是构建在 tcp 或 udp，所以可以穿越 proxy，nat，firewalls；此外还可以向 client 端推送 ip 地址，路由和一些关于连接的选项。

### 安装

#### 安装依赖库

    yum install gcc openssl-devel
    cd /usr/local/src
    wget http://www.oberhumer.com/opensource/lzo/download/lzo-2.04.tar.gz
    tar xzvf lzo-2.04.tar.gz
    cd lzo-2.04
    ./configure && make && make check && make test && make install

#### 安装 openvpn

    cd /usr/local/src
    wget http://swupdate.openvpn.net/community/releases/openvpn-2.1.4.zip
    unzip openvpn-2.1.4/zip
    cd openvpn-2.1.4
    ./configure && make && make install

### 生成证书

#### 生成工具

    mkdir -p /etc/openvpn
    mv /usr/local/src/openvpn-2.1.4/easy-rsa/ /etc/openvpn/
    chmod a+x /etc/openvpn/easy-rsa/2.0/*
    cd /etc/openvpn/easy-rsa/2.0

#### 编辑变量文件

    vi  /etc/openvpn/easy-rsa/2.0/vars
    export KEY_COUNTRY="CN"
    export KEY_PROVINCE="BJ"
    export KEY_CITY="BJ"
    export KEY_ORG="www.xdays.me"
    export KEY_EMAIL="xdays@xdays.me"
    source /etc/openvpn/easy-rsa/2.0/vars

#### 生成 cert

    ./clean-all
    ./build-ca 一串回车，建立root ca
    ./build-key-server server 一串回车 两个yes，建立server ca
    ./build-key client1 一串回车两个yes，建立client1 ca
    ./build-key client2 一串回车两个yes，建立client2 ca
    ./build-dh

注意：./build-key client1
命令建立三个文件，client 端需要 ca.crt，client1.crt 和 client1.key

### 配置 openvpn

    vi  /etc/openvpn/server.conf

#### 桥接方式配置

    port 443
    proto tcp
    dev tun
    status /var/log/openvpn/servertcp.log
    management localhost 7505
    ca ca.crt
    cert server.crt
    key server.key
    dh dh1024.pem
    client-to-client
    #server dhcp pool
    server 10.9.9.0 255.255.255.0
    ifconfig-pool-persist servertcplist.txt
    #duplicate-cn
    #push "dhcp-option DNS 8.8.8.8"
    #push "redirect-gateway"
    #push route
    push "route 192.168.61.0 255.255.255.0"
    keepalive 10 120
    comp-lzo
    persist-key
    persist-tun
    verb 3

#### 路由模式配置

    port 443
    proto tcp
    dev tun
    status /var/log/openvpn/servertcp.log
    management localhost 7505
    ca ca.crt
    cert server.crt
    key server.key
    dh dh1024.pem
    client-to-client
    #server dhcp pool
    server 10.9.9.0 255.255.255.0
    ifconfig-pool-persist servertcplist.txt
    #duplicate-cn
    #push dns
    push "dhcp-option DNS 8.8.8.8"
    #push default gateway
    push "redirect-gateway"
    keepalive 10 120
    comp-lzo
    persist-key
    persist-tun
    verb 3

再修改 server 端 iptables 做 nat：

    iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

### client 端配置

windows 安装 OpenVPN
GUI 默认安装到 C 盘，将 server 端生成的 ca.crt，client1.crt 和 client1.key 三个文件拷到 openvpn 安装目录下的 config 目录下，再新建文件 client.ovpn，内容如下：

    client
    port 443
    proto tcp
    dev tun
    remote 192.168.60.66 443
    resolv-retry infinite
    nobind
    ca ca.crt
    cert client1.crt
    key client1.key
    keepalive 10 120
    comp-lzo
    persist-key
    persist-tun
    verb 3
