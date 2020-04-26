---
title: vitualenv
date: 2013-01-04
author: admin
category: python
tags: ['python']
slug: vitualenv
---

# 简介

virtualenv 是用于隔离 Python 开发环境的工具。

# 特点

- 解决依赖同一项目的不同版本问题
- 没有 root 权限不能向系统安装包

# 基本原理

类似 chroot 的模式，virtualenv 在项目目录下创建供 python 运行的基本系统目录结构，然后把 python 解释器和 pip 放到对应的目录下，然后通过修改对应的环境变量来达到执行对应程序的目的。

# 安装使用

    sudo apt-get install virtualenv
    virtualenv test
    source test/bin/activate
    which python;which pip

# 扩展

- [virtualenvwrapper](http://www.doughellmann.com/projects/virtualenvwrapper/)  一个 shell 脚本对 virtualenv 相关命令进行了封装，更容易使用。常用命令如 mkvirtualenv,lssitepackages,workon,deactivate 等
- [pythonbrew](http://https//github.com/utahta/pythonbrew)  一个可以不需 root 权限安装多个版本 python 环境的工具

# 参考链接

<http://www.virtualenv.org/> <http://www.jeffkit.info/2011/08/1012/>
<http://blogs.360.cn/blog/how-360-uses-python-1-virtualenv/>
<https://github.com/utahta/pythonbrew>
