---
title: Zabbix监控MySQL
date: 2015-06-13
author: admin
category: monitor
tags: ['monitor', 'zabbix']
slug: zabbix监控MySQL
---

#安装源

```
rpm -ivh http://www.percona.com/downloads/percona-release/percona-release-0.0-1.x86_64.rpm
rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
rpm -ivh http://repo.zabbix.com/zabbix/2.2/rhel/6/x86_64/zabbix-release-2.2-1.el6.noarch.rpm
```

#安装包

    yum install -y zabbix-agent php php-mysql percona-zabbix-templates

安装的软件包包括：percona-zabbix-templates php php-mysql zabbix-agent apr apr-util apr-util-ldap httpd httpd-tools mailcap php-cli php-common php-pdo zabbix

#配置
##agent 配置
配置 Server 到 192.168.1.7

    sed -i 's/^Server=.*/Server=192.168.1.7/' /etc/zabbix/zabbix_agentd.conf

拷贝配置文件

    cp /var/lib/zabbix/percona/templates/userparameter_percona_mysql.conf /etc/zabbix/zabbix_agentd.d/userparameter_percona_mysql.conf

##PHP 访问数据库权限
新建/var/lib/zabbix/percona/scripts/ss_get_mysql_stats.php.cnf 内容如下：

```
cat >/var/lib/zabbix/percona/scripts/ss_get_mysql_stats.php.cnf <<EOF
<?php
\$mysql_user = "root";
\$mysql_pass = "password";
EOF
```

修改 php.ini 内容如下：

```
sed -i 's@mysql.default_socket =@mysql.default_socket = "/tmp/mysql.sock"@' /etc/php.ini
sed -i 's@mysqli.default_socket =@mysqli.default_socket = "/tmp/mysql.sock"@' /etc/php.ini
```

##脚本访问数据库权限
/var/lib/zabbix/.my.cnf 内容如下：

```
cat >/var/lib/zabbix/.my.cnf <<EOF
[client]
user = root
password = password
EOF
```

##外壳脚本修改
添加如下两行才能保证脚本正常运行：

```
sed -i '/^CACHEFILE/aPATH=/usr/local/mysql/bin/:$PATH\nHOME=/var/lib/zabbix/' /var/lib/zabbix/percona/scripts/get_mysql_stats_wrapper.sh
```

##安全加固

```
chown zabbix.zabbix /var/lib/zabbix/.my.cnf /var/lib/zabbix/percona/scripts/ss_get_mysql_stats.php.cnf
chmod 600 /var/lib/zabbix/.my.cnf /var/lib/zabbix/percona/scripts/ss_get_mysql_stats.php.cnf
```

##启动 agent

    /etc/init.d/zabbix-agent start
