---
title: 基于GitLab的Pages服务构建静态博客
date: 2016-11-04
author: admin
category: devops
tags: ['blog', 'pelican']
slug: 基于GitLab的Pages服务构建静态博客
---

# 背景

之前我有[一篇博客](//Pelican和Github构建静态博客/)讨论过基于 Pelican, Github 以及 Nginx+Lua 实现的自动发布静态博客。最近重新思考这个方案感觉不够精简，也许当时是出于学习的目的引入了 Ngnix+Lua 这块。正好今年上半年[GitLab 宣布支持 Pages 服务](https://about.gitlab.com/2016/04/07/gitlab-pages-setup/)了，而且支持的远比 Github 彻底，所以决定将我的博客托管在 GitLab 的 Pages 上。

# 流程

本地只需要往 Git 仓库里添加或者编辑 markdown 文件，当源文件被 push 到 Gitlab 服务端，触发 GitLab 的 Pipeline，Pipeline 完成由 markdown 源码到 html 文件的构建，最后由 GitLab 的 Pages 服务来托管 html 文件。

# 配置

## 迁移仓库

在 GitLab 上新建一个仓库，按照规范我这里将其命名为 `xdays.gitlab.io` ，然后将 Github 上的源码 pull 下来推到 GitLab 上：

```
git clone git@github.com:xdays/xdays.me.git
git remote add gitlab git@gitlab.com:xdays/xdays.gitlab.io.git
git push gitlab master
```

## 添加 gitlab-ci.yml

由于 Pipeline 是由仓库根目录下的 `.gitlab-ci.yml` 驱动的，我们需要往仓库里添加一个 yml 文件，内容如下：

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

注意： 按照 GitLab 的规范，输出目录的名字必须是 public，否则 deploy 会失败。

这样当再次 push 源文件到 GitLab 时就会触发 Pipeline 了，例如这是一次[成功的 Build](https://gitlab.com/xdays/xdays.gitlab.io/pipelines/4867226)

如果 Build 成功，我们就可以通过 http://xdays.gitlab.io/ 访问静态博客了。

## 添加自定义域名

接下来要在这个页面下 https://gitlab.com/xdays/xdays.gitlab.io/pages 添加自定义域名，以便通过 http://xdays.me 来访问我的博客。你甚至可以上传证书来让 GitLab 支持 https。

然后在域名服务商那里将添加 CNAME 记录 `xdays.me` 解析到 `xdays.gitlab.io` 。

# 其他

## CDN

由于 GitLab 在国外，国内访问较慢，所以我再源站前加上了[CloudFlare](https://www.cloudflare.com/)这一 CDN 服务，具体步骤不在这里介绍了。

## Mirror

虽然我将 Git 仓库从 Github 迁移到了 GitLab，但是 Github 有很强的社交氛围，所以还想做一个从 GitLab 到 Github 的 mirror，目前还没有发现好的解决办法，暂时用 Git 的 hook 来实现。编辑仓库目录下的 `.git/hooks/pre-push`

```
#!/bin/bash

exec git push github -f --mirror
```

这样每次 push 到 GitLab 时也会 push 到 Github 一份。

# 参考

- http://pages.gitlab.io/
- https://gitlab.com/pages/pelican
