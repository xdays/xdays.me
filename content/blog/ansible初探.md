---
title: Ansible初探
date: 2013-10-31
author: admin
category: devops
tags: ['ansible', 'devops']
slug: ansible初探
---

# 简介

ansible 是一个自动化管理工具，它足够简单且足够强大来管理大批量设备。可用于配置系统，部署软件以及组合复杂任务。关于其来由可参考[中文 FAQ](http://shzhangji.com/blog/2013/06/11/ansible-faq/)

# 特性

- 无 agent 模式，push 模式，这一点与[fabric](//fabric初探/)有几分类似
- 并发执行
- 可用任何语言写扩展模块
- 有类似[Puppet](http://puppetlabs.com/)（RAL）或者[SaltStack](http://saltstack.org/)（state）的 playbook
- 灵活的匹配规则，通配符，正则

# 执行模型

如图所示： ![ansible
architecture](/wp-content/uploads/2013/10/ansible_architecture.jpg)

​\* 首先，你需要定义设备列表，即任务执行的范围 \*
然后，Ansible 能通过调用模块来在这些设备上执行任务 \*
此外，可以通过用 playbook 描述要执行的任务的逻辑，完成任务组合

# ansible 命令

## 语法

    ansible <pattern_goes_here> -m <module_name> -a <arguments>

## 选项

*注意：*通常选项也可以通过配置文件来配置 \* -i
设备列表路径，注意可以通过这里制定一些动态路径，如数据库等 \* -f
并行任务数 \* --private-key 私钥路径 \* -m 模块名 \* -M 模块夹在路径 \*
-a 参数 \* -k 登陆密码 \* -K sudo 密码 \* -t 输出结果保存路径 \* -B
后台运行超时时间 \* -P 调查后台程序时间 \* -u 执行用户 \* -U sudo 用户 \*
-l 限制设备范围

# 示例

## 定义设备

vim /etc/ansible/hosts

    local   ansible_ssh_host=localhost   ansible_connection=local
    aliyun  ansible_ssh_host=cloud.xdays.me   ansible_ssh_private_key_file=~/.ssh/id_rsa​

## 执行命令

    ansible aliyun -a 'w' #默认调用command模块

# 高级功能

- Playbooks，暂时不作研究，详见官方文档;
- API，可以参考 AWX 结合 API 来做适合自己的运维平台

# 参考链接

[官方文档](http://www.ansibleworks.com/docs/)
[中文 FAQ](http://shzhangji.com/blog/2013/06/11/ansible-faq/)
