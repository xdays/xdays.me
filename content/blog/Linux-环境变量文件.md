---
title: Linux 环境变量文件
date: 2010-08-01
author: admin
category: linux
tags: ['linux']
slug: linux-环境变量文件
---

系统环境设置文件包括系统设置文件和个人设置文件。

# 系统设置文件

- /etc/sysconfig/i18n 系统语系
- /etc/profile 设置系统重要的变量
- /etc/bashrc 确定 umask 功能 确定提示符内容 命令别名及系统其他功能
- /etc/profile.d/\*.sh 进行一些附加设置值如命令别名

# 个人设置文件

- ~/bash_profile
- ~/.bashrc 个性化设置值
- ~/.bash_history 历史命令记录文件
- ~/.bash_logout 记录注销后进行的操作

# 总结：

- /etc/bashrc
- ~/.bashrc
- /etc/profile.d

通常容易忽略第三个目录下设置的命令别名。
