---
title: VMware 虚拟化架构理解
date: 2010-10-03
author: admin
category: server
tags: vmware, 虚拟化
slug: vmware-虚拟化架构理解
---

花了一上午研究了一下VMware的虚拟化产品，总体感觉挺混乱的。一开始搞不清头绪，参考了一些资料，才大体明白了怎么回事。[陈前辈](http://hi.baidu.com/chenshake/blog/category/%D0%E9%C4%E2%BB%AF)的博客里相关资料让帮我明白了好多，在此谢过。因为仅仅是一个初步的了解，只总结些基本概念，以后真正用到再深入学习吧！

什么是虚拟化？

通俗说就是用软件虚拟硬件，从而实现在单一的物理硬件平台之上运行多个操作系统，充分利用硬件资源，提高了计算机的工作效率。

VMware虚拟化架构？

[![vi3-1](/wp-content/uploads/2010/10/vi3-1.jpg "vi3-1")](/wp-content/uploads/2010/10/vi3-1.jpg)参考上图，VMware
vSphere是虚拟化平台的最新版本，它包括了VMware ESX 4.1和VMware vCenter
Server 4.1等组件。而上一个版本是VMware Infrastructure
3（简称VI3），主要包括VMware ESX 3.5和VMware vCenter Server
2.5等组件。如果再大的环境下可能要像下图所示的架构添加存储网络。

[![vi3-2](/wp-content/uploads/2010/10/vi3-2.gif "vi3-2")](/wp-content/uploads/2010/10/vi3-2.gif)[  
](/wp-content/uploads/2010/10/vi3-1.jpg)

VMware ESX
：从上图也可以看出，他就是运行在硬件上的虚拟层，调度硬件，虚拟机运行在其上。  
VMware vCenter Server :配置管理虚拟化基础架构的的中心。

文档资料?

可以参考官方的demos，如果要安装评估版本需要注册，在现在页面上有demos信息。

此外，还有HA，DRS，Consolidated
Backup，VMtion功能有待学习，初步了解就到此为止了。

参考资料：<http://hi.baidu.com/chenshake/blog/item/ff4444ee26eb78fab3fb953f.html>  
百度，谷歌
