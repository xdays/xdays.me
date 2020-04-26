---
title: fabric初探
date: 2013-06-10
author: admin
category: devops
tags: ['devops', 'python']
slug: fabric初探
---

# 简介

Fabric 是一个用于应用部署和系统管理的工具，它让基于 ssh 的的操作更灵活；你可以在本地或者远程批量执行一些命令，上传下载文件等。

# 优势

- 简单，没有架构，不需要理解 master/agent(puppet)啦，master/minion(saltstack)啦相关的概念，当然任何一个工具都有自己的逻辑规则，相比其他工具 fabric 的学习成本要低很多；
- Pythonic，最小的执行单位---任务，就是基本的 python 函数，灵活性强；
- 并行执行，尽管如此性能仍不及 M/S 模式的其他工具;
- 可扩展，这是我认为最大的优势，你可以很轻松的在 fabric 之上构建自己的平台，如监控和部署等。

# 安装

由于 fabric 尚不完善，我个人建议直接从 github 获取最新的代码安装：

    git clone https://github.com/fabric/fabric.git
    cd fabric/fabric
    python setup.py install

也可以通过 pip 安装

    pip install fabric

# 程序逻辑

## 环境字典

fabric 的配置，也可以说是环境变量，其中的变量影响了 fabric 的行为，比如要执行的设备列表，连接超时时间等。

## 设备列表

fabric 通过 host_string 来表示一个设备，host_string 的格式为：

    username@hostname:port

设备列表定义了待执行任务的设备，还有一个角色概念可以组织设备，例如将 web 服务定义为一个角色。

设备列表示例：

    env.hosts= ['username@hostname:port']

设备角色示例：

    env.roledefs = {'web': ['web1', 'web2']}

## 执行模型

fabric 在预先定义的设备上依次执行任务，你可以通过在定义任务或者命令行下分配任务，如一台设备应该执行那些任务，一个任务应该在那些设备上执行。

# fab 命令

## 命令语法

fabric 的命令行接口，负责解析 fabfile，和环境字典一样，也可以控制执行模型等。命令语法如下：

    Usage: fab [options] <command>[:arg1,arg2=val2,host=foo,hosts='h1;h2',...]

## 常见参数

常见参数如下： \* -l 察看定义的任务数 \* -H 制定要运行任务的设备列表 \*
-- 后跟要在设备上执行的命令

# 示例

## 本地执行

    from fabric.api import run
    def host_type():
        run('uname -s')

## 远程执行

    from fabric.api import local, run, env
    env.hosts = ['host']
    env.passwords = {'host': 'pass'}
    def host_type():
        run('uname -s')

# 特性用法

## Gateway

需求驱动，这里有必要重点强调下 fabric 的 gateway 特性。假设一个场景：我要在 A 设备上运行 fabric 在 B 设备上执行命令，我们最常见的数据流是 A-\>B，但是如果 B 做了安全限制之允许 C 登陆 B，但是 C 又无法运行 fabric 怎么办？设想一下，假如数据流这么走 A-\>C-\>B，在 B 看来是 C 在操作自己所以允许执行，实际上是 A 告诉 C 去操作 B 又满足了我们的需求。是的，这就是 fabric 的 gateway 特性你之需要通过环境字典或者命令行方式制定 gateway 和对应的权限信息就可以实现了。
代码示例：

    from fabric.api import local, run, env
    env.gateway = 'gateway'
    env.hosts = ['host']
    env.passwords = {'host': 'pass', 'gateway':'pass'}
    def host_type():
        run('uname -s')

**注意**：fabric 目前还不够完美，在查找 host 或者 gateway 对应密码的两个函数（见 network.py）还不够灵活，所以我这里建议在设备列表和密码字典中都用完整的 host_string。

# 相关项目

[fabric 的强化版 ansible](http://www.ansibleworks.com/)

# 参考链接

[官方文档](http://docs.fabfile.org/en/1.6/)

[Github 主页](https://github.com/fabric/fabric)
