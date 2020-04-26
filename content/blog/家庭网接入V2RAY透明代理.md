---
title: 家庭网接入V2RAY透明代理
date: 2019-08-21
author: admin
category: network
tags: ['v2ray', 'openwrt']
slug: 家庭网接入V2RAY透明代理
---

# 目标

上一篇[V2Ray 透明代理](/V2RAY透明代理/)里详细解释了在 OpenWrt 上配置 V2RAY 作为透明代理，本文提供两种将这种透明代理应用到家庭局域网的两种方式。主要目标有以下几个：

1. 兼容各种设备，比如 IPTV，NAS
2. 接入设备无感知，无需做任何配置
3. 设备间互访不受影响

下图为应用透明代理前我的家庭网拓扑：

![home network before](/wp-content/uploads/2019/08/home-network-before.png)

由于联通路由光猫如果改成光猫的话 IPTV 就不好使了，所以这个猫比如像其名字一样作为家庭网关了。

# 方案 1 嵌套路由器模式

这种方案的网络拓扑图如下：

![home network after1](/wp-content/uploads/2019/08/home-network-1.png)

直接把极路由刷上 OpenWrt 改成路由模式，然后上透明代理就可以了。这种方案优点就是配置成本很小，缺点是电视，IPTV 和 NAS 和手机电脑等设备被分割到了两个局域网内，这就造成了：

1. 只能单向发起通信，比如电脑可以访问 NAS，而 NAS 就不能直接访问电脑了
2. AirPlay 之类的就不好使了，手机没法投屏到电视了

# 方案 2 两个网关模式

这种方案拓扑图如下：

![home network after2](/wp-content/uploads/2019/08/home-network-2.png)

极路由还是工作在 AP 模式，当然也可以把透明代理做在上面。由于我的极路由已经跑了老毛子系统，而且从 NAS 上虚拟出来的 OpenWrt 性能应该比极路由更好一些，所以我就跑了一个 OpenWrt 以单臂路由方式当做透明代理。首先，这个拓扑上所有的设备都跑在一个局域网内，包括极路由，NAS 以及 NAS 上的虚拟机，而且这个局域网里有两个网关路由光猫和 OpenWrt；然后，我要关闭路由光猫的 DHCP 功能，因为这个 DHCP 不满足条件，不能将非本机的的 IP 配置成 DHCP 网关；最后，我需要在 OpenWrt 上做如下的配置：

1. 默认的 DHCP 配置让所有的设备的网关指向了 OpenWrt
2. OpenWrt 要配置一个静态地址，而且默认路由要指向路由光猫
3. 我们可以配置 DHCP 来根据 mac 地址来让部分设备的网关直接指向路由光猫，这样对于不需要翻墙的电视和 IPTV 就绕过了 OpenWrt 直接出去了。

现在我们来配置下 OpenWrt：

```bash
# 在lan接口上开启DHCP
uci set dhcp.lan.ignore='0'
uci set dhcp.lan.start='100'
uci set dhcp.lan.limit='99'

# 配置静态IP并且默认路由指向联通路由光猫
uci set network.lan.proto='static'
uci set network.lan.ipaddr='192.168.1.200'
uci set network.lan.netmask='255.255.255.0'
uci set network.lan.gateway='192.168.1.1'
uci set network.lan.dns='192.168.1.1'

# 匹配特定mac地址，对它们分配特殊的网关地址
uci set dhcp.iptv=host
uci set dhcp.iptv.name='iptv'
uci set dhcp.iptv.tag='free'
uci set dhcp.iptv.mac='2c:55:d3:ab:86:64' 'c8:0e:77:75:ea:b3'
uci set dhcp.free=tag
uci set dhcp.free.dhcp_option='3,192.168.1.1'

uci commit
service dnsmasq restart
```

## 方案 3 单路由器模式

这种方案拓扑图如下：

![home network after3](/wp-content/uploads/2019/08/home-network-3.png)

首先，修改联通路由光猫改成桥接模式让其只作为猫使用，具体可以参考[这个帖子](https://www.v2ex.com/t/583187#reply35)，具体方法如下：

1. 进 http://192.168.1.1/hidden_version_switch.gch ，选 default version，密码 CUAdmin
2. 机器自动重启之后就可以进 http://192.168.1.1/cu.html 了， 选管理员账户，密码 CUAdmin
3. 进去之后删掉之前的 internet 配置，然后新建 internet bridge，vlan 选项记得选改 tag，然后在 vlan_id 里填 3961（这里是北京联通的 vlan_id，我测试是可以的）
4. iptv 那块选 dhcp，vlan_i 填 3964 即可（这步我做了但是 iptv 并不能工作，IPTV 能正常工作的朋友请分享下你的配置吧）

然后极路由作为网关和透明代理，所有的设备都以极路由为网关，而且 DHCP 这块不需要啥特殊配置了。但是路由光猫改成桥接模式后 IPTV 就不好使了，所以这种场景不适合我，如果你不需要 IPTV，那么这种模式最为理想，当然得有个比较牛逼的路由器哇。

# 参考文档

- [利用 Dnsmasq 部署 DHCP 服务](https://www.hi-linux.com/posts/17088.html)
- [DHCP Option Reference](http://www.networksorcery.com/enp/protocol/bootp/options.htm)
- [OpenWrt DNS and DHCP configuration](https://openwrt.org/docs/guide-user/base-system/dhcp)
- [OpenWrt DNS and DHCP configuration examples](https://openwrt.org/docs/guide-user/base-system/dhcp_configuration)
