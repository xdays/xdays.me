Title: OpenLDAP构建统一认证之安装配置
Date: 2014-05-15 18:04
Author: admin
Category: arch
Tags: arch, ldap
Slug: openldap构建统一认证之安装配置

安装OpenLDAP
============

ubuntu
------

确保本机有符合FQDN的主机名，因为安装程序会根据主机名提取域来作为baseDN

    apt-get install slapd

安装过程中会提示设置管理员密码

centos
------

    yum install slapd

配置OpenLDAP
============

slapd.conf和cn=config
---------------------

配置slapd服务有两种方式：  

* slapd.conf是传统方式，修改配置文件然后重启服务，centos默认采用这种方式。  
* cn=config是新的配置方式，称之为on-line configuration，ubuntu默认采用这种方式。

配置TLS
=======

自签名证书
----------

    mkdir /etc/ldap/certs
    openssl genrsa -out ldap.key 1024
    openssl req -new -key ldap.key -out ldap.csr
    openssl x509 -req -days 1095 -in ldap.csr -signkey ldap.key -out ldap.crt

更新配置
--------

### 编写配置数据文件

    dn: cn=config
    replace: olcTLSCertificateFile
    olcTLSCertificateFile: /etc/openldap/certs/ldap.crt
    -
    replace: olcTLSCertificateKeyFile
    olcTLSCertificateKeyFile: /etc/openldap/certs/ldap.key

### 导入配置

    ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f tls.ldif

修改启动选项
------------

slapd加上`-h ldaps:///`选项即可。

参考资料
========

-   http://my.oschina.net/5lei/blog/193484
-   http://mosquito.blog.51cto.com/2973374/1098456
-   http://bneijt.nl/blog/post/connecting-to-ldaps-with-self-signed-cert-using-python/

