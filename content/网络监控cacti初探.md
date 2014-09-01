Title:  网络监控cacti初探
Date: 2010-12-02 17:01
Author: admin
Category: server
Tags: cacti, monitor, server
Slug: 网络监控cacti初探

什么是cacti？

cacti是一个套基于lamp的网络流量监控软件，也可以监控服务器状态等方面。它是由php编写的完全基于web管理，而且可以安装插件来扩展其功能和监控对象的范围，有做好的模板可供使用简化了配置。

cacti有哪些组成部分？

[![cacti-componets](http://www.xdays.info/wp-content/uploads/2010/12/cacti-componets.jpg "cacti-componets")](http://www.xdays.info/wp-content/uploads/2010/12/cacti-componets.jpg)

由上图可以看出，cacti是调用mysql,rrdtool,net-snmp来实现监控的，net-snmp定时轮询设备采集信息，将采集的信息写入rrd文件中，而mysql负责记录这些数据的对应关系以及其他相关的配置信息。当用户请求查看相应设备流量时，cacti查询mysql然后调用rrdtool来完成绘图。

如何安装配置？

关于安装可以参考官方手册，具体见参考链接。对于配置，大体上是先建立设备，然后添加相应的模板，然后创建相应的图形，最后再编辑一下自己的监控列表树。

下面附张效果图：

[![cacti-monitor](http://www.xdays.info/wp-content/uploads/2010/12/cacti-monitor.jpg "cacti-monitor")](http://www.xdays.info/wp-content/uploads/2010/12/cacti-monitor.jpg)

参考链接：

官方手册从安装到配置<http://docs.cacti.net/manual:087>

中文文档<http://www.docin.com/p-12395104.html>

详细的中文文档<http://www.docin.com/p-47052887.html>
