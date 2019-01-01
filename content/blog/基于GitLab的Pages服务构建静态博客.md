---
title: 基于GitLab的Pages服务构建静态博客
date: 2016-11-04
author: admin
category: devops
tags: blog,pelican
slug: 基于GitLab的Pages服务构建静态博客
---

# 背景

之前我有[一篇博客](//Pelican和Github构建静态博客/)讨论过基于Pelican, Github以及Nginx+Lua实现的自动发布静态博客。最近重新思考这个方案感觉不够精简，也许当时是出于学习的目的引入了Ngnix+Lua这块。正好今年上半年[GitLab宣布支持Pages服务](https://about.gitlab.com/2016/04/07/gitlab-pages-setup/)了，而且支持的远比Github彻底，所以决定将我的博客托管在GitLab的Pages上。

# 流程

本地只需要往Git仓库里添加或者编辑markdown文件，当源文件被push到Gitlab服务端，触发GitLab的Pipeline，Pipeline完成由markdown源码到html文件的构建，最后由GitLab的Pages服务来托管html文件。

# 配置

## 迁移仓库

在GitLab上新建一个仓库，按照规范我这里将其命名为 `xdays.gitlab.io` ，然后将Github上的源码pull下来推到GitLab上：

```
git clone git@github.com:xdays/xdays.me.git
git remote add gitlab git@gitlab.com:xdays/xdays.gitlab.io.git
git push gitlab master
```

## 添加gitlab-ci.yml

由于Pipeline是由仓库根目录下的 `.gitlab-ci.yml` 驱动的，我们需要往仓库里添加一个yml文件，内容如下：

```
image: python:2.7-alpine
pages:
  script:
  - apk update && apk add git && git submodule update --init --recursive
  - pip install -r requirements.txt
  - ./genblog.sh
  artifacts:
    paths:
    - public/
```

注意： 按照GitLab的规范，输出目录的名字必须是public，否则deploy会失败。

这样当再次push源文件到GitLab时就会触发Pipeline了，例如这是一次[成功的Build](https://gitlab.com/xdays/xdays.gitlab.io/pipelines/4867226)

如果Build成功，我们就可以通过 http://xdays.gitlab.io/ 访问静态博客了。

## 添加自定义域名

接下来要在这个页面下 https://gitlab.com/xdays/xdays.gitlab.io/pages 添加自定义域名，以便通过 http://xdays.me 来访问我的博客。你甚至可以上传证书来让GitLab支持https。

然后在域名服务商那里将添加CNAME记录 `xdays.me` 解析到 `xdays.gitlab.io` 。

# 其他

## CDN

由于GitLab在国外，国内访问较慢，所以我再源站前加上了[CloudFlare](https://www.cloudflare.com/)这一CDN服务，具体步骤不在这里介绍了。

## Mirror

虽然我将Git仓库从Github迁移到了GitLab，但是Github有很强的社交氛围，所以还想做一个从GitLab到Github的mirror，目前还没有发现好的解决办法，暂时用Git的hook来实现。编辑仓库目录下的 `.git/hooks/pre-push`

```
#!/bin/bash

exec git push github -f --mirror
```

这样每次push到GitLab时也会push到Github一份。

# 参考

* http://pages.gitlab.io/
* https://gitlab.com/pages/pelican
