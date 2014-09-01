Title: Centos5搭建Exmail邮件系统
Date: 2011-08-02 19:48
Author: admin
Category: server
Tags: mail
Slug: centos5搭建exmail邮件系统

### 邮件系统运行原理

#### [![mail-architecture](http://www.xdays.info/wp-content/uploads/2011/08/mail-architecture.gif "mail-architecture")](http://www.xdays.info/wp-content/uploads/2011/08/mail-architecture.gif)

#### MUA，MTA和MDA

MUA叫邮件用户代理，是客户端软件负责与用户交互，接受用户指令；MTA是邮件传输代理，负责判断邮件取向，如果目的地是自己就直接交给MDA处理，如果是其他MTA则用SMTP转发邮件；MDA是邮件投递代理，负责将目的地是本机的邮件投放到相应用户的邮箱中，将不是本机的邮件通过MTA发送给其他的主机，在这个过程中可以执行邮件过滤和自动回复等操作。

#### 传送流程

1.  用户写明邮件发件人A和收件人B，标题以及正文内容点发送，邮件便发送到A自己的MTA上，进入MTA的队列中
2.  如果邮件收件人B属于用户自己的MTA则直接通过MDA投放到收件人B相应的邮箱里去
3.  如果是收件人B属于其他的MTA，则发件人A的MTA开始转发（relay）流程，通过SMTP发送给下一台MTA，当然这个过程需要经过下一台MTA的许可（通过IP地址限制）或者认证（用户名密码）
4.  最后收件人的MTA收到邮件后，通过MDA放到收件人的邮箱里，等待收件人查看和下载

### Extmail 简介

Extmail是一套基于开源软件的邮件系统解决方案。其主要特点有支持STMP和POP统一用数据库认证及ESTMP，支持1G大邮件，web界面，病毒过滤和内容过滤，图形化日志分析，spam过滤，别名和多域等特点，目前应用广泛。

### Extmail 系统结构

  -------------------------- --------------------- ----------------------------------------------
  功能模块                   功能模块2             功能模块2
  操作系统（OS）             CentOS 5.3            CentOS和RHEL是一样的，而且升级免费
  Web 服务器                 Apache 2.2.x          CentOS 自带
  数据库/目录服务            MySQL 5.0.X           CentO 自带
  邮件传输代理（MTA）        postfix-2.6.2         使用最新版本2.6.2
  邮件投递代理（MDA）        maildrop 2.0.x        支持过滤和强大功能
  Web帐户管理后台            ExtMan 1.0            支持无限域名、无限用户
  WebMail 系统               ExtMail 1.1.0         支持多语言、全部模板化，功能基本齐全
  日志分析及显示             mailgraph\_ext        ExtMan中已经包含了
  其他数据认证库             Courier Authlb 0.62   负责courier-imap,maildrop的认证
  SMTP认证库                 Cyrus SASL 2.1.x      标准的SASL实现库，可以支持Courier authlib
  内容过滤器                 Amavisd-new 2.6.4     Content-Filter软件，支持与Camav/SA的挂接
  内容级别的反垃圾邮件工具   SpamAssassin-3.2.5    著名的SA，可以支持大量规则
  防病毒软件（Anti-Virus）   ClamAV 0.95.2         最热门的开源杀毒软件
  SMTP阶段反垃圾邮件工具     Spam Locker 0.99      基于SMTP行为识别的Antispam软件，大量可选插件
  高效的反垃圾邮件工具       Dspam-3.8             高精确度的、智能的过滤功能
  -------------------------- --------------------- ----------------------------------------------

注意：ExtMail很好的实现了统一认证，SMTP认证和POP认证统一通过Courier-Authlib提供的authdaemon认证，只是STMP需要透过cyrus-sasl连接到authdaemon来认证。

### Extmail安装配置

#### EMOS安装盘

EMOS是继承了Extmail的centos系统安装盘，安装后有命令行的图形界面的配置向导，默认点回车就可以，但是不利于理解Extmail的运行机制。

参考链接：http://linzhibin824.blog.163.com/blog/static/7355771020103515222334/

#### 手工yum方式安装

官方给的wiki里有详细的配置方法，唯一需要注意的细心配置，可能落下一条命令整个系统就无法跑起来，所以要细心细心在细心！！

官方文档：<http://wiki.extmail.org/extmail_solution_for_linux_centos-5>
