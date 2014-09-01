Title: virtualbox note
Date: 2010-08-01 21:04
Author: admin
Category: tool
Tags: virtualbox
Slug: virtualbox-note

​1. 安装虚拟机virtualbox-3.0.4  

源内的版本2.1.4老了，还是用官方网站上的方法安装最新的版本吧，只是速度有点慢。，官方安装：<http://www.virtualbox.org/wiki/Linux_Downloads>  
1) 添加源：deb <http://download.virtualbox.org/virtualbox/debian> lenny
non-free  
2） 安装公钥：wget -q
<http://download.virtualbox.org/virtualbox/debian/sun_vbox.asc> -O- |
sudo apt-key add -  
3）安装：apt-get install virtualbox-3.0

​2.
找个教程：<http://www.kafan.cn/edu/xuniji/200811012526.html>讲的很详细了，这里只是提一下几个需要特别注意的点：  
1）虚拟机的双向共享剪切板可以实现宿主机与客户机之间的拷贝粘贴。  
2）宿主机的虚拟光驱会作为客户机的物理光驱。  
3）分配共享空间后可以用net use x:
[\\vboxsvrsharename](file://vboxsvr/sharename)打开共享空间。  
4）系统安装完毕之后要安装增强功能，以实现鼠标捕捉及共享剪切板功能。

​3. 读取usb设备  
1）查看vboxusers用户组的GID：sudo cat /etc/group |grep vbox  
2）添加开机挂载项，编辑/etc/fstab，最后添加行：none/proc/bus/usb usbfs
devgid=123,devmode=644 0 0  
3）重启ubuntu  
4. 网络配置  

virtualbox各个版本提供的网络连接方式不一样，最新的3.0.4给了四种连接方式NAT，Bridged
Adapter，Internal和Host-only Adapter，分别来解释一下：  

1）NAT：最简单的联网方式，不需要配置，所以是默认的联网方式。虚拟机就像通过路由器连接到网络，它可以通过整合在虚拟机内的虚拟DHCP服务器来分配IP，虚拟机实际上是以主机IP地址来访问web的，因此虚拟机对外网是不可见的，然而最大的弊端也在于此，主机也就无法到达虚拟机了。但是可以利用port
forwarding端口转接实现访问虚拟机的目的。  
2)Bridged
Adapter：virtualbox用一个设备驱动程序来过滤通过物理网卡的数据，允许virtualbox阻止和添加数据，这样就有效的在虚拟机里创建了一个网络接口。以这种方式接入网络的虚拟机在主机看来是和自己有同等地位的，直接介入网络，但前提是你得给虚拟机分配一个合理的IP。但是我的实验没有成功，可以从虚拟机ping通主机，但是不能从主机ping通虚拟机，可能是virtualbox的局限性造成的。（原来是虚拟机的xp系统的防火墙搞的怪，问题解决了。09.08.23）  
3）Internal：与Bridged
Adapter相似，通过Internal可以直接连接到外网，只是这里的外网是指其他的虚拟机。尽管理论上讲，能用Internal实现的功能都能用Bridged
Adapter实现。但是选择Internal的理由有两点，安全和速度。  
4）Host-only
Adapter：主机多出一个vboxnet0接口，这个接口和虚拟机的网卡直接相连，这就是Host-only模式，主机和虚拟机之间可以互相通信，而虚拟机不可以连接外网。这也是很灵活的一种设置方式，扩展性很好，至于怎么扩展还待研究中。
