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
VERSION=v1.0.0
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
port: 7890
socks-port: 7891
redir-port: 7892
allow-lan: true
mode: Rule
log-level: info
external-controller: 127.0.0.1:9090
# secret: ""

dns:
  enable: true
  listen: 0.0.0.0:853
  enhanced-mode: redir-host
  nameserver:
    - 'tls://dns.rubyfish.cn:853'
    - '114.114.114.114'
  fallback:
    - 'tls://1.1.1.1:853'
    - 'tls://dns.google'


proxies:
# 这两个tlb proxy配合我的tlb项目使用的，因为clash内置了proxy选择的策略，所以目前暂时也没有开发的动力
# https://github.com/xdays/tlb
- name: ss-tlb
  type: ss
  server: 127.0.0.1
  port: 443
  cipher: rc4-md5
  password: changeme

- name: vmess-tlb
  type: vmess
  server: 127.0.0.1
  port: 345
  uuid: changeme
  alterId: 64
  cipher: aes-128-gcm
  network: ws
  ws-path: /
  ws-headers:
    Host: foo.xdays.me
  tls: true

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
  server: 1.1.1.2
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
- name: "UrlTest"
  type: url-test
  proxies:
    - "vmess-hkg01"
    - "vmess-hkg02"
  url: 'http://www.gstatic.com/generate_204'
  interval: 300

# fallback 通过指定的 URL 测试并选择可用的节点，当 1 故障不可用时自动切换到 2 以此类推
- name: "Fallback"
  type: fallback
  proxies:
    - "vmess-hkg01"
  url: 'http://www.gstatic.com/generate_204'
  interval: 300

# 代理节点选择
- name: "PROXY"
  type: select
  proxies:
    - "UrlTest"
    - "vmess-tlb"
    - "vmess-hkg01"

# 白名单模式 PROXY，黑名单模式 DIRECT
- name: "Final"
  type: select
  proxies:
    - "PROXY"
    - "DIRECT"

# 运营商及声名狼藉网站劫持
- name: "Hijacking"
  type: select
  proxies:
    - "REJECT"
    - "DIRECT"

# 规则
rules:
# Internet Service Providers Hijacking 运营商劫持
- DOMAIN-SUFFIX,17gouwuba.com,Hijacking
- DOMAIN-SUFFIX,186078.com,Hijacking
- DOMAIN-SUFFIX,189zj.cn,Hijacking
- DOMAIN-SUFFIX,285680.com,Hijacking
- DOMAIN-SUFFIX,3721zh.com,Hijacking
- DOMAIN-SUFFIX,4336wang.cn,Hijacking
- DOMAIN-SUFFIX,51chumoping.com,Hijacking
- DOMAIN-SUFFIX,51mld.cn,Hijacking
- DOMAIN-SUFFIX,51mypc.cn,Hijacking
- DOMAIN-SUFFIX,58mingri.cn,Hijacking
- DOMAIN-SUFFIX,58mingtian.cn,Hijacking
- DOMAIN-SUFFIX,5vl58stm.com,Hijacking
- DOMAIN-SUFFIX,6d63d3.com,Hijacking
- DOMAIN-SUFFIX,7gg.cc,Hijacking
- DOMAIN-SUFFIX,91veg.com,Hijacking
- DOMAIN-SUFFIX,9s6q.cn,Hijacking
- DOMAIN-SUFFIX,adsame.com,Hijacking
- DOMAIN-SUFFIX,aiclk.com,Hijacking
- DOMAIN-SUFFIX,akuai.top,Hijacking
- DOMAIN-SUFFIX,atplay.cn,Hijacking
- DOMAIN-SUFFIX,baiwanchuangyi.com,Hijacking
- DOMAIN-SUFFIX,beerto.cn,Hijacking
- DOMAIN-SUFFIX,beilamusi.com,Hijacking
- DOMAIN-SUFFIX,benshiw.net,Hijacking
- DOMAIN-SUFFIX,bianxianmao.com,Hijacking
- DOMAIN-SUFFIX,bryonypie.com,Hijacking
- DOMAIN-SUFFIX,cishantao.com,Hijacking
- DOMAIN-SUFFIX,cszlks.com,Hijacking
- DOMAIN-SUFFIX,cudaojia.com,Hijacking
- DOMAIN-SUFFIX,dafapromo.com,Hijacking
- DOMAIN-SUFFIX,daitdai.com,Hijacking
- DOMAIN-SUFFIX,dsaeerf.com,Hijacking
- DOMAIN-SUFFIX,dugesheying.com,Hijacking
- DOMAIN-SUFFIX,dv8c1t.cn,Hijacking
- DOMAIN-SUFFIX,echatu.com,Hijacking
- DOMAIN-SUFFIX,erdoscs.com,Hijacking
- DOMAIN-SUFFIX,fan-yong.com,Hijacking
- DOMAIN-SUFFIX,feih.com.cn,Hijacking
- DOMAIN-SUFFIX,fjlqqc.com,Hijacking
- DOMAIN-SUFFIX,fkku194.com,Hijacking
- DOMAIN-SUFFIX,freedrive.cn,Hijacking
- DOMAIN-SUFFIX,gclick.cn,Hijacking
- DOMAIN-SUFFIX,goufanli100.com,Hijacking
- DOMAIN-SUFFIX,goupaoerdai.com,Hijacking
- DOMAIN-SUFFIX,gouwubang.com,Hijacking
- DOMAIN-SUFFIX,gzxnlk.com,Hijacking
- DOMAIN-SUFFIX,haoshengtoys.com,Hijacking
- DOMAIN-SUFFIX,hyunke.com,Hijacking
- DOMAIN-SUFFIX,ichaosheng.com,Hijacking
- DOMAIN-SUFFIX,ishop789.com,Hijacking
- DOMAIN-SUFFIX,jdkic.com,Hijacking
- DOMAIN-SUFFIX,jiubuhua.com,Hijacking
- DOMAIN-SUFFIX,jsncke.com,Hijacking
- DOMAIN-SUFFIX,junkucm.com,Hijacking
- DOMAIN-SUFFIX,jwg365.cn,Hijacking
- DOMAIN-SUFFIX,kawo77.com,Hijacking
- DOMAIN-SUFFIX,kualianyingxiao.cn,Hijacking
- DOMAIN-SUFFIX,kumihua.com,Hijacking
- DOMAIN-SUFFIX,ltheanine.cn,Hijacking
- DOMAIN-SUFFIX,maipinshangmao.com,Hijacking
- DOMAIN-SUFFIX,minisplat.cn,Hijacking
- DOMAIN-SUFFIX,mkitgfs.com,Hijacking
- DOMAIN-SUFFIX,mlnbike.com,Hijacking
- DOMAIN-SUFFIX,mobjump.com,Hijacking
- DOMAIN-SUFFIX,nbkbgd.cn,Hijacking
- DOMAIN-SUFFIX,newapi.com,Hijacking
- DOMAIN-SUFFIX,pinzhitmall.com,Hijacking
- DOMAIN-SUFFIX,poppyta.com,Hijacking
- DOMAIN-SUFFIX,qianchuanghr.com,Hijacking
- DOMAIN-SUFFIX,qichexin.com,Hijacking
- DOMAIN-SUFFIX,qinchugudao.com,Hijacking
- DOMAIN-SUFFIX,quanliyouxi.cn,Hijacking
- DOMAIN-SUFFIX,qutaobi.com,Hijacking
- DOMAIN-SUFFIX,ry51w.cn,Hijacking
- DOMAIN-SUFFIX,sg536.cn,Hijacking
- DOMAIN-SUFFIX,sifubo.cn,Hijacking
- DOMAIN-SUFFIX,sifuce.cn,Hijacking
- DOMAIN-SUFFIX,sifuda.cn,Hijacking
- DOMAIN-SUFFIX,sifufu.cn,Hijacking
- DOMAIN-SUFFIX,sifuge.cn,Hijacking
- DOMAIN-SUFFIX,sifugu.cn,Hijacking
- DOMAIN-SUFFIX,sifuhe.cn,Hijacking
- DOMAIN-SUFFIX,sifuhu.cn,Hijacking
- DOMAIN-SUFFIX,sifuji.cn,Hijacking
- DOMAIN-SUFFIX,sifuka.cn,Hijacking
- DOMAIN-SUFFIX,smgru.net,Hijacking
- DOMAIN-SUFFIX,taoggou.com,Hijacking
- DOMAIN-SUFFIX,tcxshop.com,Hijacking
- DOMAIN-SUFFIX,tjqonline.cn,Hijacking
- DOMAIN-SUFFIX,topitme.com,Hijacking
- DOMAIN-SUFFIX,tt3sm4.cn,Hijacking
- DOMAIN-SUFFIX,tuia.cn,Hijacking
- DOMAIN-SUFFIX,tuipenguin.com,Hijacking
- DOMAIN-SUFFIX,tuitiger.com,Hijacking
- DOMAIN-SUFFIX,websd8.com,Hijacking
- DOMAIN-SUFFIX,wsgblw.com,Hijacking
- DOMAIN-SUFFIX,wx16999.com,Hijacking
- DOMAIN-SUFFIX,xchmai.com,Hijacking
- DOMAIN-SUFFIX,xiaohuau.xyz,Hijacking
- DOMAIN-SUFFIX,ygyzx.cn,Hijacking
- DOMAIN-SUFFIX,yinmong.com,Hijacking
- DOMAIN-SUFFIX,yitaopt.com,Hijacking
- DOMAIN-SUFFIX,yjqiqi.com,Hijacking
- DOMAIN-SUFFIX,yukhj.com,Hijacking
- DOMAIN-SUFFIX,zhaozecheng.cn,Hijacking
- DOMAIN-SUFFIX,zhenxinet.com,Hijacking
- DOMAIN-SUFFIX,zlne800.com,Hijacking
- DOMAIN-SUFFIX,zunmi.cn,Hijacking
- DOMAIN-SUFFIX,zzd6.com,Hijacking
- IP-CIDR,39.107.15.115/32,Hijacking,no-resolve
- IP-CIDR,47.89.59.182/32,Hijacking,no-resolve
- IP-CIDR,103.49.209.27/32,Hijacking,no-resolve
- IP-CIDR,123.56.152.96/32,Hijacking,no-resolve
# > ChinaTelecom
- IP-CIDR,61.160.200.223/32,Hijacking,no-resolve
- IP-CIDR,61.160.200.242/32,Hijacking,no-resolve
- IP-CIDR,61.160.200.252/32,Hijacking,no-resolve
- IP-CIDR,61.174.50.214/32,Hijacking,no-resolve
- IP-CIDR,111.175.220.163/32,Hijacking,no-resolve
- IP-CIDR,111.175.220.164/32,Hijacking,no-resolve
- IP-CIDR,122.229.8.47/32,Hijacking,no-resolve
- IP-CIDR,122.229.29.89/32,Hijacking,no-resolve
- IP-CIDR,124.232.160.178/32,Hijacking,no-resolve
- IP-CIDR,175.6.223.15/32,Hijacking,no-resolve
- IP-CIDR,183.59.53.237/32,Hijacking,no-resolve
- IP-CIDR,218.93.127.37/32,Hijacking,no-resolve
- IP-CIDR,221.228.17.152/32,Hijacking,no-resolve
- IP-CIDR,221.231.6.79/32,Hijacking,no-resolve
- IP-CIDR,222.186.61.91/32,Hijacking,no-resolve
- IP-CIDR,222.186.61.95/32,Hijacking,no-resolve
- IP-CIDR,222.186.61.96/32,Hijacking,no-resolve
- IP-CIDR,222.186.61.97/32,Hijacking,no-resolve
# > ChinaUnicom
- IP-CIDR,106.75.231.48/32,Hijacking,no-resolve
- IP-CIDR,119.4.249.166/32,Hijacking,no-resolve
- IP-CIDR,220.196.52.141/32,Hijacking,no-resolve
- IP-CIDR,221.6.4.148/32,Hijacking,no-resolve
# > ChinaMobile
- IP-CIDR,114.247.28.96/32,Hijacking,no-resolve
- IP-CIDR,221.179.131.72/32,Hijacking,no-resolve
- IP-CIDR,221.179.140.145/32,Hijacking,no-resolve
# > Dr.Peng
# - IP-CIDR,10.72.25.0/24,Hijacking,no-resolve
- IP-CIDR,115.182.16.79/32,Hijacking,no-resolve
- IP-CIDR,118.144.88.126/32,Hijacking,no-resolve
- IP-CIDR,118.144.88.215/32,Hijacking,no-resolve
- IP-CIDR,118.144.88.216/32,Hijacking,no-resolve
- IP-CIDR,120.76.189.132/32,Hijacking,no-resolve
- IP-CIDR,124.14.21.147/32,Hijacking,no-resolve
- IP-CIDR,124.14.21.151/32,Hijacking,no-resolve
- IP-CIDR,180.166.52.24/32,Hijacking,no-resolve
- IP-CIDR,211.161.101.106/32,Hijacking,no-resolve
- IP-CIDR,220.115.251.25/32,Hijacking,no-resolve
- IP-CIDR,222.73.156.235/32,Hijacking,no-resolve

# Local Area Network
- IP-CIDR,192.168.0.0/16,DIRECT
- IP-CIDR,10.0.0.0/8,DIRECT
- IP-CIDR,172.16.0.0/12,DIRECT
- IP-CIDR,127.0.0.0/8,DIRECT
- IP-CIDR,100.64.0.0/10,DIRECT

# GeoIP China
- GEOIP,CN,DIRECT

- MATCH,Final
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
