---
title: linux 环境变量文件
date: 2010-08-01
author: admin
category: linux
tags: linux
slug: linux-环境变量文件
---

环境设置文件包括系统设置文件和个人设置文件。  
1. 系统设置文件：  
/etc/sysconfig/i18n   系统语系  
/etc/profile   设置系统重要的变量  
/etc/bashrc   确定umask功能 确定提示符内容 命令别名及系统其他功能  
/etc/profile.d/\*.sh   进行一些附加设置值如命令别名  
/etc/man.config   man page查找路径  
2. 个人设置值：  
\~/bash\_profile bash\_login .profile   定义个性化路径和环境变量
按顺序搜索文件有一个就可以  
\~/.bashrc   个性化设置值  
\~/.bash\_history   历史命令记录文件  
\~/.bash\_logout 记录注销后进行的操作  
体会：  
1. 能定义个性设置值的地方有三个/etc/bashrc    \~/.bashrc  
/etc/profile.d,容易忽略第三个目录下设置的命令别名。
