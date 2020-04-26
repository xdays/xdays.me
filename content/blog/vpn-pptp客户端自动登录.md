---
title: VPN-PPTP客户端自动登录
date: 2015-10-18
author: admin
category: server
tags: ['vpn']
slug: vpn-pptp客户端自动登录
---

#安装
yum install pptp

#配置
##chap-secrets
vim /etc/ppp/chap-secrets

```
yottaa    pptp password *
```

##peers
vim /etc/ppp/peers/vpn-bos

```
pty "pptp vpn-bos.yottaa.com --nolaunchpppd"
name yottaa-1
remotename pptp
require-mppe-128
file /etc/ppp/options.pptp
```

##options
vim /etc/ppp/options

```
lock
lcp-echo-failure 10
lcp-echo-interval 1
```

# 启动

```
pppd call vpn-bos
</pre>
```
