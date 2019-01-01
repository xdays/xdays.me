---
title: 思科实验模拟器Dynamips&Dynagen
date: 2010-10-24
author: admin
category: ccna
tags: ccna, cisco, dynamips
slug: 思科实验模拟器dynamipsdynagen
---

Dynamips是所有这些软件的核心负责加载运行IOS等工作，其他的都是基于其上的中间层，目的就是便于用户使用，Dynagen是基于.net文件和命令行的工具，而DynamipsGUI也就是小凡是图形界面的更易于操作。软件最大的特点是真实加载IOS，可以与真实的网卡桥接，还可以虚拟帧中继交换机，ATM交换机。

软件下载

官方网站 <http://www.dynagen.org/>

windows版的虽然做成了安装包，软件是纯绿色的，安装后可以随意移动文件夹。

主要组件

Dynamips，Dynagen，.net文件和一些简化操作的批处理脚本。

1）  Dynamips

-H  7200 在7200端口上启动Dynamips

-e   查看真实网卡参数，供虚拟桥接用

2）Dynagen pathtonetfile

具体命令可以用help命令查看；注意加载IOS后要用idlepc get
device\_name命令计算idle值命用idlepc save device\_name default
存入net文件中

3）net文件

这是设置虚拟路由器型号和构建拓扑的关键文件，在安装目录的sample\_labs目录下有一个all\_config\_options.txt文件供参考，具体配置可以参考网上别人测试后作的现成文件。

4）批处理脚本bat文件

需要注意的就是：要在tmp目录下运行Dynamips以便产生的临时问价都位于此文件夹内便于以后清除。

操作步骤

前期准备：下载IOS，构思拓扑图

具体步骤：运行Dynamips—编写net文件也就是选设备和构建拓扑—运行Dynagen加载IOS—启动设备—telnet配置实验

一个net文件示例-三个路由器串联：

    # 3routerlab

    autostart = False

    [localhost]

    port = 7200

    udp = 10000

    workingdir = ..tmp

    [[3640]]

    image = ..imagesc3640-telco-mz.124-8.bin

    #npe = npe-400

    ram = 60

    mmap = False

    confteg = 0x2142

    [[ROUTER R1]]

    model = 3640

    s1/0 = R2 s1/0

    [[router R2]]

    model = 3640

    s1/1 = R3 s1/0

    [[router R3]]

    model = 3640

参考链接：

<http://www.ipflow.utc.fr/index.php/Cisco_7200_Simulator>

<http://www.dynagen.org/>

<http://wenku.baidu.com/view/dbaf7bbfc77da26925c5b06d.html>
