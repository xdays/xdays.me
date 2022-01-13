---
title: Linux-服务管理
date: 2010-07-20
author: admin
category: linux
tags: ['linux']
slug: linux服务管理
---

### 概述

服务就是跑在后台的程序；linux 的服务主要分为独立启动的和依靠 super
daemon(xinetd)来启动两种；系统依靠 shell 脚本来管理服务的启动与停止；另外系统又一套机制负责管理服务的访问权限；最后服务的管理离不开响应的工具。

### 服务管理脚本

系统的服务管理脚本主要位于/etc/init.d/(redhat)或者/etc/rc.d/init.d/(debian)下，脚本的结构基本上是：脚本的描述、环境调用、搜寻配置文件、加载 functions、服务的启动停止与加载、最后还会有脚本的参数。然后在需要运行该服务的 runlevel 下建立对应的软连接，由 init 程序在开机时负责在对应的 runlevel 下启动对应的服务。

### 服务访问控制

#### 验证是否支持

服务的访问的前提条件是服务加载了 libwrap.so 模块，可以通过如下命令查看服务是否支持访问控制

    ldd $(which sshd) | grep libwrap

#### hosts.allow 和 hosts.deny 格式

    ssh:192.168.1.0/255.255.255.0:allow
    服务名:要匹配的客户端地址:处理规则

更为详尽的规则参考权威的手册

    #man 5 hosts_access
    #man 5 hosts_options

### 服务管理工具

- <span style="color: #000000;">ntsysv</span>
- <span style="color: #000000;">sysv-rc-conf</span>
- <span style="color: #000000;">BUM</span>

### 服务参考列表

    acpi-support – 你最好使其在S运行等级处于“X”状态。
    acpid – acpi守护程序.这两个用于电源管理，对于笔记本和台式电脑很重要，所以让它们开启。
    alsa – 如果你使用alsa声音子系统，是的，开启它。
    alsa-utils -在我系统里，此服务取代了alsa，所以我关闭了alsa并在S运行等级将此服务开启。**注意**，我所说的“关闭”是指在所有运行等级里面去除所有 “X”。如果在你系统里没有它，没问题。
    anacron – 一个cron子系统，当时间到达时用于执行任何没有被执行的cron作业。当某种cron 作业时间准备好时，很可能你或许已经关闭了你的计算机。打个比方，updatedb被计划在每天2点执行，但是在那个时候，你的计算机是关闭的，然后如果 ananron服务如果是开启的话，它将设法抓起那个updatedb cron… 我将它关闭是因为我不经常关闭我的笔记本，但是否开启此服务完全取决于你。
    apmd – 这是十分困惑我的一个服务。我已经开启了acpid服务，那同时开启apmd有啥好处呢？如果你的计算机不是那么老，甚至不能支持acpi，然后你可以设 法关闭它。无论如何，我是关闭它的。
    atd – 就像cron，一个作业调度程序。我把它关了
    binfmt-support – 核心支持其他二进制的文件格式。我让它开着
    bluez-utiles – 我把它关了因为我没有任何蓝牙设备
    bootlogd – 开启它
    cron – 开启它
    cupsys – 管理打印机的子系统。我没有打印机所以我关闭它了，如果你有打印机，开启他。
    dbus – 消息总线系统(message bus system)。非常重要，开启它。
    dns-clean – 当使用拨号连接，主要用于清除dns信息。我不用拨号，所以我关闭了它。
    我关闭了它。
    fetchmail – 一个邮件接受守护进程，我关闭了它。
    gdm – gnome桌面管理器。 无论如何我关闭它了，因为我将系统用终端引导。如果你想直接引导到图形用户界面，这取决于你。
    gdomap – 事实上我也不知道为什么此服务必需开启。我没有在其他系统见过这个守护程序，所以我将其关闭并且我没觉得我失去了什么。开启它对笔记本或者台式机有任何好 处吗？
    gpm – 终端鼠标支持。如果你觉得你在终端使用鼠标更好，那么在运行等级 1 和2 开启它。那正是你所需要的。
    halt – 别更改它。
    hdparm – 调整硬盘的脚本。我在运行等级 2，3，4，5去除了它但是在S 运行等级添加了它。我觉得早点打开DMA，32bit I/O等等将对其余过程有益。我自己也将原来的脚本精简了一下。如果我知道我正做什么，我觉得做过多的检查没用。相应配置文件是/etc /hdparm.conf。
    hibernate – 如果你的系统支持休眠，把它打开，否则它对你没用。
    hotkey-setup – 此守护进程为你的笔记本建立一些热键映射。支持的制造商包括：HP, Acer, ASUS, Sony, Dell, 和IBM。如果你有那些品牌的笔记本，你可以打开它，否则它或许对你没有任何好处。
    hotplug and hotplug-net #激活热插拔系统是费时的。我将考虑关掉它们。我在的/etc/network/interfaces文件作了很多修改，并将其设置为自动运行，而不是在 热插拔进程期间映射我的无线网卡。所以我可以将它们关掉。我已经测试过了，甚至我将它们关闭，ubuntu仍旧可以检测到我的usb驱动器，我的数码相 机，等等。所以我认为关掉它们是很安全的**注意**如果在关闭热插拔服务以后发现你的声卡部工作了，你可以将服务打开，或者编辑 /etc/modules文件并添加声卡驱动模块。经测试，后者比较快。
    hplip – HP打印机和图形子系统，我将其关闭了。
    ifrename – 网络接口重命名（network interface rename）脚本。听上去很酷但是我把它关掉了。主要用于管理多网络接口名称。虽然我有无线网卡和以太网卡，两者被内核标识为eth0和ath0，所以 此服务对我不是很有用。
    ifupdown and ifupdown-clean – 打开它，它们是开机时网络及口激活脚本。
    inetd or inetd.real – 查看文件/etc/inetd.conf 注释掉所有你不需要的服务。如果该文件不包含任何服务，那关闭它是很安全的。
    klogd – 打开它。
    linux-restricted-modules-common – 你应该去查看下是否你的系统装载有任何受限制的模块。既然我需要madwifi ath_pci 模块，所以我将其开启。受限制的模块可以从/lib/linux-restricted-modules查看到。如果你发现你没有使用任何受限制的模块， 那关掉这个服务没事。
    lvm – 我没有使用逻辑卷所以我将此服务关闭。让它开启如果你 *确实* 有lvm（lvm是逻辑卷管理器在此不再扩充）.
    makedev – 打开它。
    mdamd – Raid管理工具。不使用Raid所以我将此服务关闭。
    module-init-tools – 从/etc/modules加载扩展模块。你可以研究/etc/modules文件查看是否有一些你不需要的模块。通常我们将此服务开启。
    networking – 在启动期间通过扫描/etc/network/interfaces文件增加网络接口和配置dns信息。让它开着。
    ntpdate – 通过ubuntu时间服务器同步时间 。在开机的时候我不需要它，故我关掉了此服务。
    nvidia-kernel – 我自己编译了nvidia驱动，所以此服务对我没用。如果你从受限制模块中使用nvidia驱动，那打开此服务。
    pcmcia – 激活pcmica设备。我将此服务打开在S运行等级而不是分别在2，3，4，5运行等级打开此服务，因为我觉得起先让硬件设备准备更好。如果你在使用没有 pcmica卡的台式机的话，请关闭此服务。
    portmap – 管理像nis，nfs等等之类服务的守护程序。如果你的笔记本或台式机是纯粹的客户端，那么关闭此服务。
    powernowd – 管理CPU频率的客户端程序。主要用于支持CPU speed stepping技术的笔记本。通常如果你在配置一台笔记本，你应该开启此服务。如果是台式机，那此服务应该没有用。
    ppp and ppp-dns – 对我没用，我不使用拨号。
    readahead – **感谢 mr_pouit!** readahead似乎是一种“预加载程序”。在开机时它将一些库文件加载到内存，以便一些程序启动的更快。但是它给启动时间增加了3-4秒。所以，你可 以留着它…或者不。**更新**，经我测试我觉得加载程序没有什么不同。所以我决定关闭此服务。如果你有打开此服务的理由，那就打开它 。
    reboot – 别更改它。
    resolvconf – 按照你的网络状态自动配置DSN信息，我将它打开着。
    rmnologin – 如果发现nologin，那么去除它。此情况不会在笔记本上面发生，所以我摆脱它。
    我不打算在我的笔记本上使用rsync协议，所以我将其关闭
    sendsigs – 在重启和关机期间发送信号。顺其自然。
    single – 激活单用户模式。顺其自然。
    ssh – ssh守护程序。 我需要ssh，所以我将此服务打开。
    stop-bootlogd – 从2，3，4，5运行等级停止bootlogd。顺其自然。
    sudo – 检查sudo 状态。我没在一台笔记本或者台式机客户端上看到任何使用sudo的好处，因此我关闭了它。
    sysklogd – 顺其自然。
    udev and udev-mab – 用户空间dev文件系统（userspace dev filesystem）。好东西，我将它们打开。
    umountfs – 顺其自然。
    urandom – 随机数生成器。可能没什么用处，但是我留着它。
    usplash – 嗯，如果你想看到漂亮的开机画面，顺其自然。无论如何沃关闭此服务了。如果你想关闭它，你也可以编辑/boot/grub/menu.lst文件注释掉 splashimage行，除去开机 splash核心选项。
    vbesave – 显卡BIOS配置工具。它能保存你显卡的状态。我将其开启。
    xorg-common – 设置X服务ICE socket。我将其从在S运行等级开启移动到2，3，4，5，运行等级。如果我引导到单用户模式，那我不需要此服务。在最初引导期间这种方法将不占用时 间。
    adjtimex – 这也是调整核心hw时钟的工具。通常你不会在开机列表中看见它。在非常少有的情况如果你确实在开机进程中看见它了，事出有因，因此最好顺其自然。在我的情 况里，它是关闭的。
    dirmngr – 证书列表管理工具（certification lists management tool）。和gnupg一起工作。你必须看看你是否需要它。在我的情况里，我是关掉它的。
    hwtools – 一个优化irqs的工具。不确定打开它的好处。在我的情况里，我是关掉它的。
    libpam-devperm – 在系统崩溃之后用于修理设备文件许可的一个守护程序。听起来不错，因此我打开它了。
    lm-sensors – 如果你的主板内建一些传感芯片，通过用户空间（userspace）查看hw状态可能是有帮助的。我运行了它，但是它提示“没有发现传感器”，因此我关闭 了此服务。
    mdadm-raid – 作用和mdadm服务相同。用来管RAID设备。如果你没有此类设备，那尽管关掉它好了。
    screen-cleanup – 一个用来清除开机屏幕的脚本。嗯，是否关闭它有你决定。在我的情况里，我打开它了。
    xinetd – 用来管理其他守护进程的一个inetd超级守护程序。在我的系统里，xinetd管理chargen, daytime, echo和time (在 /etc/xinetd.d 目录找到的)，我不关系任何一个，因此我关掉了此服务。如果在xinetd下你确实有一些重要的服务，那打开它。

### 参考链接

挺全面的： <http://www.opsers.org/base/one-day-of-learning-linux-system-services-that-manage.html>

鸟哥经典的：<http://vbird.dic.ksu.edu.tw/linux_basic/linux_basic.php#part5>
