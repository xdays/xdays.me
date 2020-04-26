---
title: Centos5搭建Exmail邮件系统
date: 2011-08-02
author: admin
category: server
tags: ['email']
slug: centos5搭建exmail邮件系统
---

### 邮件系统运行原理

#### [![mail-architecture](/wp-content/uploads/2011/08/mail-architecture.gif 'mail-architecture')](/wp-content/uploads/2011/08/mail-architecture.gif)

#### MUA，MTA 和 MDA

MUA 叫邮件用户代理，是客户端软件负责与用户交互，接受用户指令；MTA 是邮件传输代理，负责判断邮件取向，如果目的地是自己就直接交给 MDA 处理，如果是其他 MTA 则用 SMTP 转发邮件；MDA 是邮件投递代理，负责将目的地是本机的邮件投放到相应用户的邮箱中，将不是本机的邮件通过 MTA 发送给其他的主机，在这个过程中可以执行邮件过滤和自动回复等操作。

#### 传送流程

1.  用户写明邮件发件人 A 和收件人 B，标题以及正文内容点发送，邮件便发送到 A 自己的 MTA 上，进入 MTA 的队列中
2.  如果邮件收件人 B 属于用户自己的 MTA 则直接通过 MDA 投放到收件人 B 相应的邮箱里去
3.  如果是收件人 B 属于其他的 MTA，则发件人 A 的 MTA 开始转发（relay）流程，通过 SMTP 发送给下一台 MTA，当然这个过程需要经过下一台 MTA 的许可（通过 IP 地址限制）或者认证（用户名密码）
4.  最后收件人的 MTA 收到邮件后，通过 MDA 放到收件人的邮箱里，等待收件人查看和下载

### Extmail 简介

Extmail 是一套基于开源软件的邮件系统解决方案。其主要特点有支持 STMP 和 POP 统一用数据库认证及 ESTMP，支持 1G 大邮件，web 界面，病毒过滤和内容过滤，图形化日志分析，spam 过滤，别名和多域等特点，目前应用广泛。

### Extmail 系统结构

---

功能模块 功能模块 2 功能模块 2
操作系统（OS） CentOS 5.3 CentOS 和 RHEL 是一样的，而且升级免费
Web 服务器 Apache 2.2.x CentOS 自带
数据库/目录服务 MySQL 5.0.X CentO 自带
邮件传输代理（MTA） postfix-2.6.2 使用最新版本 2.6.2
邮件投递代理（MDA） maildrop 2.0.x 支持过滤和强大功能
Web 帐户管理后台 ExtMan 1.0 支持无限域名、无限用户
WebMail 系统 ExtMail 1.1.0 支持多语言、全部模板化，功能基本齐全
日志分析及显示 mailgraph_ext ExtMan 中已经包含了
其他数据认证库 Courier Authlb 0.62 负责 courier-imap,maildrop 的认证
SMTP 认证库 Cyrus SASL 2.1.x 标准的 SASL 实现库，可以支持 Courier authlib
内容过滤器 Amavisd-new 2.6.4 Content-Filter 软件，支持与 Camav/SA 的挂接
内容级别的反垃圾邮件工具 SpamAssassin-3.2.5 著名的 SA，可以支持大量规则
防病毒软件（Anti-Virus） ClamAV 0.95.2 最热门的开源杀毒软件
SMTP 阶段反垃圾邮件工具 Spam Locker 0.99 基于 SMTP 行为识别的 Antispam 软件，大量可选插件
高效的反垃圾邮件工具 Dspam-3.8 高精确度的、智能的过滤功能

---

注意：ExtMail 很好的实现了统一认证，SMTP 认证和 POP 认证统一通过 Courier-Authlib 提供的 authdaemon 认证，只是 STMP 需要透过 cyrus-sasl 连接到 authdaemon 来认证。

### Extmail 安装配置

#### EMOS 安装盘

EMOS 是继承了 Extmail 的 centos 系统安装盘，安装后有命令行的图形界面的配置向导，默认点回车就可以，但是不利于理解 Extmail 的运行机制。

参考链接：http://linzhibin824.blog.163.com/blog/static/7355771020103515222334/

#### 手工 yum 方式安装

官方给的 wiki 里有详细的配置方法，唯一需要注意的细心配置，可能落下一条命令整个系统就无法跑起来，所以要细心细心在细心！！

官方文档：<http://wiki.extmail.org/extmail_solution_for_linux_centos-5>
