Title: CCNP-Switch-Security
Date: 2011-03-26 16:19
Author: admin
Category: ccnp
Tags: ccnp, cisco, switch-security
Slug: ccnp-switch-security

-   交换机安全的知识框架
    -   MAC层的攻击及解决方案
    -   MAC扩散
    -   解决方案
-   Vlan层攻击及解决方案
    -   vlan跳跃攻击
    -   解决方案
    -   vlan流量控制
    -   Pvlan部署
    -   隔离端口
-   欺骗攻击
    -   DHCP欺骗（DHCP spoofing）
    -   解决方案
    -   盗地址
    -   解决方案
    -   ARP欺骗
    -   解决方案

 

### 交换机安全的知识框架

<table border="1" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td colspan="2" width="253" valign="top">
威胁类型

</td>
<td width="315" valign="top">
应对措施

</td>
</tr>
<tr>
<td colspan="2" width="253" valign="top">
MAC层攻击

</td>
<td width="315" valign="top">
端口安全（基于mac允许和拒绝，阻止单播扩散）

</td>
</tr>
<tr>
<td rowspan="3" width="111" valign="top">
vlan攻击

</td>
<td width="142" valign="top">
vlan跳跃

</td>
<td width="315" valign="top">
所有非trunk置于access

</td>
</tr>
<tr>
<td width="142" valign="top">
vlan流量控制

</td>
<td width="315" valign="top">
RACL，VACL和PACL

</td>
</tr>
<tr>
<td width="142" valign="top">
Pvlan和隔离端口

</td>
<td width="315" valign="top">
限制相同网段主机之间访问

</td>
</tr>
<tr>
<td rowspan="3" width="111" valign="top">
spoofing（欺骗）攻击

</td>
<td width="142" valign="top">
DHCP spoofing

</td>
<td width="315" valign="top">
DHCP snoop（监听）

</td>
</tr>
<tr>
<td width="142" valign="top">
盗地址

</td>
<td width="315" valign="top">
IPSG（ip source guard）源防护结合DHCP snoop

</td>
</tr>
<tr>
<td width="142" valign="top">
arp spoofing

</td>
<td width="315" valign="top">
DAI动态ARP检测结合DHCP snoop

</td>
</tr>
</tbody>
</table>
 

### MAC层的攻击及解决方案

#### MAC扩散

主机更改MAC地址发送大量帧，交换机的CAM表被填充满了就会泛洪接下来接收到的帧，这样就影响了网络的性能。

#### 解决方案

端口安全：包括限制方法和违规行为两方面的内容；限制方法包括允许特定数量的mac地址的数据通过和如何学习这些MAC地址（静态配置和sticky粘滞）；当超过时则发生违规，违规包括关闭（也就是err-disable状态），限制（发送SNMP警告信息）和保护。

基于mac阻止流量：显示的配置命令组织特定MAC地址的帧通过接口。

阻止单播帧扩散：不需要从配有端口安全的端口扩散出单播帧，所以通过命令显示丢弃。

### vlan攻击及解决方案

#### vlan跳跃攻击

1）通过发送DTP报文和交换机建立trunk，非法主机能看到发往不同vlan的流量。

2）给帧打两层标签，并且两层标签的vlan不同，交换机去掉第一层标签后会把帧发往另一个vlan。

#### 解决方案

避免建立trunk的机会因为实现vlan跳跃都用到了trunk链路，所以务必把trunk端口之外的端口配成access端口。

#### vlan流量控制

有三种控制表可以应用于vlan：RACL是传统访问控制表；VACL可以控制通过SVI的流量，除了转发和丢弃外还可以重定向以用作监控流量，具体见配置实验部分。

#### Pvlan部署

Pvlan可以更灵活的控制接入端口之间的流量，可以做到同在一个网段内的终端那些可以相互访问，哪些不能相互访问的关系。由于现在没有支持Pvlan的设备，此部分略去。

#### 隔离端口

隔离端口实现了Pvlan的一个功能就是，让同在一个网段的终端之间不能互访，可以通过命令达到要求。

### 欺骗攻击

#### DHCP欺骗（DHCP spoofing）

因为配置有自动获取地址的终端会采纳先接收到的DHCP响应报文（offer），而且这个过程没有什么验证机制。那么非法接入的DHCP服务器就可以随意的分配地址扰乱正常网络的进行，这中攻击叫DHCP欺骗。

#### 解决方案

采用DHCP
snoop窥探技术，基本原理是：在交换机上设置信任端口和非信任端口，信任端口可以收发DHCP报文，而非信任端口仅仅能接收DHCP请求报文丢弃其他的；可以在非信任端口上配置限制流量，防止发生DOS攻击；交换机建立DHCP绑定表，记录的IP，MAC，端口，vlan信息等信息。

#### 盗地址

如果仅开启了DHCP
snoop特性，那么如果非法主机直接填地址而不通过DHCP获取仍然可以访问网络。

#### 解决方案

结合HDCP snoop窥探，IPSG（ip source
guard，ip源防护）可以通过拿主机的二层和三层地址和HDCP绑定表对比来决定是否转发流量。

#### ARP欺骗

主机总是把最后一次接受的ARP信息加入到自己的ARP表中，这是产生ARP欺骗的根本原因。参考下图，非法主机C通过发送ARP让主机A和B的ARP表中相互之间的三层地址对应的MAC地址指向C的MAC地址，这成为中间人攻击。

#### 解决方案

DAI（dynamic arp inspection，动态ARP检测）结合DHCP
snoop，其原理是：配置信任端口和非信任端口，非信任端口不能发出request，心热端口可以收发ARP报文；收到数据包和DHCP绑定表对比，一致则为合法流量转发，否则属于违规采取相应的措施；可以在非信任端口上配置限制流量，防止发生DOS攻击。

 

 
