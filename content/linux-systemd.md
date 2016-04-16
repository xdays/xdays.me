Title: Linux Systemd笔记
Date: 2016-04-16 15:29
Author: admin
Category: linux
Tags: linux,systemd
Slug: linux-systemd

# 背景

这是我的一篇我之前学习systemd的这个[系列教程](http://0pointer.net/blog/projects/systemd-pdf.html)的笔记，在此记录下吧。

# 简介
* 和init和upstart类似的Linux服务管理程序
* 提供优秀框架以表示系统服务间的依赖关系
* 并行启动服务，并通过cgroup跟踪服务进程
* 支持对系统状态建立和恢复快照
* 支持crontab

# 使用
## 服务状态
* 因为启动过程太快，用户可能来不及看服务启动过程，故systemd跟踪进程的启动过程保留下来，以便后续查看。通过systemctl status能看到服务的状态以及返回的状态码。

## cgroup
* 通过cgroup来管理进程，没有继承可以脱离管理。通过两个命令来查看进程的所属cgroup，一个是`ps xawf -eo pid,user,cgroup,args`，一个是systemd-cgls

## 迁移sysv脚本
* 如何把传统的sysv脚本迁移为systemd的配置文件。shell脚本的弊端，慢，可读性差，脆弱，不具备有序并行执行，不能监控进程。
* 迁移需要获取的信息，服务描述，服务依赖，运行级别，启动命令
* 字段描述
    * Unit段表示服务的通用信息，systemd不仅管理服务，还管理设备，挂载点，时钟等系统的其他组件，所有这些被管理的对象都称为unit
    * After仅表达一种依赖关系，不会对依赖服务做任何操作
    * Servcie段表示服务的本身信息，ExecStart表示启动命令，Type表示服务如何告知系统其已经启动完毕，早先都是通过forking的方式，现在为了让systemd更好的监视进程用dbus，配合指定一个BusName来制定其标识
    * Install段表示什么条件下才会启动该服务，WantedBy表示在需要启动哪个target的时候启动该服务

## 关闭服务
* systemctl kill name.service
* systemctl kill -s SIGKILL name.service
* systemctl kill -s HUP --kill-who=main name.service

## 开关启动
* systemctl enable/disable name.service 开关开机启动
* systemctl start/stop name.service 开关服务
* /etc/systemd/system里的配置覆盖/lib/systemd/system里的配置

## chroot
* chroot有两种用法，一个是为了安全，一个是为了测试和调试等
* ReadOnlyDirectories和InaccessibleDirectories是一个替代chroot的解决办法
* RootDirectory就是chroot，要配合ExecStartPre脚本把环境弄好
* systemd-nspawn就是一个精简的LXC

## 系统提速
* systemd-analyze blame
* systemd-analyze plot > /tmp/boot.svg

## 配置文件
### 新增功能
* 文件系统挂载
* 文件系统配额
* 配置主机名
* 配置环回接口设备
* 加载SELinux策略
* 注册额外的二进制格式，如java，wine等
* 设置系统locale
* 配置console字体和字符集
* 创建删除临时文件
* 应用/etc/fstab的挂在选项
* 应用sysctl的设置
* 收集和中继预读信息
* 更新utmp文件
* 加载和保存随即seed
* 静态加载特定的内核模块
* 配置加密磁盘和分区
* 在console口启动tty
* 维护plymouth
* 机器ID维护
* 设置UTC时钟

### 配置文件
* /etc/hostname
* /etc/vconsole.conf 终端的字符集和字体
* /etc/locale
* /etc/modules-load.d/*.conf 静态加载内核模块
* /etc/sysctl.d/*.conf
* /etc/tmpfiles.d/*.conf 临时文件目录，在开机和关机时会被创建更新和删除
* /etc/binfmt.d/*.conf 二进制文件注册
* /etc/os-releases
* /etc/machine-id


## /etc/sysconfig和/etc/default
* 作者列举了一堆理由来说明这两个目录已经不需要了
* 目录存在的意义就是更新时保持兼容
* EnvironmentFile这个指令来兼容这两个目录

## 实例化进程
* 我想大概就是通过定义模板来实例化多个进程吧

## 迁移inetd服务
* system基于socket激活服务机制
* socket激活的三种应用场景
    * 为并行性，简化性，鲁棒性
    * 当请求时激活单个进程
    * 当请求时每个请求激活单个进程

## 加固服务
* 服务和网络隔离，PrivateNetwork
* 服务单独的/tmp，PrivateTmp
* 让目录对服务不可见或者只读，ReadOnlyDirectories和InaccessibleDirectories
* Taking away capabilities from services，CapabilityBoundingSet
* 不允许forking，限制服务创建文件，RLIMIT_NPROC和RLIMIT_FSIZE
* 控制服务访问设备，DeviceAllow
* 其他选项RootDirectory，USER，GROUP

## 日志和服务状态
* systemctl status

## 不言自明的启动过程
* systemctl status有对应服务的manpage
* 启动过程http://www.freedesktop.org/software/systemd/man/bootup.html

## watchdog

## 串口终端

## 日志管理
日志通过journalctl命令查看
* -f 追踪日志
* -b 查看本次启动的日志
* -p 错误等级
* --since --until 时间范围
* _metadata 通过meta信息查询

## 管理资源
* DefaultControllers，可配置cpu, memory和blkio分别对cpu，内存和io做限制
* cpu，CPUShares
* memory，MemoryLimit和MemorySoftLimit
* blkio，BlockIOWeight，BlockIOReadBandwidth和BlockIOWriteBandwidth可针对磁盘和目录做控制
* 其他控制ControlGroupAttribute

## 虚拟化
* systemd-detect-virt用来检测虚拟化
* ConditionVirtualization可以指定yes/no，也可以指定特定的虚拟化类型

## Socket激活服务和容器
* socket激活可复用资源
* systemd通过socket启动container(通过service名一一对应)，然后和container里的systemd配合，启动container里的service

# 参考
* http://www.freedesktop.org/wiki/Software/systemd/
* http://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html
