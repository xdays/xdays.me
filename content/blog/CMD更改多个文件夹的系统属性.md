---
title: CMD更改多个文件夹的系统属性
date: 2010-06-05
author: admin
category: windows
tags: ['cmd']
slug: cmd更改多个文件夹的系统属性
---

    @echo off
    for /d /r %%a in (*) do attrib -s "%%a"
    pause

这个批处理放在哪运行,就把哪当前的所有子目录去掉系统属性..

在 cmd 命令提示符下(对当前命令提示符的目录进行操作)

    for /d /r %a in (*) do attrib -s "%a"
