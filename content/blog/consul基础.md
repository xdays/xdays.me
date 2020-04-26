---
title: Consul基础
date: 2016-02-24
author: admin
category: database
tags: ['kv']
slug: Consul基础
---

# 简介

- 服务发现，提供了 DNS 和 HTTP 两种接口
- 健康检查，可针对服务和节点两个级别检查
- KV 存储，提供 HTTP 接口
- 多数据中心支持

# 基础

## 概览

![architect-of-consul](/wp-content/uploads/2016/02/consul-arch.png)

- 通过一个 WAN 的 Gossip 池来原生支持跨数据中心的状态同步
- 一个数据中心内部通过 LAN Gossip 来维持数据中心内部状态同步
- 一个数据中心内部通过 Raft 协议来维护在 Server 模式的 agent 之间的 leader 选举和同步数据
- Client 模式下的 agent 负责转发 RPC 请求给 Server 模式的 agent
- 所有的 agent 都负责做健康检查

## Raft

Raft 一致性算法是 Consul 的核心，用于在一个数据中心内部的 Server 之间同步数据，关于 Raft 算法[这里](http://thesecretlivesofdata.com/raft)有个非常直观的演示。

## Gossip

Gossip 分布式通信协议是 Consul 的另一个核心，用于管理成员和广播消息。

## Agent

Consul 要在集群的所有的节点上部署一个 agent，可以工作在 client 或者 server 模式。client 模式 agent 主要职责是做健康检查，对外提供 HTTP 和 DNS 接口以及同步数据，以及向 server 模式的 agent 转发请求；server 模式的 agent 额外的需要维护集群的状态跨数据中心通信等。

# 安装

consul 仅有一个二进制文件，开箱即用。 从[这里](https://www.consul.io/downloads.html)下载。

# 启动

## 启动 Server 模式的 agent

    consul agent -server -bootstrap-expect 1 -data-dir /tmp/consul -ui-dir /tmp/dist -client=0.0.0.0

注意： `--ui-dir` 启动了 Consul 的 web-ui, 该参数是可选的。

## 启动 Client 模式的 agent

    consul agent -data-dir=/tmp/consul

## 加入集群

    consul join peer-ip

# 安全

0.4 之后的版本开始支持 ACL 控制，控制对象包括 kv 和 service，这里我们给出初始的 ACL 配置 config.json：

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

Consul 的 systemd 配置文件

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
