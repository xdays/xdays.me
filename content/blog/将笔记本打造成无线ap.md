---
title: 将笔记本打造成无线AP
date: 2011-05-28
author: admin
category: windows
tags: ['windows', '无线']
slug: 将笔记本打造成无线ap
---

这月的流量包月在前 10 天就用完了，没有网的日子好难熬。今天突然冒出一个想法：手机支持 wifi，笔记本有无线网卡，能不能把笔记本模拟成无线 AP，通过笔记本走 IP 网络？Google 了下找到了如下方法，经本人实验成功，欣喜之情难以言表，哈哈！

以下为转帖原文：[Windows
7 无线 AP 网络](http://tech.chinawin.net/laptop/article-47e9.html)

---

如果你的系统是 Windows
7 操作系统，刚好你的[笔记本电脑](http://www.chinawin.net/tag/bijibendiannao/)无线网卡硬件又支持，那么你就可以简单的组建起一个无线 AP 网络，实现共享上网。

具备以上两个前提条件之后，你将会在“计算机-属性-设备管理器-网络适配器”里面看到有一项“Microsoft
Virtual WiFi Miniport Adapter”，那么在“控制面板网络和
Internet 网络连接”里头也会看到有一个名字为“无线网络连接 2”的连接，这个连接正是使用了 Microsoft
Virtual WiFi Miniport Adapter 硬件。

点击“开始-所有程序-附件-命令提示符”右键点击“以管理员身份运行”，DOS 窗口执行如下两条指令，即可将无线 AP 网络开启：

netsh wlan set hostednetwork mode=allow ssid=Windows7AP key=password  
netsh wlan start hostednetwork

这个 Wi-Fi 无线网络的名字为 Windows7AP，密码是 password；指令中这两参数可以自行更改。

再将你的“本地连接”右键-“属性”-“共享”、在“Internet 连接共享”框框那打勾，选择“无线网络连接 2”。意思为要将你的有线网卡的互联网上网功能，通过无线网络 Windows7AP 共享出去。

之后，你就可以用另外的笔记本电脑、各种支持 Wi-Fi 的手机、iPad、iPod
Touch、iPhone、PSP 等等搜索到这个无线网络，输入密码，就可以 share 上网啦。

Microsoft Virtual WiFi Miniport
Adapter 是微软 Windows7 最新支持的一个功能，目前只能通过 DOS 指令来开启，但是已经令我感到很欣喜。适合经常出差的伙伴，又或者有一大堆
Wi-Fi 电子设备的机迷们，不用你随身携带一台无线路由器，就可以实现互联网共享。

我更喜欢将这两条指令做成一个.bat 批处理文件，瞬间加载，实现 Wi-Fi 网络的快速启动。

Microsoft Virtual WiFi Miniport Adapter，一如谷歌 Android
2.2“冻酸奶”支持的 3G 无线 AP 般前卫。

---
