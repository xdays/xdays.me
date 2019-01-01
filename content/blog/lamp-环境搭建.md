---
title: lamp 环境搭建
date: 2010-09-26
author: admin
category: server
tags: lamp, sever
slug: lamp-环境搭建
---

注：一下是在百度文库中找到的资料，写的不错，步骤简明扼要。

一、拷贝软件到服务器（Discuz、UCenter、mysql、
php、apache、ZendOptimizer）

二、修改远程登录显示乱码

1.编辑：/etc/sysconfig/il8n

2.把UTF-8改成GB2312

关闭selinux

使用文本编辑工具打开 /etc/selinux/config把 SELINUX=enforcing
注释掉：\#SELINUX=enforcing ，然后新加一行为：SELINUX=disabled  
保存，关闭。  
重启系统。

三、关闭不需要的服务（discuz可选）

\# ntsysv

以下仅列出需要启动的服务，未列出的服务一律推荐关闭：

atd ,crond ,irqbalance ,microcode\_ctl ,network ,sendmail ,sshd ,syslog
,,snmpd (cacti时启用) ,snmptrapd（cacti时启用）

四、重启

\#init 6

五、安装mysql

1.如果有老版本的rpm包，给他卸载了

\# rpm -qa |grep mysql
查看系统中是否已经安装了MySQL，如果是卸载所有以mysql开头的包.

\# rpm -e mysql-5.0.45-7.el5 --nodeps

--nodeps：参数安装和卸载的时候不考虑依赖关系

​2. 解压

\#tar -zxvf mysql-5.0.56.tar.gz -C /usr/local/src/

-C: 解压到制定目录

3.进入目录

\# cd /usr/local/src/mysql-5.1.30/

​4. 配置安装 (配置前先建立一个mysql文件夹)

\# ./configure --prefix=/usr/local/mysql/  
\> --with-extra-charsets=all  
\> --sysconfdir=/etc 配置文件的路径

（出现Thank you for choosing MySQL!就成功了）

以下可选：

--localstatedir=/usr/local/mysql/data 数据库存放的路径  
\> --enable-assembler 使用一些字符函数的汇编版本  
\> --with-mysqld-ldflags=-all-static 以纯静态方式编译服务端  
\> --with-charset=utf8 添加utf8字符支持  
\> --with-extra-charsets=all 添加所有字符支持

--with-plugins=all
如果从源代码编译安装mysql,缺省安装时,是没有innodb引擎的.所以,在configure的时候,要加入--with-
plugins=all(或者max),这样才会支持innodb.在mysql里可以执行show
engines命令来查看当前的mysql服务器所支持的存储引擎.

5 make

6 make install

7 拷贝一个配置文件，当作以后mysql的配置文件

\# cp /usr/local/mysql/share/mysql/my-large.cnf /etc/my.cnf（出现cp:
overwrite \`/etc/my.cnf'?
y问是否覆盖，因为rpm装过所以有一个原来的，选择y是）

！这里添加一个选择项，如果没有用rpm装过，那么系统本身不会有mysql的用户和组，所以要自己建立。

\#groupadd mysql

\#useradd -g mysql -d m/usr/local/var mysql

注意：my.cnf里注释掉skip-federated新版本不需要这个参数了。如果需要这个引擎的在编译的时候要加上--with-plugins=federated,在my.cnf里用federated参数就行了。  
先修改my.cnf,再初使化数据库,要不然过不去的。

8 改Mysql用户的宿主目录

\# vi /etc/passwd 找mysql用户，把宿主目录的路径改成/usr/local/mysql/var
（var文件夹要自己建立\# mkdir /usr/local/mysql/var）

建立完了用ll -d var/看下文件夹的属性，发现属主和属组不对，应该是mysql

9 改mysql用户宿主目录的属主和属组

chown -R mysql:mysql /usr/local/mysql/var/

-R:递归处理

10 切换到mysql用户

\# su - mysql

11 初始化mysql服务器中的数据库，也就是安装数据库

\$ /usr/local/mysql/bin/mysql\_install\_db

12 修改MySQL的最大连接数

\# vi /etc/my.cnf

//添加以下行

[mysqld]  
set-variable=max\_connections=1000  
set-variable=max\_user\_connections=500

set-variable=wait\_timeout=200

//max\_connections设置最大连接数为1000

//max\_user\_connections设置每用户最大连接数为500  

//wait\_timeout表示200秒后将关闭空闲（IDLE）的连接，但是对正在工作的连接不影响

13 启动mysql

\$ /usr/local/mysql/bin/mysqld\_safe & （出现Starting mysqld daemon with
databases from /usr/local/var，多按几下回车）

停止mysql

\# /usr/local/mysql/bin/mysqladmin -u root -p shutdown  
13 测试下是否运行

\$ netstat -tnl |grep 3306 （看到 3306 就是mysql
的默认端口，显示3306端口表示成功启动了mysql）

14 登陆mysql

1).如果在root用户下：先给root用户设置密码：

\#/usr/local/mysql/bin/mysqladmin -u root password "这里写密码"

\# /usr/local/mysql/bin/mysql -uroot -p （加-p参数是要求输入密码）

2).如果还在mysql用户下：

\$ mysql -uroot
(如果找不到mysql命令，那么就用绝对路径/usr/local/mysql/bin/mysql -uroot)

3).显示所有数据库：mysql\> show databases;

4).创建数据库：mysql\> create database cacti; cacti是数据库名字

5).删除数据库：mysql\> drop database cacti;

6).给mysql的root用户设置密码，（默认root用户是没有密码的）

mysqladmin -u root password 密码

这时，以后在登录就给用：mysql -u root -p 然后输入密码的方式登录了。

q:退出

15 设置自动启动

1). su - 换成管理员身份

\# echo "/usr/local/bin/mysqld\_safe &" \>\> /etc/rc.local

more /etc/rc.local 查看是否添加成功

2）.这是另外一种方法

在MySQL二进制包里面有一个叫myslq.server的启动脚本程序。把它复制到/etc/rc.d/init.d目录里面

\#cp /usr/local/src/mysql-5.0.56/support-files/mysql.server
/etc/rc.d/init.d/mysqld （cp: overwrite \`/etc/rc.d/init.d/mysqld'?
y询问是否覆盖，选y是）

修改/etc/rc.d/init.d/mysqld文件的权限

\# chmod 700 /etc/rc.d/init.d/mysqld

使用 chkconfig  
\#chkconfig --level 35 mysqld on

\# chkconfig --list mysqld

六、安装apache

1 查看gcc环境：\#rpm -q gcc

2 将源码包拷贝到/usr/local/src/目录下

\#mv httpd-2.2.9.tar.gz php-5.2.6.tar.gz /usr/local/src/

3 解压

\#tar zxvf httpd-2.2.9.tar.gz

4 进入目录

\#cd httpd-2.2.9

5 新建apache2文件夹

mkdir /usr/local/apache2

6 编译前的配置

\#./configure --prefix=/usr/local/apache2 --enable-so --enable-rewrite

--prefix=:指定apache安装的目录（如果不指定，就安装到=/usr/local目录下）  
--enable-so ：开启动态加载模块功能  
--enable-rewrite:开启rewrite功能  
--enable-ssl 支持ssl套接字层

7 编译程序

\#make

8 安装已编译好的程序

\#make install

9 apache启动

\#/usr/local/apache2/bin/apachectl start

查看：\#ps -All |grep httpd

在浏览器测试一下，因该能看见：It works!

安装GD库 http://blog.sina.com.cn/s/blog\_517e2e1b0100ejyg.html

七、以模块方式安装php

1 解压

\# tar -zxvf php-5.2.6.tar.gz -C /usr/local/src/

-C ：配合tar命令，把源码包释放到指定目录

2 进入目录

\# cd /usr/local/src/php-5.2.6

3 编译前配置

\# cd php-5.2.6/  
[root@localhost php-5.2.6]\# ./configure --prefix=/usr/local/php5  
\> --with-apxs2=/usr/local/apache2/bin/apxs  
\> --with-config-file-path=/usr/local/php5  
\> --with-mysql=/usr/local/mysql/  
\> --with-gd  
\> --enable-gd-native-ttf  
\> --with-libxml-dir=/usr/local/libxml2  
\> --with-zlib-dir=/usr/local/zlib  
\> --with-freetype-dir=/usr/local/freetype  
\> --with-jpeg-dir=/usr/local/libjpeg  
\> --with-png-dir=/usr/local/libpng  
\> --enable-xml  
\> --enable-sockets  
\> --enable-mbstring

--with-apxs2 ：设置php为apache服务器提供的模块安装的位置  
--with-config-file-path ：设置php程序的配置文件所在位置。  
--with-mysql=/usr/local/mysql/：设置php为mysql提供模块的位置  
--with-gd:这样安装的是php自带的gd库  
--enable-gd-native-ttf //激活对本地 TrueType 字符串函数的支持  
--with-freetype-dir=/usr/local/freetype //激活对 FreeType 2.x 的支持  
--with-jpeg-dir=/usr/local/libjpeg //激活对 jpeg-6b 的支持  
--with-png-dir=/usr/local/libpng //激活对 png 的支持  
--enable-xml //支持XML  
--enable-sockets //支持套接字  
--enable-mbstring //安装phpmyadmin时用  
--with-mcrypt //安装phpmyadmin时用,php传输加密方法

4 编译和安装

\#make ；make install

5 拷贝模板配置文件

因为安装完成后，还没有配置文件，所以把php源码包里的php.ini-dist文件拷贝出来

\# cp php.ini-dist /usr/local/php5/php.ini

6 apache设置

打开apache配置文件：/usr/local/apache2/conf/httpd.conf

看看是否存在这行：LoadModule php5\_module modules/libphp5.so

再加入一行 AddType application/x-httpd-php .php .php4 .php5（加在AddType
application/x-compress .Z

\\.php .php4
.php5意思是以这些扩展名结尾的文件，在apache中用php解析器解析。  
AddType application/x-gzip .gz .tgz下面就行）

再找到 DirectoryIndex关键字：添加 index.php

7 重启apache服务

[root@localhost php5]\# /usr/local/apache2/bin/apachectl stop  
[root@localhost php5]\# /usr/local/apache2/bin/apachectl start

8 测试一下

在/usr/local/apache2/htdocs下建立test.php文件

\<?php  
phpinfo();  
?\>

八、安装ZendOptimizer

1 解压

\# tar zxvf ZendOptimizer-3.3.0a-linux-glibc21-i386.tar.gz -C
/usr/local/src/

2 进入目录

\#cd /usr/local/src/ZendOptimizer-3.3.0a-linux-glibc21-i386

3 安装

./install

然后一路回车，看到这个，php.ini的路径，要写的是目录路径,然后再一路回车

4 测试下，做个php测试页

\# vi /usr/local/apache2/htdocs/testZend.php

5 访问下看看

应该看到，红框里的内容

九、安装eaccelerato0.9.5

1.解压 tar jxvf eaccelerator-0.9.5.3.tar.bz2 -C /usr/local/src
（因为是bz2包，所以要用j，而不用z）

2.进入解压目录

cd /usr/local/src/eaccelerator-0.9.5.3/

3.指定php所在路径

\# export PHP\_PREFIX="/usr/local/php5"

\# \$PHP\_PREFIX/bin/phpize

\# ./configure --enable-eaccelerator=shared
--with-php-config=\$PHP\_PREFIX/bin/php-config

\# make ; make install

这时会将eaccelerator安装到php目录中，屏幕会显示eaccelerator.so所在路径，例如：  
Installing shared extensions:
/usr/local/php5/lib/php/extensions/no-debug-non-zts-20060613/　　记住这个路径。

4.修改php.ini 在最后加入

[eaccelerator]  

extension="/usr/local/php5/lib/php/extensions/no-debug-non-zts-20060613/eaccelerator.so"

eaccelerator.shm\_size="32"  
eaccelerator.cache\_dir="/data/cache/eaccelerator"  
eaccelerator.enable="1"  
eaccelerator.optimizer="1"  
eaccelerator.check\_mtime="1"  
eaccelerator.debug="0"  
eaccelerator.filter=""  
eaccelerator.shm\_max="0"  
eaccelerator.shm\_ttl="0"  
eaccelerator.shm\_prune\_period="0"  
eaccelerator.shm\_only="0"  
eaccelerator.compress="1"  
eaccelerator.compress\_level="9"

解释：

extension"/usr/local/php5/lib/php/extensions/no-debug-non-zts-20060613/eaccelerator.so"

解释：PHP扩展eaccelerator.so的路径。就是上面要记下的绝对路径

--------------------

eaccelerator.shm\_size="32"

解释：eaccelerator可使用的共享内存大小(单位为MB)。

在Linux下，单个进程的最大内存使用量受/proc/sys/kernel/shmmax中设置的数字限制(单位为字节)，例如CentOS
4.4的shmmax默认值为33554432字节(33554432bytes/1024/1024=32MB)。

临时更改该值：  
\# echo 字节数 \> /proc/sys/kernel/shmmax

按照以上方法更改，在每次重启系统时，该值会被自动还原。如果想永久更改，可以修改/etc/sysctl.conf文件，设置：  
kernel.shmmax = 字节数

--------------------

eaccelerator.cache\_dir="/data/cache/eaccelerator"

解释：缓存路径，可以使用命令mkdir -p
/data/cache/eaccelerator创建该目录，然后使用命令chmod 0777
/data/cache/eaccelerator设置该目录权限为0777

--------------------

eaccelerator.enable="1"

解释：打开或者关闭eaccelerator。"1"指打开，"0"指关闭。默认值为"1"。

--------------------

eaccelerator.optimizer="1"

解释：打开或者关闭代码优化，开启可以加快代码的执行速度。"1"指打开，"0"指关闭。默认值为"1"。

--------------------

eaccelerator.check\_mtime="1"

解释：当打开此项时，eaccelerator会在每次请求时检查php文件的修改时间，看其是否被修改过，这会耗费一点时间，如果php文件被修改过，eaccelerator会重新编译缓存该php文件。当关闭此项时，如果php文件被修改，则需要手工删除eaccelerator缓存，才能显示被修改的php文件。"1"指打开，"0"指关闭。默认值为"1"。

--------------------

eaccelerator.debug="0"

解释：打开或者关闭调试记录。当打开时，eaccelerator会将对一个缓存文件的每次请求都写进log。打开此项只对调试eaccelerator是否有BUG时有益处。"1"指打开，"0"指关闭。默认值为"0"。

--------------------

eaccelerator.filter=""

解释：决定哪些PHP文件应该被缓存。可以指定一个范围(比如"\*.php
\*.phtml")，这样被指定的文件就会被缓存。如果该范围以!开头，被指定的文件就不会被缓存。默认值为""，表示缓存所有的PHP文件。

--------------------

eaccelerator.shm\_max="0"

解释：一个用户使用例如eaccelerator\_put之类的函数能够往共享内存中加载的最大数据。默认值为"0"，表示不限制。(单位为字节)

--------------------

eaccelerator.shm\_ttl="0"

解释：当没有足够的空闲共享内存去尝试缓冲一个新脚本时，将删除至少在shm\_ttl秒之前没有被访问过的文件。默认值为"0"，表示不尝试从共享内存中删除任何旧的脚本。(单位为秒)

--------------------

eaccelerator.shm\_prune\_period="0"

解释：当没有足够的空闲共享内存去尝试缓冲一个新脚本时，将删所有旧脚本，前提是这个尝试在超过shm\_prune\_period秒之前被执行过。默认值为"0"，表示不尝试从共享内存中删除任何旧的脚本。(单位为秒)

--------------------

eaccelerator.shm\_only="0"

解释：打开或者关闭在磁盘上缓存编译过的脚本。这个参数对会话数据和内容缓存没有效果。默认值为"0"，表示使用磁盘和共享内存来缓存。

--------------------

eaccelerator.compress="1"

解释：打开或者关闭缓存内容压缩。"1"指打开，"0"指关闭。默认值为"1"。

--------------------

eaccelerator.compress\_level="9"

解释：内存压缩的级别。默认值为"9"，表示最大压缩。

5.建立缓存目录：  
\# mkdir -p /data/cache/eaccelerator  
\# chmod 0777 /data/cache/eaccelerator  
6.重启apache

\# /usr/local/apache2/bin/apachectl stop

\# /usr/local/apache2/bin/apachectl start  
测试下：出现以下表示ok。

十、 安装ucenter

1 解压ucenter

\#unzip UCenter\_1.0.0\_SC\_GBK.zip -d ucenter

-d：解压的目录，不指定-d，解压出来的文件都是分散的。

2 进入ucenter文件夹

\#cd /root/ucenter

3 把upload文件夹放到apache文档目录

\# mv upload/ /usr/local/apache2/htdocs/uc

4 给data文件加777的权限

\#ll -d usr/local/apache2/htdocs/uc/data

\# chmod 777 -R data/

5 安装ucenter

在浏览器里输入http://192.168.254.35/uc/install/

6 填写相关配置

如果没有初始密码，这里就空着

十一、 安装discuz

1 解压discuz

\# unzip Discuz\_6.1.0\_SC\_GBK.zip -d discuz6

2 把upload文件夹放到apache文档目录（随便来个名字）

\# mv upload/ /usr/local/apache2/htdocs/bbs

3 改bbs目录分配777权限

\# chmod 777 -R /usr/local/apache2/htdocs/bbs/

4 安装过程

输入这个http://192.168.254.35/bbs/install/
（不要忘了install，否则会报mysql错误）

补充：

安装phpmyadmin（备忘）

最基本的修改就这几项：  
\$cfg['Servers'][\$i]['controluser'] = 'root';  
\$cfg['Servers'][\$i]['controlpass'] = 'single';  
\$cfg['blowfish\_secret'] = 'cisco'; /\* YOU MUST FILL IN THIS FOR
COOKIE AUTH! \*/

参考链接

<http://cn.php.net/manual/en/install.unix.apache2.php>

<http://www.libgd.org/FAQ>

[](http://www.libgd.org/FAQ)<http://www.libgd.org/FAQ_PHP>[](http://cn.php.net/manual/en/install.unix.apache2.php)
