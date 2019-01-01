---
title: Consul基础
date: 2016-02-24
author: admin
category: database
tags: nosql, consul
slug: Consul基础
---
 
 
# 简介

* 服务发现，提供了DNS和HTTP两种接口
* 健康检查，可针对服务和节点两个级别检查
* KV存储，提供HTTP接口
* 多数据中心支持

# 基础

## 概览

![architect-of-consul](/wp-content/uploads/2016/02/consul-arch.png)

* 通过一个WAN的Gossip池来原生支持跨数据中心的状态同步
* 一个数据中心内部通过LAN Gossip来维持数据中心内部状态同步
* 一个数据中心内部通过Raft协议来维护在Server模式的agent之间的leader选举和同步数据
* Client模式下的agent负责转发RPC请求给Server模式的agent
* 所有的agent都负责做健康检查

## Raft

Raft一致性算法是Consul的核心，用于在一个数据中心内部的Server之间同步数据，关于Raft算法[这里](http://thesecretlivesofdata.com/raft)有个非常直观的演示。

## Gossip

Gossip分布式通信协议是Consul的另一个核心，用于管理成员和广播消息。

## Agent

Consul要在集群的所有的节点上部署一个agent，可以工作在client或者server模式。client模式agent主要职责是做健康检查，对外提供HTTP和DNS接口以及同步数据，以及向server模式的agent转发请求；server模式的agent额外的需要维护集群的状态跨数据中心通信等。

# 安装

consul仅有一个二进制文件，开箱即用。 从[这里](https://www.consul.io/downloads.html)下载。

# 启动

## 启动Server模式的agent

    consul agent -server -bootstrap-expect 1 -data-dir /tmp/consul -ui-dir /tmp/dist -client=0.0.0.0

注意： `--ui-dir` 启动了Consul的web-ui, 该参数是可选的。

## 启动Client模式的agent

    consul agent -data-dir=/tmp/consul

## 加入集群

    consul join peer-ip

# 安全

0.4之后的版本开始支持ACL控制，控制对象包括kv和service，这里我们给出初始的ACL配置config.json：

```
{
  "acl_datacenter": "dc1",
  "acl_master_token": "changeme",
  "acl_token": "ttSsL3mx3k9vqd5OzXgD",
  "acl_default_policy": "deny"
}
```

启动的时候添加 `-config-file=config.json` 即可

# 其他

Consul的systemd配置文件

```
[Unit]
Description=consul agent
Requires=network-online.target
After=network-online.target
[Service]
EnvironmentFile=-/etc/sysconfig/consul
Environment=GOMAXPROCS=2
Restart=on-failure
ExecStart=/usr/local/sbin/consul agent $OPTIONS
ExecReload=/bin/kill -HUP $MAINPID
KillSignal=SIGINT
[Install]
WantedBy=multi-user.target
```
