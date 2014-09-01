Title: freeradius&mysql简单配置一例
Date: 2011-01-20 14:02
Author: admin
Category: server
Slug: freeradiusmysql-简单配置

总体说下：

我用的是ubuntu
server，因为他的强大方便的包管理系统，省了好多脑细胞。总体环境是lamp +
phpmyadmin +
freeradius，lamp提供给freeradius数据库和phpmyadmin运行的环境。这里我仅仅实现了基本的功能就是认证，拿的思科交换机开启aaa功能测试，也就是客户端登录交换机先通过freeradius的认证，通过即可操作交换机否则拒绝。

引用一张图：

[![aaacs](http://www.xdays.info/wp-content/uploads/2011/01/AAAbs-1024x804.jpg "aaacs")](http://www.xdays.info/wp-content/uploads/2011/01/AAAbs.jpg)

基于C/S架构，只是这里数据库和freeradius放一台上了。

开始安装：

1）安装lamp

安装系统的时候直接选上lamp环境就行了，需要设置一个mysql密码（这里是thinkin）

2）安装phpmyadmin

apt-get install
phpmyadmin，安装过程时让设置个管理phpmyadmin自身数据库的密码（还是thinkin，其实也没大用处，没考虑安全，直接用的root）

3）安装freeradius

apt-get intall freeradius
freeradius-sql（数据库模块），默认安装没什么问题

开始配置：

首先列举下需要配置的文件radiusd.conf（主配置文件，其他文件都是通过@INCLUDE包含进来的），client.conf（NAS网络接入服务器，对于freeradius来说是客户端的配置文件），sql.conf（数据库相关的配置文件），sites-available/default（默认虚拟主机的配置文件），再者就是mysql数据库中的数据了下面是具体每个文件需要修改的地方：

1）radiusd.conf：找到\$INCLUDE
sql.conf这一行去掉前面的注释，把sql.conf的相关配置包含进来

2）sql.conf：找到如下两行：

login = "radius"

password = "radpass"修改为：

login = "root"

password = "thinkin"其他的默认

3）sites-available/default：去掉authorize {}（授权）和accounting
{}（记账）中的sql一行前的\#，对于认证authenticate
（认证）{}字段中sql已经开启

4）创建导入mysql数据库

\#mysql –u root –p

\#create database
radius（也可用phpmyadmin，但是这里的数据库名必须是radius，和sql.conf对应的）

\#mysql –u root –p \<
/etc/freeradius/sql/mysql/schema.sql（导入数据库模板）

\#insert into radius  (username,attribute,op,value)  values (0,’test’,’
User-Password’,’ :=’,’test’);（添加一个测试用户）后续的添加类似。
