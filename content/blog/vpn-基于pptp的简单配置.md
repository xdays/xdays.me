---
title: VPN-基于pptp的简单配置
date: 2011-03-02
author: admin
category: server
tags: ['pptpd', 'server', 'vpn']
slug: vpn-基于pptp的简单配置
---

上学期用 squid 实现了宿舍不用客户端代理上网，但是如果不是全局代理好多软件不支持代理就有很多限制。这学期对 vpn 有了一点了解，发现这才是解决客户端的终极方法。它类似宽带拨号上网，没有任何限制，并且用户管理方便。但是在一个下午的激情努力下，我终于被教程中的概念搞晕了。因为要抓紧学习 NP 的内容，确实没有很大精力搞这个，所以请周丰杰帮忙，这里表示感谢。这里先把配置记录下，至于这其中的原理和详细过程，我想留待以后研究吧。

pptp 的运行原理

实验拓扑图

[![pptpd-vpn-top](/wp-content/uploads/2011/03/pptpd-vpn-top.jpg 'pptpd-vpn-top')](/wp-content/uploads/2011/03/pptpd-vpn-top.jpg)

安装软件包

需要安装的软件包有 ppp，iptables 和 pptpd，我用的 centos5.5 默认包含了 ppp 和 iptables，在有些没有加载 ppp 模块的系统用 modprobe 挂上 ppp_mppe 模块；另外 pptpd 没有包含在源中，要用 wget
http://acelnmp.googlecode.com/files/pptpd-1.3.4-1.rhel5.1.i386.rpm下载后安装。

配置 pptpd 服务

配置如下：

<div id="_mcePaste">

--------------pptp.conf--------------//pptpd 的主配置文件

</div>

<div id="_mcePaste">

option /etc/ppp/options.pptpd 包含 pptp 选项

</div>

<div id="_mcePaste">

logwtmp

</div>

<div id="_mcePaste">

localip
192.168.122.1 这里是本地（服务器端的 ip，当客户端拨号成功服务器会生成一个 ppp 接口与之通信，接口地址在这里指定）

</div>

<div id="_mcePaste">

remoteip 192.168.122.11-130（分配给客户端的地址）

</div>

<div>

---------------chap-secrets----------//用于验证客户端的密码文件，按说明指定

</div>

<div id="_mcePaste">

\# client        server  secret                  IP addresses

</div>

<div id="_mcePaste">

xdays pptpd xdays \*

</div>

<div id="_mcePaste">

---------------options.pptpd--------//pptpd 选项指定文件

</div>

<div id="_mcePaste">

name pptpd

</div>

<div id="_mcePaste">

refuse-pap

</div>

<div id="_mcePaste">

refuse-chap

</div>

<div id="_mcePaste">

refuse-mschap

</div>

<div id="_mcePaste">

require-mschap-v2

</div>

<div id="_mcePaste">

require-mppe-128

</div>

<div id="_mcePaste">

proxyarp

</div>

<div id="_mcePaste">

lock

</div>

<div id="_mcePaste">

nobsdcomp

</div>

<div id="_mcePaste">

novj

</div>

<div id="_mcePaste">

novjccomp

</div>

<div id="_mcePaste">

nologfd

</div>

<div id="_mcePaste">

idle 2592000

</div>

<div id="_mcePaste">

ms-dns 8.8.8.8 指定分配给客户端的 DNS 服务器地址

</div>

<div id="_mcePaste">

ms-dns 8.8.4.4

</div>

<div>

配置 iptables

</div>

<div>

因为客户端拨进来后要访问外网，所以在服务器这一端还要用 iptables 配 nat，具体规则如下：

</div>

<div>

iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -o eth0 -j
MASQUERADE 意思是所有来自 192.168.0.0/24 网段的地址都以 eth0 接口的地址伪装然后发送出去。

</div>

相关资料：

<http://blog.renhao.org/2010/08/build-pptp-vpn-on-centos-5-5/>
