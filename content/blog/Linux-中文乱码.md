---
title: Linux 中文乱码
date: 2010-09-26
author: admin
category: linux
tags: ['linux']
slug: linux-中文乱码
---

开这篇文章主要目的是来总结一下自己在 linux 下遇到的各种问题及其解决办法，其实归根结底都是字符编码的问题，不同系统的不同字符编码之间相互显示就会出现乱码，要做的就是把编码统一就行了。windows 采用的 gb2312 而 linux 用的 utf8，所以两者之间经常出现编码不一致

远程登录 putty 的中文显示？

打开 putty 主程序，选择 window-〉Appearance-〉Font
settings-〉Change...,选择 Fixedsys 字体,字符集选择 CHINESE_GB2312。  
在 window-〉Appearance-〉Translation 中，Received data assumed to be in
which character set 中,把 Use font encoding 改为 UTF-8.
如果经常使用,把这些设置保存在 session 里面。  
经过这两步设置就可以显示中文了。

登录 vsftp 服务器，中文文件列表显示乱码？

还是一开始提到了，linux 用 uft8 而想 flashfxp 这样的客户端软件用 gb2312 编码，所以产生乱码。至于解决办法可以这样考虑能更改的地方有四个：linux 和 windows 系统，vsftp，flashfxp。对于服务器而言，让客户去更改设置是不明智的，所以能更改的地方就只有 linux 和 vsftp，但是 vsftp 我在配置文件中没有找到相关选项，所以干脆直接把 linux 系统默认的 locale 改成 gb2312 吧。对于 redhat 系统，编辑/etc/sysconfig/i18n 文件改为 LANG="zh_CN.gb2312"，logout 再 login 一切就正常了。
