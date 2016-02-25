Title: OpenLDAP构建统一认证之管理工具
Date: 2014-05-15 18:05
Author: admin
Category: server
Tags: server, ldap
Slug: openldap构建统一认证之管理工具

自带工具
========

**注意：** 如果服务器的ssl证书是自签名的，那么在客户端的ldap.conf文件加入一行`TLS_REQCERT never`，否则认证会不通过。

安装
----

ubuntu执行：

    apt-get install -y ldap-utils

centos执行：

    yum install -y openldap-clients

使用
----

### ldapsearch

ldapsearch，搜索目录树，示例如下：

    ldapsearch -v -x -H ldaps://example.com -D "cn=admin,dc=example,dc=com" -W -W -b "dc=xdays,dc=info" -LL

简单解释下选项的作用： 

* -H 指定服务器url
* -x 使用简单认证
* -D 绑定的DN
* -W 提示输入密码
* -b 指定搜索的baseDN
* -LL 输出LDIF格式
* -v 显示详细信息

### ldapadd

ldapadd，添加数据，要输入标准LDIF文件，示例如下：

    ldapadd -v -x -H ldaps://example.com -D "cn=admin,dc=example,dc=com" -W -f data.ldif

选项与ldapsearch类似， `-f` 指定文件路径

### ldapdelete

ldapdelete，删除数据，要输入标准LDIF文件，示例如下：

    ldapdelete -v -x -H ldaps://example.com -D "cn=admin,dc=example,dc=com" -W -f data.ldif

### ldapmodify

ldapdelete，修改数据，要输入标准LDIF文件，示例如下： 

    ldapmodify -v -x -H ldaps://example.com -D "cn=admin,dc=example,dc=com" -W -f data.ldif

LAM
===

简介
----

一个简单的DLAP账号管理工具，PHP编写，配置写静态文件，安装简单方便。

安装
----

下载程序源码：

    wget -SO ldap-account-manager-4.5.tar.bz2 "http://downloads.sourceforge.net/project/lam/LAM/4.5/ldap-account-manager-4.5.tar.bz2?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Flam%2F&ts=1400145174&use_mirror=jaist"

解压放置web服务器目录下，修改权限（因为配置信息要写到文件里）：

    tar xzf ldap-account-manager-4.5.tar.bz2 && mv ldap-account-manager-4.5 /web/www/lam
    chown -R www-data.www-data lam

php与web服务器配置这里略过

配置
----

首先，拷贝样本配置文件：

    cd config
    cp -a config.cfg_sample config.cfg
    cp -a lam.conf_sample lam.conf

然后，访问web界面，点击右上侧的lam
configuration，默认密码是lam。在general
setting里修改系统的master密码；在server
profile里配置要连接的LDAP服务器信息。这里有两点需要说明：

-   如果服务器为tls加密的那么需要指定ldaps://example.com
-   在general
    setting里要下载服务器的证书，下载完后保存，然后重启php进程。

最后返回登陆界面，用LDAP的账号信息登陆系统，第一次登陆会提示你创建对应的ou等条目，创建完成后创建一个用户组，就可以添加账号了。

优化
----

默认lam用cn来作为RDN，但是好多系统认证的时候都是找uid，所以需要修改为uid，具体配置在tools的user
profile里，修改RDN identifier为uid即可。
