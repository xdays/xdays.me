Title: 主流Linux版本自动化安装
Date: 2013-08-11 16:21
Author: admin
Category: linux
Tags: linux, kickstart, preseed
Slug: 主流linux版本自动化安装

概述
====

目前主流的发行版本（Redhat和Debian系列）都有相应的自动化安装的工具：Redhat有kickstart，Debian有preseed。其作用都类似，通过预先生成或者写好的配置文件来配合系统安装程序，回答安装过程中需要交互问题来实现自动化安装。

自动化安装配置
==============

kickstart
---------

-   所有的ks文件配置项参考[官方文档](http://fedoraproject.org/wiki/Anaconda/Kickstart)
-   在系统安装完成之后，/root/下会有一个anaconda-ks.cfg文件，此文件是根据手动安装时的配置生成的ks文件，可供下次使用
-   如果手头没有ks文件可以通过“Kickstart Configurator
    application”来创建一个，交互式图形界面工具。

**注意：** `%post`这个版块，可以写一些定制脚本。

preseed
-------

-   对debian系的安装不太了解，没有找到相关配置项的详细说明，很遗憾
-   debian的[自动化安装文档](http://www.debian.org/releases/stable/amd64/apb.html.zh-cn)以及[sample文件](http://www.debian.org/releases/wheezy/example-preseed.txt)
-   ubuntu的[自动化安装文档](https://help.ubuntu.com/lts/installation-guide/i386/appendix-preseed.html)以及[sample文件](https://help.ubuntu.com/12.04/installation-guide/example-preseed.txt)

**注意：**
`d-i preseed/late_command string`这个版块，和kickstart的`%post`的类似，执行定制脚本的。

自动化安装规划
==============

-   我觉得自动化安装系统和配置管理可以是自动化运维的两个子模块，相互独立。
-   系统自动化安装后的初始化（如主机名，IP地址，源设置等）等需要一个能提供相关API的核心信息库来配合：定制化脚本汇报给信息库信息，信息库记录反馈信息并且可以基于反馈信息返回定制脚本需要的信息。

