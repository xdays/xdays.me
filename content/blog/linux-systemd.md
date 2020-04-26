---
title: Linux Systemd笔记
date: 2016-04-16
author: admin
category: linux
tags: ['linux', 'systemd']
slug: linux-systemd
---

# 背景

这是我的一篇我之前学习 systemd 的这个[系列教程](http://0pointer.net/blog/projects/systemd-pdf.html)的笔记，在此记录下吧。

# 简介

- 和 init 和 upstart 类似的 Linux 服务管理程序
- 提供优秀框架以表示系统服务间的依赖关系
- 并行启动服务，并通过 cgroup 跟踪服务进程
- 支持对系统状态建立和恢复快照
- 支持 crontab

# 使用

## 服务状态

- 因为启动过程太快，用户可能来不及看服务启动过程，故 systemd 跟踪进程的启动过程保留下来，以便后续查看。通过 systemctl status 能看到服务的状态以及返回的状态码。

## cgroup

- 通过 cgroup 来管理进程，没有继承可以脱离管理。通过两个命令来查看进程的所属 cgroup，一个是`ps xawf -eo pid,user,cgroup,args`，一个是 systemd-cgls

## 迁移 sysv 脚本

- 如何把传统的 sysv 脚本迁移为 systemd 的配置文件。shell 脚本的弊端，慢，可读性差，脆弱，不具备有序并行执行，不能监控进程。
- 迁移需要获取的信息，服务描述，服务依赖，运行级别，启动命令
- 字段描述
  - Unit 段表示服务的通用信息，systemd 不仅管理服务，还管理设备，挂载点，时钟等系统的其他组件，所有这些被管理的对象都称为 unit
  - After 仅表达一种依赖关系，不会对依赖服务做任何操作
  - Servcie 段表示服务的本身信息，ExecStart 表示启动命令，Type 表示服务如何告知系统其已经启动完毕，早先都是通过 forking 的方式，现在为了让 systemd 更好的监视进程用 dbus，配合指定一个 BusName 来制定其标识
  - Install 段表示什么条件下才会启动该服务，WantedBy 表示在需要启动哪个 target 的时候启动该服务

## 关闭服务

- systemctl kill name.service
- systemctl kill -s SIGKILL name.service
- systemctl kill -s HUP --kill-who=main name.service

## 开关启动

- systemctl enable/disable name.service 开关开机启动
- systemctl start/stop name.service 开关服务
- /etc/systemd/system 里的配置覆盖/lib/systemd/system 里的配置

## chroot

- chroot 有两种用法，一个是为了安全，一个是为了测试和调试等
- ReadOnlyDirectories 和 InaccessibleDirectories 是一个替代 chroot 的解决办法
- RootDirectory 就是 chroot，要配合 ExecStartPre 脚本把环境弄好
- systemd-nspawn 就是一个精简的 LXC

## 系统提速

- systemd-analyze blame
- systemd-analyze plot > /tmp/boot.svg

## 配置文件

### 新增功能

- 文件系统挂载
- 文件系统配额
- 配置主机名
- 配置环回接口设备
- 加载 SELinux 策略
- 注册额外的二进制格式，如 java，wine 等
- 设置系统 locale
- 配置 console 字体和字符集
- 创建删除临时文件
- 应用/etc/fstab 的挂在选项
- 应用 sysctl 的设置
- 收集和中继预读信息
- 更新 utmp 文件
- 加载和保存随即 seed
- 静态加载特定的内核模块
- 配置加密磁盘和分区
- 在 console 口启动 tty
- 维护 plymouth
- 机器 ID 维护
- 设置 UTC 时钟

### 配置文件

- /etc/hostname
- /etc/vconsole.conf 终端的字符集和字体
- /etc/locale
- /etc/modules-load.d/\*.conf 静态加载内核模块
- /etc/sysctl.d/\*.conf
- /etc/tmpfiles.d/\*.conf 临时文件目录，在开机和关机时会被创建更新和删除
- /etc/binfmt.d/\*.conf 二进制文件注册
- /etc/os-releases
- /etc/machine-id

## /etc/sysconfig 和/etc/default

- 作者列举了一堆理由来说明这两个目录已经不需要了
- 目录存在的意义就是更新时保持兼容
- EnvironmentFile 这个指令来兼容这两个目录

## 实例化进程

- 我想大概就是通过定义模板来实例化多个进程吧

## 迁移 inetd 服务

- system 基于 socket 激活服务机制
- socket 激活的三种应用场景
  - 为并行性，简化性，鲁棒性
  - 当请求时激活单个进程
  - 当请求时每个请求激活单个进程

## 加固服务

- 服务和网络隔离，PrivateNetwork
- 服务单独的/tmp，PrivateTmp
- 让目录对服务不可见或者只读，ReadOnlyDirectories 和 InaccessibleDirectories
- Taking away capabilities from services，CapabilityBoundingSet
- 不允许 forking，限制服务创建文件，RLIMIT_NPROC 和 RLIMIT_FSIZE
- 控制服务访问设备，DeviceAllow
- 其他选项 RootDirectory，USER，GROUP

## 日志和服务状态

- systemctl status

## 不言自明的启动过程

- systemctl status 有对应服务的 manpage
- 启动过程http://www.freedesktop.org/software/systemd/man/bootup.html

## watchdog

## 串口终端

## 日志管理

日志通过 journalctl 命令查看

- -f 追踪日志
- -b 查看本次启动的日志
- -p 错误等级
- --since --until 时间范围
- \_metadata 通过 meta 信息查询

## 管理资源

- DefaultControllers，可配置 cpu, memory 和 blkio 分别对 cpu，内存和 io 做限制
- cpu，CPUShares
- memory，MemoryLimit 和 MemorySoftLimit
- blkio，BlockIOWeight，BlockIOReadBandwidth 和 BlockIOWriteBandwidth 可针对磁盘和目录做控制
- 其他控制 ControlGroupAttribute

## 虚拟化

- systemd-detect-virt 用来检测虚拟化
- ConditionVirtualization 可以指定 yes/no，也可以指定特定的虚拟化类型

## Socket 激活服务和容器

- socket 激活可复用资源
- systemd 通过 socket 启动 container(通过 service 名一一对应)，然后和 container 里的 systemd 配合，启动 container 里的 service

# 参考

- http://www.freedesktop.org/wiki/Software/systemd/
- http://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html
