---
title: 利用mailgun搭建私有域名邮箱
date: 2016-08-27
author: admin
category: tool
tags: ['email']
slug: 利用mailgun搭建私有域名邮箱
---

# 起因

本着折腾中进步的原则，从切换到 xdays.me 这个域名之后就想折腾下邮箱。个人邮箱主要带来以下好处：

1. 有些服务需要用企业邮箱
2. 看上去牛逼一些

本文总结了利用 mailgun 和 gmail 来实现私有域名邮箱功能。

# Mailgun

Mailgun 是 Rackspace 面向开发者的邮件发送服务，但是它提供的功能足够我们打造属于自己的个人邮箱了。我们知道邮箱服务简单来说就两个功能，发送邮件和接收邮件。Mailgun 为我们提供了 SMTP server 用于发送邮件和 Email Route 用于转发邮件到特定的邮箱以收取邮件。此外还涉及一些反垃圾邮件的机制。

## Domain

注册了 mailgun 的账号之后，你需要添加一个 domain，然后根据向导添加对应的 DNS 记录，等 mailgun 验证通过。

## SMTP Server

添加了 Domain 之后我们的 SMTP Server 已经设置好了，但是我们需要添加一个和 Gmail 继承的账号，如下图所示，点击“Manage SMTP credentials”来管理账号

![mailgun-credentials](/wp-content/uploads/2016/08/mailgun-credentials.png)

添加完账号之后就可以登录 SMTP 服务器发送邮件了，假设我们这里添加的是 test@xdays.me

## Route

虽然 mailgun 没有提供 POP3 的服务，但是其提供了邮件路由的功能同样能达到让我们收取邮件的目的。按照下图所示添加一个邮件路由，用来将所有发给 test@xdays.me 的邮件都转发给你的 Gmail 邮箱

![mailgun-routes](/wp-content/uploads/2016/08/mailgun-routes.png)

到这里 mailgun 的部分就配置完成了

# Gmail

其实 Gmail 的配置和添加其他免费邮箱账号没有区别。

点击 Settings -> Accounts and Import -> Add another email address you own，然后根据向导配置你的 SMTP Server 的认证信息即可。

# 总结

简单说下完成之后邮件的流向，当有人向 test@xdays.me 发送邮件时，mailgun 会将邮件通过邮件路由转发到 Gmail 邮箱，然后当在 Gmail 里回复邮件的时候，Gmail 通过 mailgun 的 SMTP 服务器将邮件回复给发送者。
