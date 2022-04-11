---
title: Clash透明代理
date: 2020-07-11
author: admin
category: network
tags: ['v2ray', 'iptables']
slug: Clash透明代理
---

# 目标

1. 配置 Clash 使其走 vmess 协议来处理透明代理流量
2. 配置 iptables 转发流量

注意：本文是基于安装了 Debian 系统的的软路由配置的，Openwrt 也可以参考自行修改。

# Clash 优势

相比原生的 V2Ray，Clash 的优势如下：

1. 灵活管理 proxy，支持不同的策略来选择最优的 proxy
2. 内置 DNS，支持 DOH
3. 基于规则来的流量转发

# Clash 安装配置

# 安装

```
TARGET=/usr/local/clash
[ -e $TARGET ] || mkdir $TARGET
VERSION=v1.8.0
FILENAME=clash-linux-amd64-$VERSION
curl -sLO https://github.com/Dreamacro/clash/releases/download/$VERSION/$FILENAME.gz
gunzip $FILENAME.gz
mv $FILENAME $TARGET/clash
chmod 755 $TARGET/clash
```

# Clash 配置

配置这里我是基于[这个模板](https://github.com/Hackl0us/SS-Rule-Snippet/blob/master/LAZY_RULES/clash.yaml)修改的，精简了一些配置。

配置放在 `/usr/local/clash/config.yml`

```
mixed-port: 7890
redir-port: 7892
allow-lan: true
mode: Rule
log-level: info
# secret: ""

dns:
  enable: true
  listen: 0.0.0.0:53
  enhanced-mode: redir-host
  default-nameserver:
    - 119.29.29.29
    - 223.5.5.5
  nameserver:
    - https://doh.pub/dns-query
    - https://dns.alidns.com/dns-query
  fallback:
    - https://1.1.1.1/dns-query # DNS over HTTPS
    - https://8.8.8.8/dns-query # DNS over HTTPS
  fallback-filter:
    geoip: true
    geoip-code: CN
    ipcidr:
      - 240.0.0.0/4

proxies:
- name: vmess-hkg01
  type: vmess
  server: 1.1.1.1
  port: 443
  uuid: changeme
  alterId: 64
  cipher: aes-128-gcm
  network: ws
  ws-path: /
  ws-headers:
    Host: foo.xdays.me
  tls: true
- name: vmess-hkg02
  type: vmess
  server: 2.2.2.2
  port: 443
  uuid: changeme
  alterId: 64
  cipher: aes-128-gcm
  network: ws
  ws-path: /
  ws-headers:
    Host: foo.xdays.me
  tls: true

# 代理组策略
proxy-groups:
# url-test 通过指定的 URL 测试并选择延迟最低的节点
- name: "Group1"
  type: url-test
  proxies:
    - "vmess-hkg01"
    - "vmess-hkg02"
  url: 'http://www.gstatic.com/generate_204'
  interval: 300

# 代理节点选择
- name: "GSLB"
  type: select
  proxies:
    - "Group1"
    - "DIRECT"

rules:
  # Local Area Network
  - IP-CIDR,192.168.0.0/16,DIRECT
  - IP-CIDR,10.0.0.0/8,DIRECT
  - IP-CIDR,172.16.0.0/12,DIRECT
  - IP-CIDR,127.0.0.0/8,DIRECT
  - IP-CIDR,100.64.0.0/10,DIRECT
  - DOMAIN-KEYWORD,linkedin,GSLB
  - GEOIP,CN,DIRECT
  - MATCH,GSLB
```

# 透明代理配置

Clash 的透明代理需要做两步：

1. DNS 解析要经过 Clash 自己监听的 DNS 服务, 我这里是 UDP 的 853 端口
2. iptables 把流量 redirect 给 clash

先说第一步，我的做法是用 dnsmasq 来作为局域网的 dhcp 和 dns server，然后 dnsmasq 将 dns 请求转发给 clash 的 853 端口，dnsmasq 的配置如下:

```
bogus-priv
no-resolv
server=127.0.0.1#853
domain=lan,192.168.2.0/24
dhcp-range=192.168.2.100,192.168.2.200,12h
dhcp-leasefile=/var/lib/misc/dnsmasq.leases
cache-size=150
```

再说第二步，iptables 的配置也很简单，我写了一个脚本来开关 iptables 规则

脚本放在 `/usr/local/clash/proxy.sh`

```
#!/bin/bash

DNSCONF=/etc/dnsmasq.d/local
echo 1 > /proc/sys/net/ipv4/ip_forward

start() {
    # TCP Redirect
    # Create new chain
    echo "create a new chain"
    iptables -t nat -N CLASH

    # Ignore LANs and any other addresses you'd like to bypass the proxy
    # See Wikipedia and RFC5735 for full list of reserved networks.
    iptables -t nat -A CLASH -d 0.0.0.0/8 -j RETURN
    iptables -t nat -A CLASH -d 10.0.0.0/8 -j RETURN
    iptables -t nat -A CLASH -d 127.0.0.0/8 -j RETURN
    iptables -t nat -A CLASH -d 169.254.0.0/16 -j RETURN
    iptables -t nat -A CLASH -d 172.16.0.0/12 -j RETURN
    iptables -t nat -A CLASH -d 192.168.0.0/16 -j RETURN
    iptables -t nat -A CLASH -d 224.0.0.0/4 -j RETURN
    iptables -t nat -A CLASH -d 240.0.0.0/4 -j RETURN
    iptables -t nat -A CLASH -s 192.168.2.0/24 -p tcp -j REDIRECT --to-ports 7892

    # apply redirect for traffic forworded by this proxy
    echo "apply the clash chain"
    iptables -t nat -A PREROUTING  -p tcp -j CLASH

    # apply redirect for proxy itself
    # for i in $OID; do
    #     iptables -t nat -A OUTPUT -m owner --uid-owner $i -j RETURN
    # done
    # iptables -t nat -A OUTPUT -p tcp -j CLASH
    echo "change dns server"
    use-gfw-dns
}

stop() {
    iptables -t nat -D PREROUTING  -p tcp -j CLASH
    iptables -t nat -F CLASH
    iptables -t nat -X CLASH
    use-normal-dns
}

status() {
    echo "==== Iptable rules ===="
    iptables -t nat -nL
    echo
    echo "==== DNS Sever===="
    grep "^server=" $DNSCONF
}

use-normal-dns() {
    # 这里要改成一个你自己的dns服务器
    sed -i '/server=.*/s/.*/server=192.168.1.1/' $DNSCONF
    systemctl restart dnsmasq
}

use-gfw-dns() {
    sed -i '/server=.*/s/.*/server=127.0.0.1#853/' $DNSCONF
    systemctl restart dnsmasq
}

case $1 in
start)
    start
    ;;
stop)
    stop
    ;;
status)
    status
    ;;
*)
    echo "$0 start | stop | status"
    ;;
esac
```

改下可执行权限

```
chmod 755 /usr/local/clash/proxy.sh
```

这个脚本里还包括的切换 dnsmasq 的 dns 配置的操作，因为如果 clash 停了整个局域网所有机器的 dns 解析就会失败，这是配合后边一键启停翻墙做准备的。

# 一键开关透明代理

编辑 `/etc/systemd/system/clash.service`

```
[Unit]
Description=Clash Service
After=network.target
Wants=network.target

[Service]
# User=nobody
# Group=nobody
Type=simple
PIDFile=/run/clash.pid
ExecStartPre=/usr/local/clash/proxy.sh start
ExecStart=/usr/local/clash/clash -d /usr/local/clash/
ExecStopPost=/usr/local/clash/proxy.sh stop
Restart=on-failure
RestartPreventExitStatus=23

[Install]
WantedBy=multi-user.target
```

然后加载配置，开机启动透明代理

```
systemctl daemon-reload
systemctl start clash
systemctl enable clash
```
