Title: vitualenv
Date: 2013-01-04 00:01
Author: admin
Category: python
Tags: python
Slug: vitualenv

简介
====

virtualenv是用于隔离Python开发环境的工具。

特点
====

-   解决依赖同一项目的不同版本问题
-   没有root权限不能向系统安装包

基本原理
========

类似chroot的模式，virtualenv在项目目录下创建供python运行的基本系统目录结构，然后把python解释器和pip放到对应的目录下，然后通过修改对应的环境变量来达到执行对应程序的目的。

安装使用
========

    sudo apt-get install virtualenv
    virtualenv test
    source test/bin/activate
    which python;which pip

扩展
====

-   [virtualenvwrapper](http://www.doughellmann.com/projects/virtualenvwrapper/) 一个shell脚本对virtualenv相关命令进行了封装，更容易使用。常用命令如mkvirtualenv,lssitepackages,workon,deactivate等
-   [pythonbrew](http://https//github.com/utahta/pythonbrew) 一个可以不需root权限安装多个版本python环境的工具

参考链接
========

<http://www.virtualenv.org/> <http://www.jeffkit.info/2011/08/1012/>
<http://blogs.360.cn/blog/how-360-uses-python-1-virtualenv/>
<https://github.com/utahta/pythonbrew>
