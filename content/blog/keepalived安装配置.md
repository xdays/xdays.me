---
title: Keepalived安装配置
date: 2015-10-18
author: admin
category: server
tags: server, keepalived
slug: keepalived安装配置
---


# 简介

Keepalived是Linux的高可用软件，其主要是高可用协议的VRRP的开元实现，此外它还提供了方便管理LVS的接口。 
 
# 安装

    wget http://www.keepalived.org/software/keepalived-1.2.7.tar.gz && tar xzf keepalived-1.2.7.tar.gz && cd keepalived-1.2.7 && ./configure --prefix=/usr/local/keepalived-1.2.7 && make &&     make install && cd /usr/local && ln -s keepalived-1.2.7 keepalived

# 配置
```
mv keepalived.conf{,.default}
vim keepalived.conf
global_defs {
   notification_email {
      test@example.com
   }
   notification_email_from noreply@example.com
   smtp_server 127.0.0.1
   smtp_connect_timeout 30
   router_id minissr
}

vrrp_script chk_nginx {
   script "if [ -f /var/run/down -o `ps U root -Ho cmd | grep -v grep | grep nginx | wc -l` -eq 0 ]; then exit 1; else exit 0; fi"
   interval 2  # check every 2 seconds
   weight -40   # if failed, decrease 40 of the priority
   fall   1     # require 1 failures for failures
   rise   1     # require 1 sucesses for ok
}

vrrp_instance nginx {
    state MASTER
    #state BACKUP
    interface eth0
    virtual_router_id 51
    priority 102
    #priority 101
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    track_script {
       chk_nginx
    }
    virtual_ipaddress {
       192.168.110.110
    }
}
```

# 启动
    /usr/local/keepalived/sbin/keepalived -f /usr/local/keepalived/etc/keepalived/keepalived.conf -D
