---
title: etcd基础
date: 2016-03-03
author: admin
category: database
tags: nosql, consul
slug: etcd基础
---
 
 
# 简介

etcd是一个分布式kv存储，与我前面介绍的[Consul](http://xdays.me/Consul基础.html)有些类似，底层都是基于[raft](http://thesecretlivesofdata.com/raft)协议的，它的主要用途包括为应用提供集中的配置管理和服务发现。

# 安装

etcd是go语言开发的，所以安装成本非常低，一般我们用systemd来管理etcd，这里我们简单过下安装过程：

```
curl -L  https://github.com/coreos/etcd/releases/download/v2.2.5/etcd-v2.2.5-linux-amd64.tar.gz -o etcd-v2.2.5-linux-amd64.tar.gz
tar xzvf etcd-v2.2.5-linux-amd64.tar.gz
cd etcd-v2.2.5-linux-amd64
mkdir -p /opt/etcd/bin && cp etcd etcdctl /opt/etcd/bin/
```

然后准备systemd配置文件 `/usr/lib/systemd/system/etcd.service`

```
[Unit]
Description=etcd

[Service]
Type=notify
Restart=always
RestartSec=10s
LimitNOFILE=40000
Environment=ETCD_DATA_DIR=/opt/etcd/default.etcd
Environment=ETCD_NAME=%m
Environment=ETCD_ELECTION_TIMEOUT=1200
Environment="ETCD_LISTEN_PEER_URLS=http://{{host.ip}}:2380,http://{{host.ip}}:7001"
Environment="ETCD_ADVERTISE_CLIENT_URLS=http://{{host.ip}}:2379,http://{{host.ip}}:4001"
Environment="ETCD_LISTEN_CLIENT_URLS=http://0.0.0.0:2379"
ExecStart=/opt/everstring/etcd/bin/etcd

[Install]
WantedBy=multi-user.target
```

注意： 上述配置中 `{{host.ip}}` 要替换成本机从外面可以访问的IP。

然后重新加载systemd配置

    systemctl daemon-reload

# 启动

## 单机模式

对于单机模式，没有需要特殊说明，直接启动etcd即是以单机模式运行：

    systemctl start etcd

然后可以运行客户端命令查看集群状态：

    etcdctl cluster-health

## 集群模式

对于集群模式，我们有几个方面要说下。

1. 架设集群
2. 增删成员


### 架设集群

根据[官方集群文档](https://coreos.com/etcd/docs/latest/clustering.html)的介绍，有两种架设集群的方式：

1. static
2. etcd discovery

官方建议etcd集群的数量是奇数个，这样能保证在网络分割的时候不会选出来两个leader。这里我重点说下Static的方式，只要理解了这种方式 etc discovery就很好理解了。先来看下集群的启动命令：

etcd0
```
etcd --name etcd0 -advertise-client-urls http://192.168.99.101:2379 \
-listen-client-urls http://0.0.0.0:2379 \
-listen-peer-urls http://0.0.0.0:2380 \
-initial-advertise-peer-urls http://192.168.99.101:2380 \
-initial-cluster-token etcd-cluster-1 \
-initial-cluster etcd0=http://192.168.99.101:2380,etcd1=http://192.168.99.102:2380,etcd2=http://192.168.99.103:2380 \
-initial-cluster-state new
```

etcd1
```
etcd --name etcd1 -advertise-client-urls http://192.168.99.102:2379 \
-listen-client-urls http://0.0.0.0:2379 \
-listen-peer-urls http://0.0.0.0:2380 \
-initial-advertise-peer-urls http://192.168.99.102:2380 \
-initial-cluster-token etcd-cluster-1 \
-initial-cluster etcd0=http://192.168.99.101:2380,etcd1=http://192.168.99.102:2380,etcd2=http://192.168.99.103:2380 \
-initial-cluster-state new
```

etcd2
```
etcd --name etcd2 -advertise-client-urls http://192.168.99.103:2379 \
-listen-client-urls http://0.0.0.0:2379 \
-listen-peer-urls http://0.0.0.0:2380 \
-initial-advertise-peer-urls http://192.168.99.103:2380 \
-initial-cluster-token etcd-cluster-1 \
-initial-cluster etcd0=http://192.168.99.101:2380,etcd1=http://192.168.99.102:2380,etcd2=http://192.168.99.103:2380 \
-initial-cluster-state new
```

要让一组etcd实例组成集群：首先要给集群一个标识，由`--initial-cluster-token`指定；然后在启动的时候要让集群里的etcd知道彼此，由`--initial-cluster`指定；此外既然集群的每个成员要接收客户端的连接就要在集群里通告自己提供给客户端连接的endpoint，由`-advertise-client-urls`指定。

但是，static方式架设集群的前提是我们已经知道了集群中所有etcd的ip列表了，如果我们在启动第一个etcd实例的时候还不知道第二个etcd实例的ip的话就要用etcd discovery的方式来动态发现集群中的所有的etcd实例列表。具体示例请参考[官方集群文档](https://coreos.com/etcd/docs/latest/clustering.html)

### 增删成员

这里要指出：

1. 在集群可用的时候，也就是说集群中大多数etcd实例仍然存活的时候，我们可以通过etcdctl来增删成员；
2. 在集群不可用的时候，也就是说离线成员超过半数，但是离线成员的数据依然存在，可以直接重启etcd成员使集群恢复健康状态
3. 在集群不可用的时候，也就是说离线成员超过半数，而且离线成员数据全部丢失，这种情况只能通过离线恢复来重建整个集群，具体可参考[灾难恢复](https://coreos.com/etcd/docs/latest/admin_guide.html#disaster-recovery)

下面我演示下如何增删成员：

新增成员

在现有的集群里增加要加入的节点信息,

    etcdctl -C http://192.168.99.101:2379 member add etcd2 http://192.168.99.103:2380

启动新增的节点

```
etcd --name etcd2 -advertise-client-urls http://192.168.99.103:2379 \
-listen-client-urls http://0.0.0.0:2379 \
-listen-peer-urls http://0.0.0.0:2380 \
-initial-advertise-peer-urls http://192.168.99.103:2380 \
-initial-cluster-token etcd-cluster-1 \
-initial-cluster etcd0=http://192.168.99.101:2380,etcd1=http://192.168.99.102:2380,etcd2=http://192.168.99.103:2380 \
-initial-cluster-state existing
```

删除成员

    etcdctl -C http://192.168.99.101:2379 member remove 9636be876f777946

注意： 如果一个etcd实例从集群中剔除，实例会自动退出，而且不能再加入集群；已删除的etcd实例，只有清空数据后重新按照新增成员的步骤才能重新加入集群。


# 使用

## key的增删改查

```
etcdctl set /key1 value1
etcdctl set --swap-with-value value1 /key1 value2
etcdctl rm /key1
etcdctl update /key1 /value2
etcdctl get /key1
```

## key的watch

    etcdctl mkdir /test
    etcdctl watch --recursive /test

然后在test目录下set一个key就能看到watch的效果

## 常见问题

1.  etcd监听在0.0.0.0，但是etcdctl却无法连接到。这种情况可能因为etcd没有指定 `-advertise-client-urls`  ，然后etcd就会在集群里宣告默认的 127.0.1，这样etcdctl从集群里拿到的就是 127.0.0.1的地址。解决办法是，给etcdctl加 `--no-sync` 参数强制etcdctl不从集群里同步状态，然后通过 `--peers` 直接去连接etcd。
