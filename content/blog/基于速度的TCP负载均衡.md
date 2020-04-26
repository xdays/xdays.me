---
title: 基于速度的TCP负载均衡
date: 2019-09-17
author: admin
category: network
tags: ['v2ray', 'ssr', 'openresty']
slug: 基于速度的TCP负载均衡
---

# 需求

基于订阅的科学上网工具方便之处在于可以随意切换节点，这时候我就想能不能用负载均衡软件来作为正向代理帮助这些工具自动选择最优的上层节点呢，先列下需求:

1. 支持订阅
2. 能自动屏蔽掉不可用的节点
3. 根据建连时间和响应速度来选择最优的节点

# 实现

比较流行的负载均衡软件有 nginx，haproxy 和 apache，调研了这三个项目后，我只在 nginx 的商业版 nginx plus 里发现了[least_time](http://nginx.org/en/docs/stream/ngx_stream_upstream_module.html#least_time)可以按照最小响应时间来调度。

这样，只能自己造轮子了，首选的方案当然是[OpenResty](https://openresty.org/en/)，一下是我用到 OpenResty 相关的功能：

1. `lua-resty-http` 这个是用来发 http 请求的，获取订阅节点
2. `lua_shared_dict` 用来存储元数据和统计数据的，注意由于 `nginx.shared.DICT` 的限制怎么用其提供的 key/value 来组织数据需要好好想想了，我的设计是通过增加额外的 key 来避免序列化
3. `ngx.balancer` 这个是本项目的核心，它可以在请求级别控制 nginx 对 upstream server 的选择，挑战主要是你需要自己实现调度逻辑

再说下整个项目的大体逻辑:

1. 定时器 `ngx.timer` 会随 worker 启动而初始化，定时器主要是定时从订阅接口获取节点，同时也会删掉不在订阅里的节点
2. 当一个请求到来的时候，因为所有的节点都没有统计数据，不知道哪个节点好，这就开始了一个冷启动的过程，这时候采用随机分发的策略，直到所有的节点都接收到 10 个请求了
3. 当然有些节点可能是不可用的，这里我的做法是 fail fast 逻辑，一旦发现节点不可用，立马丢到黑洞里；可是如果只是这样的话，那这些节点即使将来恢复了也不会被用到，所幸 `ngx.shared.DICT` 支持 `expire_time`，这样过了超时时间，这些不可用的节点对应的 key 就过期了，节点会从订阅里重新被添加进来，这样节点又会走一遍冷启动的逻辑
4. 要实现调度，前提是知道所有节点的统计信息，这一块我用到了 [ngx_stream_upstream_modle 的几个变量](http://nginx.org/en/docs/stream/ngx_stream_upstream_module.html#variables)，`$upstream_bytes_received`，`$upstream_first_byte_time`和`$upstream_session_time`分别代表了从后端获取的流量，首包时间和总时间，基于这些变量，就能统计出来后端节点的平均首包时间和传输速度。
5. 有了统计信息，调度就简单了，只需要根据设定的调度策略选择最优的节点，然后通过 `ngx.balancer` 将请求转发给节点就行了

# 安装配置

[项目地址再这里](https://github.com/xdays/tlb) 其实 readme 里已经交代的挺清楚了

先编辑 `.env` 修改配置：

1. `PANEL_HOST` 是订阅地址
2. `PANEL_TYPE` 是订阅地址的类型，目前只支持 ss 和 v2ray

然后启动就行了

```
docker-compose up -d
```

Enjoy!
