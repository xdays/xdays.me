---
title: CCNA-硬件及IOS
date: 2010-10-28
author: admin
category: ccna
tags: cisco, cli, ios
slug: ccna-硬件及ios
---

-   硬件组成
    -   主要部件
    -   接口与端口
-   配置寄存器
-   启动过程
-   IOS备份升级
-   CLI命令
    -   设置标志区
    -   重设口令
    -   启用ssh服务
    -   设置加载ios顺序和位置
    -   优化命令

### 硬件组成

#### 主要部件

应当说路由器就是一台专用计算机，它的主要组件有：

  -------------------------------------- ---------------------------------------------------------------------------------------
  名称                                   功能
  只读存储器（ROM）                      开机自检程序POST确定硬件功能及可用接口，Bootstrap引导程序加载IOS，微型IOS用于维护操作
  随机存储器（RAM）                      保存路由器运行时的临时数据，各种表，相当于ＰＣ中的内存
  非易失性存储器（NVRAM）                保存路由器和交换机的配置
  闪存（FLASH）                          用于保存IOS文件
  配置寄存器（configuration register）   控制路由器的启动方式，需要注意它存储在NVRAM中
  -------------------------------------- ---------------------------------------------------------------------------------------

#### 接口与端口

接口（interface）通常指用于转发数据包的物理接口，而端口（port）指用于管理路由器的物理接口

### 配置寄存器

共有16位来控制路由器的启动方式。其中第6位表示忽略NVRAM内容，用于重设口令，最为常见；正常情况为0x2102，忽略NVRAM中配置文件为0x2142，详见重设口令

### 启动过程

1.  上电，POST执行自检，检查接口
2.  Bootstrap查找IOS并加载，默认从闪存中加载，然后是TFTP上，最后是ROM中的迷你IOS
3.  IOS在NVRAM中查找启动配置文件，如果没有发送广播在TFTP上寻找配置文件，如果也没有就启动设置模式

### 备份升级

#### 有IOS升级备份

1.  确定与TFTP的连通性ping
2.  查看FLASH大小，sh flash / sh version
3.  升级\#copy tftp flash/备份\#copy flash tftp

#### 重新安装IOS

有时候因为一些情况flash中IOS被破坏导致系统无法正常启动，两种解决办法，具体如下：

系统无法加载IOS默认是进入rommon模式

方法一  tftpdnld

1.  设置如下环境变量，指定tftp和加载文件
2.  执行tftpdnld，然后按提示操作后，reset重启

方法二 xmodem

1.  需要说明的是用console口传很慢，能加快点的方法是提高波特率，通过rommon\>confreg按提示设置波特率最高，再修改终端软件的波特率
2.  执行命令rommon\>xmodem {the name of the IOS that is saved on the PC}
3.  根据使用情况找到send xmodem命令，按提示选择发送，等待完成，reset重启

### CLI命令

需要注意常用的命令有：

#### 设置标志区

以相同的字符作为分隔符。(config)\#banner motd \$====\$

#### 重设口令

1.  启动过程中按ctrl+break键进入rommon模式
2.  设置配置寄存器，使加载过程忽略NVRAM，rommon\>confreg
    0x2142，reset重新启动
3.  加载配置文件\#copy start run
4.  重设密码(config)\#enable secret \*\*\*
5.  保存配置文件\#copy run start

#### 启用ssh服务

1.  首先必须要添加主机名和域名因为生成密钥时会用到
2.  生成密钥（crypto key generate rsa genera-keys modulus 1024），
3.  设置超时时间和最大尝试失败次数（ip ssh
    time-out/authentication-retries 2），
4.  允许ssh请求（transport input ssh telnet）

#### 设置路由器加载IOS顺序和位置

执行（config）\#boot system ?
可以看到路由器可以从很多位置加载IOS，从tftp加载IOS的好处是可以多个路由器共享一个IOS方便升级，节省空间，另外可以配置多个启动位置以确保可以顺利启动路由器。

示例：

    R3640(config)#boot system tftp c3640-jk9s-mz.124-16.bin 192.168.1.250

    R3640(config)#boot system flash c3640-js-mz.124-12.bin

    R3640(config)#boot system rom

#### 优化命令

    no ip domain-lookup 不进行域名解析

    line console 0

    logging syn 消息同步

    exec-time 0 0 登陆不超时
