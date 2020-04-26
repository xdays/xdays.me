---
title: Bind基于DLZ实现智能DNS
date: 2015-01-11
author: admin
category: server
tags: ['dns', 'bind', 'server']
slug: Bind基于DLZ实现智能DNS
---

# 简介

在我看来基于 Bind 的只能 DNS 方案主要包括两个部分：Geolocation 和 Dynamic Record。国内的业界对智能 DNS 的定位也无非这两点，但是我所理解的智能 DNS 是建立在这两条基础上的智能调度系统，比如我有三个负载能力不同的数据中心，DNS 可以根据数据中心的 metrics（这里可能包括带宽，服务能力等）实现流量的调度，限于个人水平个人未在这个方向有所实践，这个话题留作以后讨论，所以本文只针对前两个问题。由于 Bind 本身的配置可运维性比较差，这就引出本文主要讨论的 DLZ。

# 原理

DLZ 实际上就是扩展了 Bind，将 Zonefle 的内容放到外部数据库里，然后给 Bind 配置查询语句从数据库里查询记录。当修改数据库里的记录信息的时候，无需重启 Bind，下次客户请求时直接就能返回新的记录了。另外，DLZ 本身不支持缓存，所以需要自己根据实际情况解决查询的问题。

# 安装

**注意：** 这里我以 CentOS7 上安装 dlz-mysql 模块为例。

## 安装依赖

```
yum install mariadb-devel gcc wget patch make
```

## 下载源码

Bind9.8 之前的版本需要打 patch，具体可参考 DLZ 官方文档，Bind9.8 之后（包括 9.8）的版本已经集成 DLZ：

```
wget ftp://ftp.isc.org/isc/bind9/9.10.1/bind-9.10.1.tar.gz
tar xzf bind-9.10.1.tar.gz
cd  bind-9.10.1
```

## 配置

由于 CentOS7 目录结构上的变更，在编译 dlz-mysql 时会找不到库文件或者 head 文件，所以要做个软连接：

```
ln -s /usr/lib/mysql /usr/lib64/mysql
./configure --prefix /opt/bind --with-dlz-filesystem --with-dlz-mysql
```

## 编译

    make

## 安装

    make install

# 模型

**注意：** DLZ 没有限制用户的数据模型，你可以根据业务逻辑定义模型，然后构造自己的查询语句即可。官方给出了建议的模型。

## 建模

| Field       | Type       | Null | Key | Default | Extra |
| ----------- | ---------- | ---- | --- | ------- | ----- |
| zone        | text       | YES  |     | NULL    |       |
| host        | text       | YES  |     | NULL    |       |
| type        | text       | YES  |     | NULL    |       |
| data        | text       |      |     |         |       |
| ttl         | int(11)    | YES  |     | NULL    |       |
| mx_priority | text       | YES  |     | NULL    |       |
| refresh     | int(11)    | YES  |     | NULL    |       |
| retry       | int(11)    | YES  |     | NULL    |       |
| expire      | int(11)    | YES  |     | NULL    |       |
| minimum     | int(11)    | YES  |     | NULL    |       |
| serial      | bigint(20) | YES  |     | NULL    |       |
| resp_person | text       | YES  |     | NULL    |       |
| primary_ns  | text       | YES  |     | NULL    |       |

- zone 区域
- host 记录名
- type 记录类型
- data 记录值
- ttl 缓存时间
- mx_priority mx 记录优先级
- refresh SOA 记录的刷新时间
- retry SOA 记录的重试时间
- expire SOA 记录的过期时间
- minimum SOA 记录的 minimum
- serial SOA 记录的序列号
- resp_person SOA 记录的序列号
- primary_ns <尚不明确这个字段的意义>

## 建库建表

新建数据库：

```
create database demo;
```

新建 record 表：

```
CREATE TABLE IF NOT EXISTS `records` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `zone` varchar(255) NOT NULL,
  `host` varchar(255) NOT NULL,
  `type` enum('A','MX','CNAME','NS','SOA','PTR','TXT','AAAA','SVR','URL') NOT NULL,
  `data` varchar(255) NOT NULL,
  `ttl` int(11) NOT NULL,
  `mx_priority` int(11) DEFAULT NULL,
  `refresh` int(11) DEFAULT NULL,
  `retry` int(11) DEFAULT NULL,
  `expire` int(11) DEFAULT NULL,
  `minimum` int(11) DEFAULT NULL,
  `serial` bigint(20) DEFAULT NULL,
  `resp_person` varchar(64) DEFAULT NULL,
  `primary_ns` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `type` (`type`),
  KEY `host` (`host`),
  KEY `zone` (`zone`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;
```

新建 acl 表：

```
CREATE TABLE IF NOT EXISTS `acl` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `zone` varchar(255) NOT NULL,
  `client` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `client` (`client`),
  KEY `zone` (`zone`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;
```

# 配置

## GeoIP

这块目前还没有那么灵活，基本上都是基于 acl 来实现的。虽然最新版的 bind 9.10 支持 maxmind 的 api 来做 Geo，但还是改写配置文件的方式。下面是一个示例：

```
acl "US" {
     3.0.0.0/8;
     4.0.0.0/25;
     4.0.0.128/26;
     4.0.0.192/28;
     4.0.0.208/29;
     4.0.0.216/30;
     4.0.0.220/31;
};

view "north_america" {
      match-clients { US; CA; MX; };
      recursion no;
      zone "foos.com" {
            type master;
            file "pri/foos-north-america.db";
      };
};

view "other" {
      match-clients { any; };
      recursion no;
      zone "foos.com" {
            type master;
            file "pri/foos-other.db";
      };
};
```

该示例引用自[这里](http://www.ip2location.com/tutorials/simple-geodns-using-bind-and-ip2location)

但是我们可以通过 DLZ 实现 GeoIP，二次开发一个自己的 driver，然后在 driver 里根据 client ip，结合自己的业务系统实现真正的 Geo 以及智能业务调度。

## Dynamic Record

DLZ 新定义了一个配置关键字 dlz，完整的配置项参考官方文档，这里给出简要说明：

```
dlz "Mysql zone" { //定义DLZ标识
   database "mysql //database为dlz这个block唯一可指定的关键字，mysql表示使用mysql driver
   {host=localhost dbname=dns_data ssl=tRue} //连接数据库的信息
   {select zone from dns_records where zone = '$zone$'} //用于findzone调用，查询zone
   {select ttl, type, mx_priority, case when lower(type)='txt' then concat('\"', data, '\"')
        else data end from dns_records where zone = '$zone$' and host = '$record$'
        and not (type = 'SOA' or type = 'NS')} //用于lookup调用，查询record
   {select ttl, type, mx_priority, data, resp_person, serial, refresh, retry, expire, minimum
        from dns_records where zone = '$zone$' and (type = 'SOA' or type='NS')} //用于authority调用，查询SOA或者NS记录，注意这个配置是可选的，SOA和NS查询可以放到lookup调用里，具体见后文
   {select ttl, type, host, mx_priority, data, resp_person, serial, refresh, retry, expire,
        minimum from dns_records where zone = '$zone$' and not (type = 'SOA' or type = 'NS')} //用于allnode调用，和接下来的allowzonexfr一起来提供AXFR查询，可选的配置项
   {select zone from xfr_table where zone = '$zone$' and client = '$client$'} //用于allowzonexfr()调用，用于查询客户端是否可发起AXFR查询，可选的配置项
   {update data_count set count = count + 1 where zone ='$zone$'}";
};
```

**注意：** 此配置为最新 Bind 版本的配置，如果是打 patch 的版本请将`$`换成`%`，以下的配置同样。

这里也给出我的配置：

```
logging {
    channel all {
        file "/opt/bind/log/named.log" versions 1;
        print-time yes;
        severity dynamic;
        print-category yes;
        print-severity yes;
    };

    category default { all; };
    category queries { all; };

};

options {
    directory "/opt/bind/var/";
    listen-on-v6 { none; };
    listen-on { any; };
    pid-file "/var/run/named.pid";
    recursion yes;
    allow-transfer {127.0.0.1;};
};

dlz "mysql-dlz" {
    database "mysql
    {host=localhost dbname=demo ssl=false port=3306 user=root pass=thinkin}
    {select zone from records where zone = '$zone$' limit 1}
    {select ttl, type, mx_priority, case when lower(type)='txt' then concat('\"', data, '\"') when lower(type) = 'soa' then concat_ws(' ', data, resp_person, serial, refresh, retry, expire, minimum) else data end from records where zone = '$zone$' and host = '$record$'}
    {}
    {select ttl, type, host, mx_priority, data from records where zone = '$zone$' and not (type = 'SOA' or type = 'NS')}
    {select zone from acl where zone = '$zone$' and client = '$client$'}";
};

zone "." IN {
    type hint;
    file "named.root";
};

key "rndc-key" {
    algorithm hmac-md5;
        secret "OdEg+tCn/bMe+/2vbJgQvQ==";
};

controls {
        inet 127.0.0.1 allow { localhost; } keys { "rndc-key"; };
};
```

**注意：** 这里的配置开启了递归解析且支持本机发起的 AXFR 请求。

## 根 zonefile

```
wget -SO /opt/bind/var/named.root http://www.internic.net/domain/named.root
```

# 启动

```
/opt/bind/sbin/named -n1 -c /opt/bind/etc/named.conf -d9 -g
```

# 测试

## 导入数据

导入 records 数据：

```
INSERT INTO demo.records (zone, host, type, data, ttl) VALUES ('xdays.me', 'www', 'A', '1.1.1.1', '60');
INSERT INTO demo.records (zone, host, type, data, ttl) VALUES ('xdays.me', 'cloud', 'A', '2.2.2.2', '60');
INSERT INTO demo.records (zone, host, type, data, ttl) VALUES ('xdays.me', 'ns', 'A', '3.3.3.3', '60');
INSERT INTO demo.records (zone, host, type, data, ttl) VALUES ('xdays.me', 'blog', 'CNAME', 'cloud.xdays.me.', '60');
INSERT INTO demo.records (zone, host, type, data, ttl) VALUES ('xdays.me', '@', 'NS', 'ns.xdays.me.', '60');
INSERT INTO demo.records (zone, host, type,  ttl, data,refresh, retry, expire, minimum, serial, resp_person) VALUES ('xdays.me', '@', 'SOA', '60', 'ns', '28800', '14400', '86400', '86400', '2012020809', 'admin');
```

导入 acl 数据：

```
INSERT INTO demo.acl (zone, client) VALUES ('xdays.me', '127.0.0.1');
```

## 测试记录

```
dig @127.0.0.1 www.xdays.me a
dig @127.0.0.1 blog.xdays.me a
dig @127.0.0.1 blog.xdays.me cname
dig @127.0.0.1 xdays.me ns
dig @127.0.0.1 www.xdays.me axfr
```

#参考

- 配置指令参考 [DLZ 官方文档](http://bind-dlz.sourceforge.net/mysql_driver.html)
- 安装文档参考 [这篇](http://www.vfeelit.com/610.html)
- Bind 的 GeoIP 支持参考 [这篇](https://kb.isc.org/article/AA-01149/0/Using-the-GeoIP-Features-in-BIND-9.10.html)
