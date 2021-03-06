---
title: CCNA-硬件及IOS
date: 2010-10-28
author: admin
category: network
tags: ['ccna']
slug: ccna-硬件及ios
---

- 硬件组成
  - 主要部件
  - 接口与端口
- 配置寄存器
- 启动过程
- IOS 备份升级
- CLI 命令
  - 设置标志区
  - 重设口令
  - 启用 ssh 服务
  - 设置加载 ios 顺序和位置
  - 优化命令

### 硬件组成

#### 主要部件

应当说路由器就是一台专用计算机，它的主要组件有：

---

名称 功能
只读存储器（ROM） 开机自检程序 POST 确定硬件功能及可用接口，Bootstrap 引导程序加载 IOS，微型 IOS 用于维护操作
随机存储器（RAM） 保存路由器运行时的临时数据，各种表，相当于ＰＣ中的内存
非易失性存储器（NVRAM） 保存路由器和交换机的配置
闪存（FLASH） 用于保存 IOS 文件
配置寄存器（configuration register） 控制路由器的启动方式，需要注意它存储在 NVRAM 中

---

#### 接口与端口

接口（interface）通常指用于转发数据包的物理接口，而端口（port）指用于管理路由器的物理接口

### 配置寄存器

共有 16 位来控制路由器的启动方式。其中第 6 位表示忽略 NVRAM 内容，用于重设口令，最为常见；正常情况为 0x2102，忽略 NVRAM 中配置文件为 0x2142，详见重设口令

### 启动过程

1.  上电，POST 执行自检，检查接口
2.  Bootstrap 查找 IOS 并加载，默认从闪存中加载，然后是 TFTP 上，最后是 ROM 中的迷你 IOS
3.  IOS 在 NVRAM 中查找启动配置文件，如果没有发送广播在 TFTP 上寻找配置文件，如果也没有就启动设置模式

### 备份升级

#### 有 IOS 升级备份

1.  确定与 TFTP 的连通性 ping
2.  查看 FLASH 大小，sh flash / sh version
3.  升级\#copy tftp flash/备份\#copy flash tftp

#### 重新安装 IOS

有时候因为一些情况 flash 中 IOS 被破坏导致系统无法正常启动，两种解决办法，具体如下：

系统无法加载 IOS 默认是进入 rommon 模式

方法一  tftpdnld

1.  设置如下环境变量，指定 tftp 和加载文件
2.  执行 tftpdnld，然后按提示操作后，reset 重启

方法二 xmodem

1.  需要说明的是用 console 口传很慢，能加快点的方法是提高波特率，通过 rommon\>confreg 按提示设置波特率最高，再修改终端软件的波特率
2.  执行命令 rommon\>xmodem {the name of the IOS that is saved on the PC}
3.  根据使用情况找到 send xmodem 命令，按提示选择发送，等待完成，reset 重启

### CLI 命令

需要注意常用的命令有：

#### 设置标志区

以相同的字符作为分隔符。(config)\#banner motd \\\$====\$

#### 重设口令

1.  启动过程中按 ctrl+break 键进入 rommon 模式
2.  设置配置寄存器，使加载过程忽略 NVRAM，rommon\>confreg
    0x2142，reset 重新启动
3.  加载配置文件\#copy start run
4.  重设密码(config)\#enable secret \*\*\*
5.  保存配置文件\#copy run start

#### 启用 ssh 服务

1.  首先必须要添加主机名和域名因为生成密钥时会用到
2.  生成密钥（crypto key generate rsa genera-keys modulus 1024），
3.  设置超时时间和最大尝试失败次数（ip ssh
    time-out/authentication-retries 2），
4.  允许 ssh 请求（transport input ssh telnet）

#### 设置路由器加载 IOS 顺序和位置

执行（config）\#boot system ?
可以看到路由器可以从很多位置加载 IOS，从 tftp 加载 IOS 的好处是可以多个路由器共享一个 IOS 方便升级，节省空间，另外可以配置多个启动位置以确保可以顺利启动路由器。

示例：

    R3640(config)#boot system tftp c3640-jk9s-mz.124-16.bin 192.168.1.250

    R3640(config)#boot system flash c3640-js-mz.124-12.bin

    R3640(config)#boot system rom

#### 优化命令

    no ip domain-lookup 不进行域名解析

    line console 0

    logging syn 消息同步

    exec-time 0 0 登陆不超时
