---
title: GRUB2笔记
date: 2010-09-26
author: admin
category: linux
tags: ['grub2', 'linux']
slug: grub2笔记
---

GRUB2 的组成部分？

GRUB2 主要有三个部份：

/etc/default/grub            --这个文件包含了 GRUB2 的菜单。  
/etc/grub.d/                   --这个目录包含了生成 GRUB2 菜单的脚本。  
/boot/grub/grub.cfg       --GRUB2 的配置文件，勿直接编辑。  
update-grub command reads the /etc/grub.d directory and looks for
executable scripts inside it. The scripts are read, in the order of
their numbering, and written into the grub.cfg file, along with the menu
settings read from the /etc/default/grub file.

update-grub 命令读取 /etc/grub.d
目录中的可执行脚本，并且按照数字顺序执行来生成 grub.cfg
文件，这期间 00_header 会读取/etc/default/grub 文件中的配置。

启动条目来自多个地方，默认的来自安装 GRUB 的发行版，还有在硬盘上探测到的其他操作系统，外加用户添加 shell 脚本增加的定制条目。

添加或者删除某个条目，您可以通过更改脚本的权限实现，并不需要删除它们。GRUB2 可以在任何时候重新安装，包括通过 GRUB2 启动的系统中。

如何恢复 GRUB2？

比较通用的办法：  
1）想办法用 livecd 启动系统  
2）挂载相应分区：如果没有给/boot 单独分区就直接\#sudo  mount  /dev/sdax
/mnt;然后\#sudo grub-install --root-directory=/mnt /dev/sda 就完成了  
3）还有一种用到 chroot 的方法，chroot 挺可怕的，根目录都变了。

GRUB2 启动引导器 – 完全教程
(1)<http://apps.hi.baidu.com/share/detail/15773952>  
GRUB2 启动引导器 – 完全教程
(2)<http://apps.hi.baidu.com/share/detail/15224191>

再附上一篇比较详细的教程： <http://blog.chinaunix.net/u/4466/showart_2108545.html>
