---
title: 思科实验模拟器GNS3使用总结
date: 2011-01-04
author: admin
category: network
slug: 思科实验模拟器gns3使用总结
---

实验模拟器除了 packet
tracer 我学习过 dynamips 和 dynagen，在我总结 dynagen 时已经提高基本上所有这些通过加载真实设备 IOS 的模拟器都是基于 dynamips 的，是它提供了供 iso 运行的环境，然后其他的软件就是让用户界面更有好些，相比 dynagen 的命令行 GNS3 的图形界面就更有好了，操作更方便了。对于 GNS3 的学习基本上自己摸索出来的，可以自己用图形界面配置了然后看看对配置文件产生了哪些更改从而对软件的运行有更深的了解。

什么是 GNS3？

基于图形界面的网络设备模拟器，可以模拟思科路由器、交换机（路由的交换模块）、PIX 和 ASA 等设备，最大的优势是加载真实的 ios 镜像文件，命令和配置和真实设备一样。它是一下三个组件的集合：

- dynamips   提供 ios 的运行环境
- dynagen   基于文本的 dynamips 的前端界面
- qemu   图形界面的设备模拟器，虚拟机

GNS3 的配置文件在哪？

GNS3 的配置文件主要包括两个部分，一个是软件的配置文件，在 edit-\>preferences 下可以看到配置文件在 C:Documents
and SettingsAdministratorApplication
Data 下的 gns3.ini，这个文件主要负责软件的全局配置比如 dynamips 和 qemu 的运行参数以及可以加载的 ios 的相关配置；另一个是工程（project）的相关配置，实际上就是相对 dynagen 的 net 文件也是拓扑的核心文件，这里面的配置选项不细列举了，可以参考 dynagen 的文档有关于这些选项的详细配置，其中几个比较关键的部分：

- workingdir = D:GNS3top..tmp  --\>
  指定工作目录，所有产生的临时文件都放于这个目录下
- cnfg = D:GNS3confccnpP1R2.cfg  --\>
  指定配置文件，当在路由器上执行了配置并保存，配置文件中就会有这条指令，下次再载入路由器自动导入相应配置，减少劳动力，所以这是一个很好的特性。但是有时候我们需要在不同环境对对相同的拓扑加载不同的配置，这时候如果配置文件自动加载了就不能再加载不同的配置文件，所以需要用\#注释掉响应的配置文件选项。
- 其他的由软件自动生成就可以不需要动

GNS3 的配置配置建议？

实际上 GNS3 是绿色软件，唯一不够绿的地方就是软件的配置文件在 C:Documents
and SettingsAdministratorApplication
Data 不能更改，如果要移动 GNS3 需要把这个文件也转移了。下面是我对 GNS3 配置的心得：

1.  在软件根目录下新建 img（存放镜像文件）、top（存放工程文件也就是拓扑文件也就是 net 文件）、conf（针对相同拓扑不同配置环境的不同配置）、tmp（临时文件目录存放各种临时文件）
2.  将 dynamips、qemu 和抓包工具 wireshark 的临时文件目录都指向 tmp 文件
3.  将 image directory 指向 img 目录，project directory 指向 top 目录
4.  路由器 ios 镜像设置建议用 3640，分配 96M 内存，1G 内存跑五六个路由器不成问题

另外推荐一个鸿鹄的详细的 GNS3 视频教程<http://bbs.hh010.com/forum.php?mod=viewthread&tid=36653&highlight=gns3>
