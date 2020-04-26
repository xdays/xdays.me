---
title: iconv-字符编码转换
date: 2010-07-20
author: admin
category: tool
tags: ['iconv']
slug: iconv-字符编码转换
---

linux 下打开 windows 下的文本文件时通常都是乱码，这是因为 windows 的字符编码是 gbk 而 linux 的是 utf8，所以需要转换才行。  
转换工具：iconv  
用法：

-f, --from-code=NAME 原始文本编码

-t, --to-code=NAME 输出编码

信息：

-l, --list 列举所有已知的字符集

输出控制：

-c 从输出中忽略无效的字符

-o, --output=FILE 输出文件

-s, --silent suppress warnings

--verbose 打印进度信息

-?, --help 给出该系统求助列表

--usage 给出简要的用法信息

-V, --version 打印程序版本号

示例：iconv -f gbk -t utf8 gbktext.txt \>utf8text
