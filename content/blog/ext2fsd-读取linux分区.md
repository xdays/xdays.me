---
title: Ext2Fsd-读取linux分区
date: 2010-09-26
author: admin
category: tool
tags: ['software']
slug: ext2fsd-读取linux分区
---

Ext2Fsd 这个小工具，便可以实现在 Windows 中挂载 Linux
分区的目的。Ext2Fsd 能够在 Windows 2000、XP、2003、Vista
等系统中运行，支持挂载 Ext2/Ext3 类型的分区,对 Ext4 的支持还不是太好。

我的双系统是 xp 和 ubuntu10.04，能看到文件件看不到里面的内容，虽然我安装时没选可写功能，但还是悠着点，期待更新吧！

程序目录内就那几个文件主要有这样几个工具：Ext2Mgr.exe 是主程序，Mke2fs.exe 格式化工具，Mount.exe 挂载工具，具体用法用-h 选项查看，DrvRemover.exe 删除所有挂载点。

[官方主页：http://www.ext2fsd.com/](http://www.ext2fsd.com/)
