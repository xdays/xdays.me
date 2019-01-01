---
title: IPython自动重新加载模块
date: 2014-01-18
author: admin
category: python
tags: ipython, python
slug: ipython自动重新加载模块
---

问题
====

调试模块的时候需要不断修改代码，只有重新加载模块才可以看修改效果，而重新加载的方法有reload内置方法和重新运行解释器，这样都不是很方便，我希望修改代码能立刻生效。

解决
====

IPython有个autoreload扩展，只需要开启扩展并定义扩展的模式即可。

开启扩展
--------

默认的配置位于\~/.config/ipython/profile\_default/ipython\_config.py，编辑该文件新增：

    c.InteractiveShellApp.extensions = ['autoreload']

设定模式
--------

编辑文件\~/.config/ipython/profile\_default/ipython\_config.py，新增：

    c.TerminalIPythonApp.exec_lines = ['%autoreload 2']

这样即可满足需求。
