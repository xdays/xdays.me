---
title: VPN-PPTP客户端自动登录
date: 2015-10-18
author: admin
category: server
tags: vpn
slug: vpn-pptp客户端自动登录
---
 
#安装
    yum install pptp 

#配置
##chap-secrets
vim /etc/ppp/chap-secrets
<pre>
yottaa    pptp password * 
</pre>

##peers
vim /etc/ppp/peers/vpn-bos
<pre>
pty "pptp vpn-bos.yottaa.com --nolaunchpppd" 
name yottaa-1 
remotename pptp 
require-mppe-128 
file /etc/ppp/options.pptp 
</pre>

##options
vim /etc/ppp/options
<pre>
lock 
lcp-echo-failure 10 
lcp-echo-interval 1 
</pre>

# 启动
<pre>
pppd call vpn-bos
</pre> 
