Title: Bind搭建DNS服务系统
Date: 2013-10-16 15:31
Author: admin
Category: server
Tags: bind, dns, server
Slug: bind搭建dns服务系统

简介
====

Bind是目前应用最广泛的DNS服务器软件，其主要包括服务器实现，解析器库实现和测试三个部分。

说明
====

本文仅讨论如何把Bind配置成一台DNS域名服务器，关于DNS协议的说明，请参考[DNS协议详解](dns协议详解.md)

安装
====

centos
------

    yum install bind bind-libs bind-utils bind-chroot

其中bind-chroot用于让bind运行于chroot模式下。

ubuntu
------

    apt-get install bind9 dnsutils

配置
====

概述
----

bind的配置文件为named.conf，没有chroot时位于/etc/named.conf，chroot时位于/var/named/chroot/etc/named.conf下。配置文件由配置语句和注释组成。关于配置的详细说明可参考[BIND
9 Administrator Reference
Manual](http://www.oit.uci.edu/dcslib/bind/bind-9.2.1/Bv9ARM.html)

配置语句列表
------------

-   acl 定义一个IP列表名，用于接入控制
-   controls 宣告rndc使用的控制通道
-   include 包含一个文件
-   key 设置密钥信息，用于授权和认证配置中
-   logging 设置日志服务器
-   options 控制服务器的全局配置
-   server 单服务器基础上配置
-   trusted-keys 定义信任的 DNSSED 密匙
-   view 定义视图
-   zone 定义zonefile

注释形式
--------

-   C语言风格
-   C++风格
-   Shell风格

Zonefile
--------

### TTL

zone文件有三处控制TTL的地方，分别是：

-   \$TTL 是没有指定TTL的记录使用的缓存时间
-   SOA 记录中的TTL是NXDOMAIN相应的缓存时间
-   资源记录的第二个字段记录了本记录的缓存时间

### SOA记录

SOA记录是zone文件里最复杂的记录类型了，所以单独说明下：

    $TTL 2d ; zone TTL default = 2 days or 172800 seconds
    $ORIGIN example.com.
    @      IN      SOA   ns.example.net. hostmaster.example.com. (
                   2003080800 ; serial number
                   1d12h      ; refresh =  1 day 12 hours
                   15M        ; update retry = 15 minutes
                   3W12h      ; expiry = 3 weeks + 12 hours
                   2h20M      ; minimum = 2 hours + 20 minutes
                   )

具体参考[这里](http://www.zytrax.com/books/dns/ch8/soa.html)

### 其他记录

记录格式为：

    名称 TTL 类 类型 具体信息（随类型变化而变化）

示例如下：

    www 360 IN A 192.168.1.1
    @ 360 IN MX 90 mail.example.com
    @ 360 IN NS ns.example.com

演示
====

说明
----

本示例我将演示如何通过四台服务器搭建一个完整DNS系统，其中包括root，com和info的授权，xdays.com和xdays.me的授权案，cache-only域名解析服务器。

配置
----

### root

named.conf如下：

    //
    // named.conf
    //
    // Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
    // server as a caching only nameserver (as a localhost DNS resolver only).
    //
    // See /usr/share/doc/bind*/sample/ for example named configuration files.
    //


    options {
     listen-on port 53 { any; };
     //listen-on-v6 port 53 { ::1; };
     directory  "/var/named";
     dump-file  "/var/named/data/cache_dump.db";
            statistics-file "/var/named/data/named_stats.txt";
            memstatistics-file "/var/named/data/named_mem_stats.txt";
     allow-query     { any; };
     recursion yes;


     //dnssec-enable yes;
     //dnssec-validation yes;
     dnssec-enable no;
     dnssec-validation no;
     dnssec-lookaside auto;


     /* Path to ISC DLV key */
     bindkeys-file "/etc/named.iscdlv.key";


     managed-keys-directory "/var/named/dynamic";
    };


    logging {
            channel default_debug {
                    file "data/named.run";
                    severity dynamic;
            };
    };


    zone "." IN {
     type master;
     file "named.ca";
    };


    include "/etc/named.rfc1912.zones";
    include "/etc/named.root.key";

named.ca如下：

    $TTL 86400
    @ IN SOA @ root (
     42 ; serial (d. adams)
     3H ; refresh
     15M ; retry
     1W ; expiry
     1D ) ; minimum


    . 518400 IN NS xdays.root.net.
    xdays.root.net. 3600000 IN A 192.168.110.100
    info. 518400 IN NS ns.info.
    ns.info. 3600000 IN A 192.168.110.101
    com. 518400 IN NS ns.com.
    ns.com. 3600000 IN A 192.168.110.101

### info

named.conf如下：

    //
    // named.conf
    //
    // Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
    // server as a caching only nameserver (as a localhost DNS resolver only).
    //
    // See /usr/share/doc/bind*/sample/ for example named configuration files.
    //


    options {
     listen-on port 53 { any; };
     //listen-on-v6 port 53 { ::1; };
     directory  "/var/named";
     dump-file  "/var/named/data/cache_dump.db";
            statistics-file "/var/named/data/named_stats.txt";
            memstatistics-file "/var/named/data/named_mem_stats.txt";
     allow-query     { any; };
     recursion yes;


     //dnssec-enable yes;
     //dnssec-validation yes;
     dnssec-enable no;
     dnssec-validation no;
     dnssec-lookaside auto;


     /* Path to ISC DLV key */
     bindkeys-file "/etc/named.iscdlv.key";


     managed-keys-directory "/var/named/dynamic";
    };


    logging {
            channel default_debug {
                    file "data/named.run";
                    severity dynamic;
            };
    };


    zone "." IN {
     type hint;
     file "named.ca";
    };


    zone "info." IN {
     type master;
     file "info.zone";
    };


    zone "com." IN {
     type master;
     file "com.zone";
    };


    include "/etc/named.rfc1912.zones";
    include "/etc/named.root.key";

named.ca如下：

    . 518400 IN NS xdays.root.net.
    xdays.root.net. 3600000 IN A 192.168.110.100

info.zone如下：

    $TTL 86400
    @ IN SOA @ root (
     42 ; serial (d. adams)
     3H ; refresh
     15M ; retry
     1W ; expiry
     1D ) ; minimum


    info. 518400 IN NS ns.info.
    ns.info. 3600000 IN A 192.168.110.101
    xdays.me. 518400 IN NS ns.xdays.me.
    ns.xdays.me. 3600000 IN A 192.168.110.102

### xdays.me

named.conf如下：

    //
    // named.conf
    //
    // Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
    // server as a caching only nameserver (as a localhost DNS resolver only).
    //
    // See /usr/share/doc/bind*/sample/ for example named configuration files.
    //


    options {
     listen-on port 53 { any; };
     //listen-on-v6 port 53 { ::1; };
     directory  "/var/named";
     dump-file  "/var/named/data/cache_dump.db";
            statistics-file "/var/named/data/named_stats.txt";
            memstatistics-file "/var/named/data/named_mem_stats.txt";
     allow-query     { any; };
     recursion yes;


     //dnssec-enable yes;
     //dnssec-validation yes;
     dnssec-enable no;
     dnssec-validation no;
     dnssec-lookaside auto;


     /* Path to ISC DLV key */
     bindkeys-file "/etc/named.iscdlv.key";


     managed-keys-directory "/var/named/dynamic";
    };


    logging {
            channel default_debug {
                    file "data/named.run";
                    severity dynamic;
            };
    };


    zone "." IN {
     type hint;
     file "named.ca";
    };


    zone "xdays.me." IN {
     type master;
     file "xdays.me.zone";
    };


    zone "xdays.com." IN {
     type master;
     file "xdays.com.zone";
    };


    include "/etc/named.rfc1912.zones";
    include "/etc/named.root.key";

named.ca如下：

    . 518400 IN NS xdays.root.net.
    xdays.root.net. 3600000 IN A 192.168.110.100

xdays.me.zone如下：

    $TTL 86400
    @ IN SOA @ root (
     42 ; serial (d. adams)
     3H ; refresh
     15M ; retry
     1W ; expiry
     1D ) ; minimum


    xdays.me. 86400 IN NS ns.xdays.me.
    ns.xdays.me. 360 IN A 192.168.110.101
    www.xdays.me. 360 IN A 1.1.1.1
    img.xdays.me. 360 IN A 2.2.2.2

### cache-only

named.conf如下：

    //
    // named.conf
    //
    // Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
    // server as a caching only nameserver (as a localhost DNS resolver only).
    //
    // See /usr/share/doc/bind*/sample/ for example named configuration files.
    //


    options {
     listen-on port 53 { any; };
     listen-on-v6 port 53 { ::1; };
     directory  "/var/named";
     dump-file  "/var/named/data/cache_dump.db";
            statistics-file "/var/named/data/named_stats.txt";
            memstatistics-file "/var/named/data/named_mem_stats.txt";
     allow-query     { any; };
     recursion yes;


     //dnssec-enable yes;
     //dnssec-validation yes;
     dnssec-enable no;
     dnssec-validation no;
     dnssec-lookaside auto;


     /* Path to ISC DLV key */
     bindkeys-file "/etc/named.iscdlv.key";


     managed-keys-directory "/var/named/dynamic";
    };


    logging {
            channel default_debug {
                    file "data/named.run";
                    severity dynamic;
            };
    };


    zone "." IN {
     type hint;
     file "named.ca";
    };


    include "/etc/named.rfc1912.zones";
    include "/etc/named.root.key";

named.ca如下：

    . 518400 IN NS xdays.root.net.
    xdays.root.net. 3600000 IN A 192.168.110.100

抓包信息
--------

### 标准域名解析

执行dig www.xdays.me，数据包如下： ![DNS A
Record](/wp-content/uploads/2013/10/dns-a.png)

### 带CNAME域名解析

执行dig img.xdays.me，数据包如下： ![DNS
A-CNAME](/wp-content/uploads/2013/10/dns-cname.png)
注意一点，如果img.xdays.me的CNAME记录是img.xdays.com，而且这里俩域的授权是同一台，那么授权会把CNAME记录和A记录同时返回给本地域名解析服务器，数据包如下：
![DNS A-CNAME
detail](/wp-content/uploads/2013/10/dns-cname-detail.png)

注意：这里有个疑问尚未解决，在CNAME和A记录同时被返回之后，本地域名服务器又对img.xdays.com进行了一次递归解析，我不知道意义何在，如有结论请指教。经过请教这个过程称为**DNS重查**，也就是说即使你直接给我了CNAME和A记录，但是我无法验证你到底是不是xdays.com的授权，所以我要递归解析查询一次。

参考链接
========

-   [BIND 9 Administrator Reference
    Manual](http://www.oit.uci.edu/dcslib/bind/bind-9.2.1/Bv9ARM.html)
-   [Pro DNS and BIND](http://www.netwidget.net/books/apress/dns/)
