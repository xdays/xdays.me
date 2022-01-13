---
title: dhcp服务器
date: 2010-07-18
author: admin
category: server
tags: ['dhcp', 'server']
slug: dhcp服务器
---

执行过程：

1、客户发出的 IP 租用请求报文

DHCP 客户机初始化 TCP/IP，通过 UDP 端口 67 向网络中发送一个 DHCPDISCOVER 广播包，请求租用 IP 地址。该
广播包中的源 IP 地址为 0.0.0.0，目标 IP 地址为 255.255.255.255；包中还包含客户机的 MAC 地址和计算机名。

2、DHCP 回应的 IP 租用提供报文

任何接收到 DHCPDISCOVER 广播包并且能够提供 IP 地址的 DHCP 服务器，都会通过 UDP 端口 68 给客户机回应一个 DHCPOFFER 广播
包，提供一个 IP 地址。该广播包的源 IP 地址为 DCHP 服务器 IP，目标 IP 地址为 255.255.255.255；包中还包含提供的 IP 地址、子网掩码
及租期等信息。

3、客户选择 IP 租用报文

客户机从不止一台 DHCP 服务器接收到提供之后，会选择第一个收到的 DHCPOFFER 包，并向网络中广播一个
DHCPREQUEST 消息包，表明自己已经接受了一个 DHCP 服务器提供的 IP 地址。该广播包中包含所接受的 IP 地址和服务器的 IP 地址。
所有其他的 DHCP 服务器撤消它们的提供以便将 IP 地址提供给下一次 IP 租用请求。

4、DHCP 服务器发出 IP 租用确认报文

被客户机选择的 DHCP 服务器在收到 DHCPREQUEST 广播后，会广播返回给客户机一个 DHCPACK 消息包，表明已经接受客户机的选择，并将这
一 IP 地址的合法租用以及其他的配置信息都放入该广播包发给客户机。

5、客户配置成功后发出的公告报文

客户机在收到 DHCPACK 包，会使用该广播包中的信息来配置自己的 TCP/IP，则租用过程完成，客户机可以在网络中通信。

至此一个客户获取 IP 的 DHCP 服务过程基本结束，不过客户获取的 IP 一般是用租期，到期前需要更新租期，这个过程是通过租用更新数据包来完成的。

安装配置：

1. `#sudo apt-get install dhcp3-server`

2. 启动停止脚本：/etc/init.d/dhcp3-server start | stop | status | reload

3. 配置文件：/etc/dhcp3/dhcpd.conf，配置文件对基本配置的说明很清楚了，这里只重点强调几个配置选项。

1）基本及动态配置：

```
default-lease-time 600;//默认租期
max-lease-time 7200;
subnet 10.254.239.0 netmask 255.255.255.224 {  //建立地址池
    range 10.254.239.10 10.254.239.20;  //用于dhcp协议的地址范围
    range dynamic-bootp 10.254.239.40 10.254.239.60;  
    //用于bootp协议的地址范围
    option routers 10.254.239.1; //网关
    option broadcast-address 10.254.239.63;  //广播地址
    option domain-name-servers 192.168.10.1;  //dns服务器地址
}
```

2）静态配置：

```
host fantasia {
    hardware ethernet 08:00:07:26:c0:a5;  //按照规定格式
    fixed-address 10.254.239.62;
}
```
