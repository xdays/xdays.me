---
title: RPM包制作
date: 2012-12-07
author: admin
category: linux
tags: linux, rpm
slug: rpm包制作
---

工厂简介
========

RPM为Redhat Package
Manager缩写，是一个为Redhat系列Linux生产软件包的小工厂。其产品是RPM包，包含一些归档文件和meta信息;这些meta信息用来记录如何安装和删除这些文件，一些帮助脚本，文件属性和描述行信息（如包依赖哪些包和被哪些包依赖）。整个RPM包的制作过程严格按照SPEC文件规范的执行，然后通过rpmbuild命令来解析SPEC文件生成对应的RPM包。

生产车间
========

制作RPM的工厂包括四个实体生产车间，也就是目录结构如下：rpmfactory/{SOURCES,BUILD,SPECS,RPMS,SRPMS}；SOURCES是原材料车间用于存放程序的源代码，通常是以.tar.gz后缀结尾的，且压缩前后的的文件名要符合SPEC文件的命令规则，通常是name-version.tar.gz；BUILD是生产车间，是临时目录，主要用于在RPM制作过程中生成临时文件，编译和链接都是在此目录下完成的；SPEC是整个工厂的控制核心车间，所有RPM包的特性都是由次目录下的spec文件来控制的；RPMS是成品车间，此目录下按架构存放对应的rpm包文件；SRPMS是半成品车间，此目录下存放封装好的srpm文件，需要到目标系统上去生产然后安装的。此外有一个目录必须要提下，就是\$BUILDROOT目录，在rpm包的生产过程中除了编译和链接外也进行了安装，只是没有安装到系统中去，而是安装到了\$BUILDROOT目录下，此目录必须提供。

生产线流程
==========

RPM这家工厂虽不是很大，但自动化很高，简要说下这家工厂的生产线，源码包作为原材料被放到SOURCES目录下，首先解压源码包得到源码目录，如果需要就打上适当的patch;然后传送至BUILD目录下开始生产主要进程一些配置和编译操作;接着生产完成，需要将中间临时产品安装，这里安装不是安装到系统上去，而是将\$BUILDROOT当作系统的根来安装这个临时产品；如果所有这些都通过就将成品写入RPM和SRPM文件，分别放到成品车间RPMS和半成品车间SRPMS

厂规厂纪
========

一个高自动化的工厂肯定有一套完善的规范供每个车间执行，这就是SPEC文件的语法，其控制着RPM制作过程的方方面面，主要包含由一些macro构成的描述信息,
%prep, %build, %check, %install, %clean, %file和%changelog,
最后还有Scriptlets脚本段（包括%pre和%post，%preun和%postun，%pretrans和%posttrans）。

描述信息
--------

-   Name 软件名称
-   Version 软件版本
-   Release 软件分支
-   Summary 一句话介绍
-   Group 软件所属组
-   License 软件产权
-   URL 软件主页
-   Source 源码位置
-   Patch Patch位置
-   BuildArch 编译架构
-   BuildRoot 安装目录,重要
-   BuildRequires 编译依赖包
-   Requires 安装依赖包
-   %description 详细的介绍信息
-   %define 用来定义和修改macro变量，macro变量用%{macro}来引用

安装前处理%prep
---------------

-   %setup 便捷的解压macro
-   %patch 便捷的打patch工具

编译处理%build
--------------

-   %build 通常是./configure && make

测试处理%check
--------------

-   %check通常是make test

安装阶段%install
----------------

-   %install
    特别注意这个阶段是将编译好的软件安装到\$BUILDROOT下，通常是make
    DESTDIR=%{buildroot} install

清理阶段%clean
--------------

-   %clean 主要进程一些安装后的清理工作，比如清理BUILD目录下的临时文件

文件列表%file
-------------

-   此段主要设置安装到系统上的文件和目录的属性，注意所有安装到系统上的文件都要在此段声明，否则制作就不成功。
-   %defattr(<file permissions>, <user>, <group>,
    <directory permissions>)用来定义默认属性
-   %config(noreplace) 用来制定配置，升级是不会被覆盖
-   %attr(mode, user, group) 单独指定属性
-   %doc 指定文件为帮助文档

改动日志%changelog
------------------

-   有特定格式来指定文件变动信息

脚本段Scriptlets
----------------

-   %pre和%post 用于安装前后指定的脚本
-   %preun和%postun 用于卸载前后执行的脚本
-   %pretrans和%posttrans 用于一个事务前后的操作

rpmbuild用法
============

编译选项
--------

-   -ba 构建二进制和源码包
-   -bb 构建二进制包
-   -bp 执行到%prep段
-   -bc 执行到%build段
-   -bi 执行到%install段
-   -bl 通过%file进行列表检查
-   -bs 构建源码包
-   --sign 给软件包签名
-   --rebuild 编译源码包并安装
-   --showrc 查看配置文件内容

rpm用法
=======

通用选项
--------

-   --root 切换根目录

安装选项
--------

-   -i 安装
-   -U 升级
-   -F 存在才升级
-   --force 相当与执行--replacepkgs, --replacefiles, and --oldpackage
-   --test 测试

卸载选项
--------

-   -e 卸载

包选择选项
----------

-   -a 所有包
-   -f 包含文件的包
-   -p 查询一个未安装的包

包查询选项
----------

-   --changelog 查询changelog
-   -c 查询配置文件
-   -i 包信息
-   -l 包含的文件
-   --provides 包兼容性
-   -R 包依赖
-   --scripts 包脚本
-   -s 包状态

验证选项
--------

-   -V 验证包

重建数据库
----------

-   --rebuilddb 重建rpm信息库

查看配置
--------

-   --showrc 查看配置信息

参考链接

-   [Fedora制作教程](http://fedoraproject.org/wiki/How_to_create_an_RPM_package)
-   [淘宝核心团队对spec介绍](http://rdc.taobao.com/blog/cs/?p=43)

