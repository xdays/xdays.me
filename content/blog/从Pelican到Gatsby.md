---
title: 从Pelican到Gatsby
date: 2019-01-03
author: admin
category: devops
tags: ['blog', 'pelican', 'gatsby']
slug: 从Pelican到Gatsby
---

最近一直在关注 React 生态，本着更好的学习 React 的目的和新年新气象重新开起写博客的计划，把博客从 Pelican 迁移到了 Gatsby，接下来记录下整个迁移过程。

## 初始化

```
npm i -g gatsby-cli
gatsby new blog https://github.com/gatsbyjs/gatsby-starter-blog
cd blog
gatsby develop
```

## 模板

首先 Gatsby 的模板机制并不像其他的静态网站生成器那样可插拔，官方叫 starters，你可以基于这些 starters 构建自己的模板，或者说这些 starters 还比较简单，虽然可以开箱即用但是不够完善。这里我用的 [gatsby-starter-blog](https://github.com/gatsbyjs/gatsby-starter-blog), 这个 starter 只有索引页和博客内容页，不过这倒挺符合我目前的想法，过去的几年里我一直做加法，以后要开始做减法了。

## 迁移源码

由于之前 pelican 也是用 markdown 写的，所以迁移起来不算麻烦，我写了一个脚本来转换：

    python gatsby-migrate.py '/path/to/src.md' content/blog/

## 静态资源

因为我的图片都是早年间从 wordpress 里迁移过来的，所以都是集中放到一个目录下的，现在只需要把 wp-content 放到 static 目录下即可

## 持续集成

这里我做了两条持续集成的 pipeline(固有的运维思维，什么事情都想着有个备份)，一条是 gitlab 的 CI，另一条是 netlify 平台

先说 Gitlab，也比较简单，因为之前我有一个 [xdays.gitlab.io](https://gitlab.com/xdays/xdays.gitlab.io), 这次只需要修改 `.gitlab-ci.yml` :

```
image: node:8.11.2-alpine
pages:
  script:
  - npm i -g gatsby-cli
  - npm i
  - gatsby build
  artifacts:
    paths:
    - public/
```

即可，然后每次推送新的 commit，我就可以在这里 https://xdays.gitlab.io 访问我的新博客了。

再说 Netlify，这个本来主打静态网站托管的 SaaS 服务，现在又集成了 Severless 的一些服务，使用起来确实很方便：

1. Github 账号登陆
2. 添加个人仓库，Netlify 自动识别 Gatsby 项目
3. 添加自定义域名，将域名解析指向到 Netlify 给的 CNAME。
