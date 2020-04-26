---
title: 非常经典的iptables配置脚本
date: 2011-04-10
author: admin
category: server
tags: ['iptables', 'server', 'linux']
slug: 非常经典的iptables配置脚本
---

花了一下午和一晚上通过<http://www.frozentux.net/iptables-tutorial/cn/iptables-tutorial-cn-1.1.19.html>这篇文档深入学习了 iptables 这一有力的包过滤系统，文档最后作者提供了一个脚本来配置 iptables，我觉得这个脚本的结构设计的相当棒，这里转载过来并附上自己的理解共以后参考。

    #!/bin/sh

    #

    # rc.firewall - Initial SIMPLE IP Firewall script for Linux 2.4.x and iptables

    #

    # Copyright (C) 2001  Oskar Andreasson <bluefluxATkoffeinDOTnet>

    #

    # This program is free software; you can redistribute it and/or modify

    # it under the terms of the GNU General Public License as published by

    # the Free Software Foundation; version 2 of the License.

    #

    # This program is distributed in the hope that it will be useful,

    # but WITHOUT ANY WARRANTY; without even the implied warranty of

    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the

    # GNU General Public License for more details.

    #

    # You should have received a copy of the GNU General Public License

    # along with this program or from the site that you downloaded it

    # from; if not, write to the Free Software Foundation, Inc., 59 Temple

    # Place, Suite 330, Boston, MA  02111-1307   USA

    #

    ###########################################################################

    #

    # 1. Configuration options.

    #

    #

    # 1.1 Internet Configuration.

    #定义网络参数变量

    #

    INET_IP="194.236.50.155"

    INET_IFACE="eth0"

    INET_BROADCAST="194.236.50.255"

    #

    # 1.1.1 DHCP

    #

    #

    # 1.1.2  PPPoE

    #

    #

    # 1.2 Local Area Network configuration.

    #

    # your LAN's IP range and localhost IP. /24 means to only use the first 24

    # bits of the 32 bit IP address. the same as netmask 255.255.255.0

    #

    LAN_IP="192.168.0.2"

    LAN_IP_RANGE="192.168.0.0/16"

    LAN_IFACE="eth1"

    #

    # 1.3 DMZ Configuration.

    #

    #

    # 1.4 Localhost Configuration.

    #

    LO_IFACE="lo"

    LO_IP="127.0.0.1"

    #

    # 1.5 IPTables Configuration.

    #

    IPTABLES="/usr/sbin/iptables"

    #

    # 1.6 Other Configuration.

    #

    ###########################################################################

    #

    # 2. Module loading.

    #加载模块

    #

    #

    # Needed to initially load modules

    #

    /sbin/depmod -a

    #

    # 2.1 Required modules

    #

    /sbin/modprobe ip_tables

    /sbin/modprobe ip_conntrack

    /sbin/modprobe iptable_filter

    /sbin/modprobe iptable_mangle

    /sbin/modprobe iptable_nat

    /sbin/modprobe ipt_LOG

    /sbin/modprobe ipt_limit

    /sbin/modprobe ipt_state

    #

    # 2.2 Non-Required modules

    #

    #/sbin/modprobe ipt_owner

    #/sbin/modprobe ipt_REJECT

    #/sbin/modprobe ipt_MASQUERADE

    #/sbin/modprobe ip_conntrack_ftp

    #/sbin/modprobe ip_conntrack_irc

    #/sbin/modprobe ip_nat_ftp

    #/sbin/modprobe ip_nat_irc

    ###########################################################################

    #

    # 3. /proc set up.

    #设置/proc参数开启转发功能，主要用于nat

    #

    #

    # 3.1 Required proc configuration

    #

    echo "1" > /proc/sys/net/ipv4/ip_forward

    #

    # 3.2 Non-Required proc configuration

    #

    #echo "1" > /proc/sys/net/ipv4/conf/all/rp_filter

    #echo "1" > /proc/sys/net/ipv4/conf/all/proxy_arp

    #echo "1" > /proc/sys/net/ipv4/ip_dynaddr

    ###########################################################################

    #

    # 4. rules set up

    #开始配置具体的规则.

    #

    ######

    # 4.1 Filter table

    #

    #

    # 4.1.1 Set policies

    #

    $IPTABLES -P INPUT DROP

    $IPTABLES -P OUTPUT DROP

    $IPTABLES -P FORWARD DROP

    #

    # 4.1.2 Create userspecified chains

    #作者的总体思路是先写好自定义的链，然后再后续的系统预定义链中调用，类似函数的概

    #念

    #

    # Create chain for bad tcp packets

    #

    $IPTABLES -N bad_tcp_packets

    #

    # Create separate chains for ICMP, TCP and UDP to traverse

    #

    $IPTABLES -N allowed

    $IPTABLES -N tcp_packets

    $IPTABLES -N udp_packets

    $IPTABLES -N icmp_packets

    #

    # 4.1.3 Create content in userspecified chains

    #

    #

    # bad_tcp_packets chain

    #拒绝或者记录不正常的数据包

    #

    $IPTABLES -A bad_tcp_packets -p tcp --tcp-flags SYN,ACK SYN,ACK

    -m state --state NEW -j REJECT --reject-with tcp-reset

    #拒绝带有SYN和ACK标记的状态为NEW的包并返回错误信息

    $IPTABLES -A bad_tcp_packets -p tcp ! --syn -m state --state NEW -j LOG

    --log-prefix "New not syn:"

    #不是SYN标记但是状态时NEW的数据包并记录日志

    $IPTABLES -A bad_tcp_packets -p tcp ! --syn -m state --state NEW -j DROP

    #拒绝不是SYN标记但是状态时NEW的数据包并记录日志

    #

    # allowed chain

    #允许特定的数据包

    #

    $IPTABLES -A allowed -p TCP --syn -j ACCEPT

    #允许带有SYN标记的数据包

    $IPTABLES -A allowed -p TCP -m state --state ESTABLISHED,RELATED -j ACCEPT

    #允许状态为ESTABLISH和RELATED的数据包

    $IPTABLES -A allowed -p TCP -j DROP

    #拒绝其他所有的数据包

    #

    # TCP rules

    #

    $IPTABLES -A tcp_packets -p TCP -s 0/0 --dport 21 -j allowed

    #允许访问ftp服务

    $IPTABLES -A tcp_packets -p TCP -s 0/0 --dport 22 -j allowed

    #允许访问ssh服务

    $IPTABLES -A tcp_packets -p TCP -s 0/0 --dport 80 -j allowed

    #允许访问www服务

    $IPTABLES -A tcp_packets -p TCP -s 0/0 --dport 113 -j allowed

    #允许访问IRC服务

    #

    # UDP ports

    #

    #$IPTABLES -A udp_packets -p UDP -s 0/0 --destination-port 53 -j ACCEPT

    #允许DNS服务

    #$IPTABLES -A udp_packets -p UDP -s 0/0 --destination-port 123 -j ACCEPT

    #允许ntp服务

    $IPTABLES -A udp_packets -p UDP -s 0/0 --destination-port 2074 -j ACCEPT

    #允许多媒体服务

    $IPTABLES -A udp_packets -p UDP -s 0/0 --destination-port 4000 -j ACCEPT

    #允许ICQ服务

    #

    # In Microsoft Networks you will be swamped by broadcasts. These lines

    # will prevent them from showing up in the logs.

    #

    #$IPTABLES -A udp_packets -p UDP -i $INET_IFACE -d $INET_BROADCAST

    #--destination-port 135:139 -j DROP

    #拒绝微软的netbios的广播服务

    #

    # If we get DHCP requests from the Outside of our network, our logs will

    # be swamped as well. This rule will block them from getting logged.

    #

    #$IPTABLES -A udp_packets -p UDP -i $INET_IFACE -d 255.255.255.255

    #--destination-port 67:68 -j DROP

    #拒绝DHCP服务

    #

    # ICMP rules

    #

    $IPTABLES -A icmp_packets -p ICMP -s 0/0 --icmp-type 8 -j ACCEPT

    #允许8类ICMP服务

    $IPTABLES -A icmp_packets -p ICMP -s 0/0 --icmp-type 11 -j ACCEPT

    #允许11类ICMP服务

    #

    # 4.1.4 INPUT chain

    #

    #

    # Bad TCP packets we don't want.

    #

    $IPTABLES -A INPUT -p tcp -j bad_tcp_packets

    #检查是否是坏包

    #

    # Rules for special networks not part of the Internet

    #

    $IPTABLES -A INPUT -p ALL -i $LAN_IFACE -s $LAN_IP_RANGE -j ACCEPT

    #来自内部网络的包一律允许通过

    $IPTABLES -A INPUT -p ALL -i $LO_IFACE -s $LO_IP -j ACCEPT

    #来自本地的包一律通过

    $IPTABLES -A INPUT -p ALL -i $LO_IFACE -s $LAN_IP -j ACCEPT

    $IPTABLES -A INPUT -p ALL -i $LO_IFACE -s $INET_IP -j ACCEPT

    #

    # Special rule for DHCP requests from LAN, which are not caught properly

    # otherwise.

    #

    $IPTABLES -A INPUT -p UDP -i $LAN_IFACE --dport 67 --sport 68 -j ACCEPT

    #允许DHCP服务

    #

    # Rules for incoming packets from the internet.

    #

    $IPTABLES -A INPUT -p ALL -d $INET_IP -m state --state ESTABLISHED,RELATED

    -j ACCEPT

    #允许外部过来的响应本地请求或者和本地已有连接有关系的包

    $IPTABLES -A INPUT -p TCP -i $INET_IFACE -j tcp_packets

    #TCP包由对应链处理

    $IPTABLES -A INPUT -p UDP -i $INET_IFACE -j udp_packets

    #UDP包由对应链处理

    $IPTABLES -A INPUT -p ICMP -i $INET_IFACE -j icmp_packets

    #ICMP包由对应链处理

    #

    # If you have a Microsoft Network on the outside of your firewall, you may

    # also get flooded by Multicasts. We drop them so we do not get flooded by

    # logs

    #

    #$IPTABLES -A INPUT -i $INET_IFACE -d 224.0.0.0/8 -j DROP

    #拒绝组播包

    #

    # Log weird packets that don't match the above.

    #

    $IPTABLES -A INPUT -m limit --limit 3/minute --limit-burst 3 -j LOG

    --log-level DEBUG --log-prefix "IPT INPUT packet died: "

    #如果包与上述规则均不匹配则写入日志

    #

    # 4.1.5 FORWARD chain

    #

    #

    # Bad TCP packets we don't want

    #

    $IPTABLES -A FORWARD -p tcp -j bad_tcp_packets

    #先检查是否是坏包

    #

    # Accept the packets we actually want to forward

    #

    $IPTABLES -A FORWARD -i $LAN_IFACE -j ACCEPT

    #允许由本地发来的包被转发

    $IPTABLES -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

    #允许ESTABLISHED,RELATED状态的包转发

    #

    # Log weird packets that don't match the above.

    #

    $IPTABLES -A FORWARD -m limit --limit 3/minute --limit-burst 3 -j LOG

    --log-level DEBUG --log-prefix "IPT FORWARD packet died: "

    #如果包与上述规则均不匹配则写入日志

    #

    # 4.1.6 OUTPUT chain

    #

    #

    # Bad TCP packets we don't want.

    #

    $IPTABLES -A OUTPUT -p tcp -j bad_tcp_packets

    #先检查是否是坏包

    #

    # Special OUTPUT rules to decide which IP's to allow.

    #

    $IPTABLES -A OUTPUT -p ALL -s $LO_IP -j ACCEPT

    #允许所有包通过

    $IPTABLES -A OUTPUT -p ALL -s $LAN_IP -j ACCEPT

    $IPTABLES -A OUTPUT -p ALL -s $INET_IP -j ACCEPT

    #

    # Log weird packets that don't match the above.

    #

    $IPTABLES -A OUTPUT -m limit --limit 3/minute --limit-burst 3 -j LOG

    --log-level DEBUG --log-prefix "IPT OUTPUT packet died: "

    #如果包与上述规则均不匹配则写入日志

    ######

    # 4.2 nat table

    #

    #

    # 4.2.1 Set policies

    #

    #

    # 4.2.2 Create user specified chains

    #

    #

    # 4.2.3 Create content in user specified chains

    #

    #

    # 4.2.4  PREROUTING chain

    #

    #

    # 4.2.5  POSTROUTING chain

    #

    #

    # Enable simple IP Forwarding and Network Address Translation

    #

    $IPTABLES -t nat -A POSTROUTING -o $INET_IFACE -j SNAT --to-source $INET_IP

    #对所有沿外网口出去的包执行SNAT

    #

    # 4.2.6 OUTPUT chain

    #

    ######

    # 4.3 mangle table

    #

    #

    # 4.3.1 Set policies

    #

    #

    # 4.3.2 Create user specified chains

    #

    #

    # 4.3.3 Create content in user specified chains

    #

    #

    # 4.3.4  PREROUTING chain

    #

    #

    # 4.3.5 INPUT chain

    #

    #

    # 4.3.6 FORWARD chain

    #

    #

    # 4.3.7 OUTPUT chain

    #

    #

    # 4.3.8  POSTROUTING chain

    #

    ##本脚本来自http:

    #www.faqs.org/docs/iptables/index.html
