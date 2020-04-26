---
title: Golang依赖管理
date: 2019-08-17
author: admin
category: golang
tags: ['golang']
slug: Golang依赖管理
---

# 关于 Module

Module 在 1.11 成为官方的依赖管理工具，虽然引起了不小的[关于 Go Module 的争吵](https://zhuanlan.zhihu.com/p/41627929) ,但是应该就是以后主流的依赖管理工具了。

# Module 使用

当前版本 1.12.8 中 go 自动判断是否启用 module 功能，当位于 GOPATH 里时关闭，否则自动开启。

```bash
GO111MODULE=auto
```

新建一个 module

```bash
mkdir example
cd example
go mod init github.com/xdays/example
```

然后你就基本不需要单独跑`go get`来获取依赖了，`go run`和`go build`等命令会根据你的`import`来自动下载依赖并确立依赖的版本，至于怎么确立的可以在跑完命令后参考`go.mod`文件的内容。

再者就是如果你更新了依赖版本，可以通过如下命令来清掉旧版本

```bash
go mod tidy
```

# Module 的管理

对于包管理者来说也可以通过上面的步骤切换到 module 上来，但是当需要更新大版本的时候就需要注意了。官方的原则是：

> "If an old package and a new package have the same import path, the new package must be backwards compatible with the old package.”

简而言之，更新大版本只需要如下几个步骤：

1. 将上一个版本开个分支，比如`v5`，然后打上 tag，继续维护
2. 在 master 分支上开发不兼容的`v6`分支，然后打上对应的 tag
3. 最重要的是更新 module 的 path，在最后添加上大版本的后缀，如果之前是`github.com/xdays/example`，那么更新之后就是`github.com/xdays/example/v6`，所以其实已经是不同的 package 了

更复杂的需求可以参[考官方的 Module 文档](https://github.com/golang/go/wiki/Modules)

## 使用中遇到的问题

## go-redis 代码不兼容问题

### 问题

测试代码在这里[redis-migrate](https://github.com/xdays/go-utils/tree/9455f2e5946e582553b977059903e59f5e1fe4cf)，直接运行代码有问题

```bash
$ go run main.go
./main.go:105:55: cannot use &rangeBy (type *redis.ZRangeBy) as type redis.ZRangeBy in argument to srcClient.cmdable.ZRangeByScoreWithScores
./main.go:110:33: cannot use &z (type *redis.Z) as type redis.Z in argument to dstClient.cmdable.ZAdd
```

但是通过`go get`获取的 redis-migrate 却没有问题

```bash
go get github.com/xdays/go-utils/redis-migrate
redis-migrate                                            <aws:loop-staging>
found 5 keys
start migrating key test3 from scratch
set ttl to -1ns
start migrating key test5 from scratch
set ttl to -1ns
start migrating key test2 from scratch
set ttl to -1ns
start migrating key test1 from scratch
set ttl to -1ns
start migrating key test4 from scratch
set ttl to -1ns
```

### 分析

如果我在开启了 module，这样 import

```go
import "github.com/go-redis/redis"
```

那么 go module 拿到的就是最小的稳定版本，go.mod 里是这样的

```go
github.com/go-redis/redis v6.15.3+incompatible
```

而如果我用传统的方式获取这个 package，那我拿到的就是 master 分支的代码

```bash
go get github.com/go-redis/redis
cd $GOPATH/src/github.com/go-redis/redis
git branch
```

可以看到两种方式拿到的 package 的版本并不一样。

### 解决

把 import 的 package 路径改为

```go
import "github.com/go-redis/redis/v7"
```

然后执行

```bash
go mod tidy
```

再看`go.mod`，已经更新到最新的版本了

```
github.com/go-redis/redis/v7 v7.0.0-beta.2
```

所以如果项目开启了 module，在 import 依赖的时候要去看下依赖的`go.mod`对应的路径，看看是不是有版本声明的后缀。这是[go-redis 的版本声明](https://github.com/go-redis/redis/blob/master/go.mod#L1)
