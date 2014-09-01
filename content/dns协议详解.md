Title: DNS协议详解
Date: 2013-10-14 16:44
Author: admin
Category: protocol
Tags: dns
Slug: dns协议详解

基本概念
========

树
--

树是一种数据结构，用来表达一种一对多的关系，一图胜千言。

![tree](http://www.xdays.info/wp-content/uploads/2013/10/dns-tree.png)

**注意：** 图选自《大话数据结构》

需要对树结构的几点说明：

-   根节点没有父节点，叶节点没有子节点
-   节点间不能有交叉
-   很多应用树结构的应用场景，如linux目录结构等

域名
----

顾名思义，就是一个域的名字。其格式说明如下：

-   以点分隔，每个字段最长63个字符，总长度最多255个字符（包括点）
-   域名中可以使用任意的ASCII字符，但是有些自负需要转义（000到040,177到377和不做分隔符的点）​
-   域名既可以表示一个域也可以表示一个主机，其实可以表示主机是因为它就是子域的根节点，如hp.com  
    ​

域命名空间
----------

用树结构表示出来的互联网所有域名数据就是域的命名空间。再来一张图说明下：

![domain
namespace](http://www.xdays.info/wp-content/uploads/2013/10/dns-model.png)

需要对命名空间有几点说明：

-   命名空间的根是root用点来表示，严格来说所有的域名最后都有个点，因为都有所以省略了
-   每个子树对应一个域
-   把域名用点拆开，然后从右向左从明明空间从上向下就能找到对应的叶节点

资源记录
--------

虽然归根结底DNS就是提供域名到IP的对应关系的服务，但是域名也分为不同的类型，比如授权服务器信息，邮件服务器信息等，下边我们列举下常见资源记录类型。

-   A ipv4地址
-   AAAA ipv6地址
-   NS 授权DNS地址
-   MX 邮件服务器地址
-   CNAME 别名记录
-   PTR 反向解析记录

详细的介绍参考[DNS Resource
Records](http://www.zytrax.com/books/dns/ch8/)

区域
----

就是zone文件，有相应的RFC规范来定义zone文件如何记录相关资源。

### 域和区域的区别

-   域是一个模型概念，区域是一个配置上的概念
-   域包含了一个或者多个区域
-   没有授权的话域和区域包含的范围就一样了  
    ​

授权
----

授权是DNS协议的核心概念，授权就是现实世界的明确分工，你需要管理的就是明确你手下的人的职责，然后能让需求方找到该找的人就可以了，也就是说如果有人问你请帮我写个脚本，你会告诉他你去找bash吧，他是专门写脚本的。

-   一个域下的域名既可以授权给子域又可以不授权给子域直接自己管理
-   授权下去之后，你就只需要管理授权信息就够了  
    ​

反向解析
--------

-   反向解析就是把IP地址树挂在in-addr.arpa节点下
-   IP地址反向写，因为高位IP地址应该位于树的上端，这样与域名的结构保持一致，如192.168.1.0/24这个地址段的记录对应的zone为1.168.192.in-addr.arpa  
    ​

超时时间
--------

超时时间（TTL）就是缓存的寿命，DNS为了提高响应时间和缩短请求路径而创建了缓存机制，域名服务器在向外查询的时候先查询本机的缓存，没有命中才走正常的递归解析。

解析方法
--------

-   解析器没有追踪的能力，所以不能通过解析器来来递归解析
-   域名服务器通过查找最精确的域授权来发起递归解析请求，这样能保证查询路径最短

数据包
======

请求包
------

![dns
request](http://www.xdays.info/wp-content/uploads/2013/10/dns-query.png)

响应包
------

![dns
response1](http://www.xdays.info/wp-content/uploads/2013/10/dns-response-1.png)  
![dns
response2](http://www.xdays.info/wp-content/uploads/2013/10/dns-response-2.png)

解析流程
========

![dns
procedure](http://www.xdays.info/wp-content/uploads/2013/10/dns-procedure.gif)

1.  用户电脑的解析器向LDNS发起域名解析请求，查询www.google.com的IP地址
2.  在缓存没有命中的情况下，LDNS向根服务器查询www.google.com的IP地址
3.  根告诉LDNS，我不知道www.google.com对应的IP，但是我知道你可以问com域的授权DNS，这个域归他管
4.  LDNS向com的授权服务器问www.google.com对应的IP地址
5.  com告诉LDNS，我不知道www.google.com对应的IP，但是我知道你可以问google.com域的授权DNS，这个域归他管
6.  LDNS向google.com的授权服务器问www.google.com对应的IP地址
7.  google.com查询自己的zone文件，找到了www.google.com对应的IP地址，返回给LDNS
8.  LDNS本地缓存一份记录，把结果返回给用户电脑的解析器

解析方法
========

递归解析
--------

即recursion，上小节详细分析的过程就是递归解析，特点是所有的任务都由LDNS完成，压力在LDNS上。

迭代解析
--------

即iteration，每个环节收到解析请求后，再从自身发起请求，就这这样一级一级的把请求转发下去，直到收到响应后再一级一级的把相应转发回来，因为不是目前主流的解析方式就不展开说了。
