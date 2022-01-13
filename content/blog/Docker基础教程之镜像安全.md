---
title: Docker基础教程之镜像安全
date: 2017-04-16
author: admin
category: container
tags: ['docker']
slug: docker基础教程之镜像安全
---

上一篇我总结下了[Docker 的镜像构建](//docker基础教程之镜像构建/)，这一篇我来谈下镜像安全。

# 概述

安全一直是一个不出事没人关心等到出事的时候也已经晚了的话题，以我目前的了解成熟的项目基本没有，而且比较知名的就是 Docker Cloud 和 Quay.io 在收费版里集成了安全扫描的功能。本文主要是我以 [A Scan of the Container Vulnerability Scanner Landscape](https://thenewstack.io/draft-vulnerability-scanners/) 这篇文章为线索，实战了其中的 Anchore 和 Clair 两个项目的简单介绍，后续还会持续观察更新。这类工具的共同特点就是静态分析镜像里的内容，找出其中的软件包和对应的版本，然后和从各大 Linux 版本的 CVE 源下载漏洞数据库做匹配，最终判断镜像里的安全漏洞。

# Anchore

项目地址在[这里](https://github.com/anchore/anchore) 。总体来说 anchore 还是比较简陋，其对应的 [SaaS 服务](https://anchore.io/) 也是处于比较初级的阶段，还有待观察。

## 安装配置

```
yum install epel-release && yum install -y python-pip rpm-python dpkg
pip install anchore
anchore feeds sync
```

## 实战演示

```
# 分析本地的镜像
anchore analyze --image ubuntu:latest --imagetype base
# 从分析结果生成报告
anchore gate --image ubuntu:latest
```

报告中会显示哪个包有漏洞，已经漏洞对应的链接。

# Clair

来自 CoreOS 的[Clair](https://github.com/coreos/clair)实现了一个 restful 的服务，同样是周期性的同步各种漏洞源信息，然后客户端可以将镜像传给 Clair，然后 Clair 解析出镜像里的软件包，如果软件包包含漏洞的话， Clair 可以调 webhook 发送通知到外部服务。我的理解 Clair 并不是一个完备的解决方案，但是你可以很容易的将 Clair 集成到自己的工作流中去。可惜这个东西目前还比较小众，目前还看到有人基于这个搞个方案。如下两个链接可以了解更多：

- https://coreos.com/blog/vulnerability-analysis-for-containers.html
- https://coreos.com/clair/docs/latest/api_v1.html

## 安装配置

准备 sample 配置文件

```
mkdir clair/clair_config/
curl -L https://raw.githubusercontent.com/coreos/clair/master/config.example.yaml -o clair/clair_config/config.yaml
```

修改数据库配置 `vi clair/clair_config/config.yaml`

```
source: host=postgres port=5432 user=postgres password=password sslmode=disable statement_timeout=60000
```

准备 compose file

```
cd clair
curl -L https://raw.githubusercontent.com/coreos/clair/master/docker-compose.yml -o docker-compose.yml
```

启动

```
docker-compose up -d
```

## 实战演示

刚才我也提到，Clair 只是提供了 api 接口，所以使用起来并不是那么方便，我在 Github 上找到了 clairctl 这个客户端工具，可以方便的测试 Clair 的功能

### 安装 clairctl

```
go get github.com/jgsqware/clairctl
cd ~/go/src/github.com/jgsqware/clairctl
go build
cp clairctl /usr/local/bin/
```

### 分析镜像

检查是否已经连接上 Clair

```
~ clairctl health

Clair: ✔
```

将镜像上传到 Clair

```
~ clairctl push -l mongo
mongo:latest has been pushed to Clair
```

分析镜像中的漏洞

```
~ clairctl analyze mongo

Image: docker.io/mongo:latest
 11 layers found

  ➜ Analysis [sha256:bb0dc] found 36 vulnerabilities.
  ➜ Analysis [sha256:2369c] found 36 vulnerabilities.
  ➜ Analysis [sha256:ef2c7] found 36 vulnerabilities.
  ➜ Analysis [sha256:9504d] found 36 vulnerabilities.
  ➜ Analysis [sha256:7584b] found 34 vulnerabilities.
  ➜ Analysis [sha256:081d7] found 34 vulnerabilities.
  ➜ Analysis [sha256:b394c] found 34 vulnerabilities.
  ➜ Analysis [sha256:a647e] found 34 vulnerabilities.
  ➜ Analysis [sha256:90df9] found 34 vulnerabilities.
  ➜ Analysis [sha256:b03f9] found 34 vulnerabilities.
  ➜ Analysis [sha256:e45e8] found 34 vulnerabilities.
```

生成漏洞报告

```
~ clairctl report mongo
HTML report at reports/html/analysis-mongo-latest.html
```

![clair report](/wp-content/uploads/2017/04/clair-report.png)

# 其他

## Open Source Solution

- [OpenSCAP/atomic scan](https://developers.redhat.com/blog/2016/05/02/introducing-atomic-scan-container-vulnerability-detection/)

# Commercial Solution

- [Docker Cloud](https://cloud.docker.com/)
- [Quay.io](https://quay.io/)
- [Aqua](https://www.aquasec.com/products/aqua-container-security-platform/)
