---
title: Puppet之API操作
date: 2014-12-31
author: admin
category: devops
tags: ['puppet']
slug: Puppet之API操作
---

# 背景

最近在做一个自动部署实例的项目，大致流程是首先调用 AWS 的 API 来生成实例，然后用 Puppet 来部署相关服务。但是由于 AWS 的 EIP 是可回收的，也就是说新起的实例可能会被分配到一个之前已经使用过 EIP，由于证书名称是根据 EIP 来的，就会导致有对应的证书名称已经在 Puppet 上记录了，这样就会导致 Puppet 这个环节失败。鉴于如此，需要在给实例绑定上 EIP 之后远程清除下 Puppet 上对应的证书，这样就用到了 Puppet 的 API 操作。

# 基础

Puppet 支持 RESTful 的 API：master 端主要涉及 catalog，certificate，report, resource, file, node, status,和 fact；agent 端主要涉及 fact 和 run。关于这些资源的详细操作参考[这里](https://docs.puppetlabs.com/guides/rest_api.html)

关于 API 的另一方面就是安全方面，Puppet 用一个单独的文件（文件名由 rest_authconfig）来配置 API 的 ACL，具体 ACL 的语法如下：

```
path [~] {/path/to/resource|regex}
[environment {list of environments}]
[method {list of methods}]
[auth[enthicated] {yes|no|on|off|any}]
[allow {hostname|certname|*}]
```

- path 为请求的 url
- environment 为环境，如 production
- method 为请求方法，包括 find, search, save 和 destroy
- auth 为是否需要认证，包括 yes, no 和 any(就是都可以)
- allow 为匹配 nodename，2.7.1 之后支持正则
- allow_ip 为匹配 ip 地址或者网段

# 配置

## 服务端

```
path /certificate_status
environment production,stage
auth yes
method find, search, save, destroy
allow *
```

## 客户端

```
curl -s --insecure --cert /var/lib/puppet/ssl/certs/test2.xdays.me.pem --key /var/lib/puppet/ssl/private_keys/test2.xdays.me.pem --cacert /var/lib/puppet/ssl/certs/ca.pem -H "Accept: pson" https://puppet.xdays.me:8140/stage/certificate_statuses/no_key | python -m json.tool
```

```
curl -s --insecure  -X PUT --cert /var/lib/puppet/ssl/certs/test2.xdays.me.pem --key /var/lib/puppet/ssl/private_keys/test2.xdays.me.pem --cacert /var/lib/puppet/ssl/certs/ca.pem -H "Content-Type: text/pson" --data '{"desired_state":"signed"}' https://puppet.xdays.me:8140/stage/certificate_status/test2.xdays.me
```

```
curl -s -X DELETE --insecure --cert /var/lib/puppet/ssl/certs/test2.xdays.me.pem --key /var/lib/puppet/ssl/private_keys/test2.xdays.me.pem --cacert /var/lib/puppet/ssl/certs/ca.pem -H "Accept: pson" https://puppet.xdays.me:8140/stage/certificate_status/test2.xdays.me
"Deleted for test2.xdays.me: Puppet::SSL::Certificate"
```

# 扩展

基于上一小节的 curl 操作，可以用 Python 简单封装一个 Puppet 的 SDK 用于日常操作，目前我发现已经有人做了[这个](https://github.com/daradib/pypuppet)。
