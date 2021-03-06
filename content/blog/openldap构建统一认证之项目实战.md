---
title: OpenLDAP构建统一认证之项目实战
date: 2015-12-26
author: admin
category: server
tags: ['server', 'ldap']
slug: openldap构建统一认证之项目实战
---

# 背景

## 问题

登录服务器的账号分散在所有的机器上，这样就带来两个问题：

1. 维护成本高，需要专门在 playbook 里定义用户权限
2. 没有明确的权限划分
3. 不便于和其他系统（如 Google Apps）对接

## 需求

1. 数据集中管理
2. 根据用户组控制用户的登陆权限
3. 控制用户的 sudo 权限，只有 operation 有 sudo 的权限
4. 自动创建家目录
5. Web 管理界面

## 原则

- 尽可能少的涉及组件，减少维护成本
- 尽可能的不入侵系统配置，便于恢复

# 配置

## 服务端

### OpenLDAP 安装配置

关于 OpenLDAP 的安装可以参考[OpenLDAP 构建统一认证之安装配置](//openldap构建统一认证之安装配置/)

### LAM 安装配置

关于 LAM 安装配置可以参考[OpenLDAP 构建统一认证之管理工具](//openldap构建统一认证之管理工具/)

### 管理账号

```
dn: olcDatabase={2}bdb,cn=config
changetype: modify
replace: olcSuffix
olcSuffix: dc=example,dc=com

dn: olcDatabase={2}bdb,cn=config
changetype: modify
replace: olcRootDN
olcRootDN: cn=admin,dc=example,dc=com

dn: olcDatabase={2}bdb,cn=config
changetype: modify
replace: olcRootPW
olcRootPW: {SSHA}1Ahx2TU+7DrRzk6eJMNIk2pPaxKsS+Om # generated by ldappasswd
```

使配置生效

    ldapmodify -Y EXTERNAL -H ldapi:/// -f example.ldif

### ssh 公钥

为了配合客户端支持 ssh 的公钥登陆，我们需要为 LDAP Server 添加 openssh-lpk 的 schema，由于最新的 OpenLDAP 都是 olc 模式来管理服务器配置，所以所有的 schema 需要通过 LDIF 的通用格式导入，这里我找到了一个能和 sssd 以及 LAM 配合的 schema：

```
dn: cn=openssh-lpk,cn=schema,cn=config
objectClass: olcSchemaConfig
cn: openssh-lpk
olcAttributeTypes: ( 1.3.6.1.4.1.24552.500.1.1.1.13 NAME 'sshPublicKey'
    DESC 'MANDATORY: OpenSSH Public key'
    EQUALITY octetStringMatch
    SYNTAX 1.3.6.1.4.1.1466.115.121.1.40 )
olcObjectClasses: ( 1.3.6.1.4.1.24552.500.1.1.2.0 NAME 'ldapPublicKey' SUP top AUXILIARY
    DESC 'MANDATORY: OpenSSH LPK objectclass'
    MAY ( sshPublicKey $ uid )
    )
```

然后导入该 schema

    ldapadd -Y EXTERNAL -H ldapi:/// -f openssh-lpk.ldif

然后给 LAM 添加上 ssh key 的模块即可用来管理 public key

### sudo 权限

和 ssh 公钥一样，sudo 权限也需要添加相应的 schema，如下的 LDIF 是我根据官方的 schema 转换而来的。

```
dn: cn=sudoRole,cn=schema,cn=config
objectClass: olcSchemaConfig
cn: sudoRole
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.1
   NAME 'sudoUser'
   DESC 'User(s) who may  run sudo'
   EQUALITY caseExactIA5Match
   SUBSTR caseExactIA5SubstringsMatch
   SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.2
   NAME 'sudoHost'
   DESC 'Host(s) who may run sudo'
   EQUALITY caseExactIA5Match
   SUBSTR caseExactIA5SubstringsMatch
   SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.3
   NAME 'sudoCommand'
   DESC 'Command(s) to be executed by sudo'
   EQUALITY caseExactIA5Match
   SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.4
   NAME 'sudoRunAs'
   DESC 'User(s) impersonated by sudo'
   EQUALITY caseExactIA5Match
   SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.5
   NAME 'sudoOption'
   DESC 'Options(s) followed by sudo'
   EQUALITY caseExactIA5Match
   SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.6
   NAME 'sudoRunAsUser'
   DESC 'User(s) impersonated by sudo'
   EQUALITY caseExactIA5Match
   SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.7
   NAME 'sudoRunAsGroup'
   DESC 'Group(s) impersonated by sudo'
   EQUALITY caseExactIA5Match
   SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.8
   NAME 'sudoNotBefore'
   DESC 'Start of time interval for which the entry is valid'
   EQUALITY generalizedTimeMatch
   ORDERING generalizedTimeOrderingMatch
   SYNTAX 1.3.6.1.4.1.1466.115.121.1.24 )
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.9
   NAME 'sudoNotAfter'
   DESC 'End of time interval for which the entry is valid'
   EQUALITY generalizedTimeMatch
   ORDERING generalizedTimeOrderingMatch
   SYNTAX 1.3.6.1.4.1.1466.115.121.1.24 )
olcAttributeTypes: ( 1.3.6.1.4.1.15953.9.1.10
    NAME 'sudoOrder'
    DESC 'an integer to order the sudoRole entries'
    EQUALITY integerMatch
    ORDERING integerOrderingMatch
    SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 )
olcObjectClasses: ( 1.3.6.1.4.1.15953.9.2.1 NAME 'sudoRole' SUP top STRUCTURAL
   DESC 'Sudoer Entries'
   MUST ( cn )
   MAY ( sudoUser $ sudoHost $ sudoCommand $ sudoRunAs $ sudoRunAsUser $ sudoRunAsGroup $ sudoOption $ sudoNotBefore $ sudoNotAfter $ sudoOrder $ description ))
```

然后导入该 schema：

    ldapadd -Y EXTERNAL -H ldapi:/// -f sudoers.ldif

由于 LAM 的 sudo 管理模块是收费的，所以只能自己手动添加 sudo 策略，示例 LDIF 文件如下：

```
dn: ou=sudoers,dc=example,dc=com
objectClass: top
objectclass: organizationalUnit
ou: sudoers

dn: cn=operation,ou=sudoers,dc=example,dc=com
objectClass: top
objectClass: sudoRole
cn: operation
sudoUser: %operation
sudoHost: ALL
sudoRunAsUser: ALL
sudoCommand: ALL
sudoOption: !authenticate
```

导入该配置：

    ldapadd -D 'cn=admin,dc=example,dc=com' -W -H ldapi:/// -f sudo.ldif

### ACL 配置

该配置主要是允许用户修改自己的密码

```
dn: olcDatabase={2}bdb,cn=config
changetype: modify
add: olcAccess
olcAccess: to attr=userPassword by self =xw by anonymous auth by * none

dn: olcDatabase={2}bdb,cn=config
changetype: modify
add: olcAccess
olcAccess: to * by * read
```

导入该配置：

    ldapmodify -Y EXTERNAL -H ldapi:/// -f acl.ldif

## 客户端（手动）

### NSS 交由 sssd 管理

编辑/etc/nsswitch.conf

```
passwd:         compat sss
group:          compat sss
shadow:         compat sss

hosts:          files dns
networks:       files

protocols:      db files
services:       db files

ethers:         db files
rpc:            db files

netgroup:       nis sss
sudoers:        files sss
automount:  files sss
```

### 配置 PAM

配置 PAM 主要为了解决两个问题，一个是用户认证走 SSSD，另一个是自动创建用户家目录。

CentOS 系统编辑/etc/pam.d/system-auth

```
auth        sufficient    pam_sss.so use_first_pass
account     [default=bad success=ok user_unknown=ignore] pam_sss.so
password    sufficient    pam_sss.so use_authtok
session     optional      pam_sss.so
```

然后执行如下命令开启自动创建家目录

    authconfig --enablemkhomedir --update

**注意** 此配置需要关闭 SELinux

Ubuntu 系统无需配置，sssd 已经帮我们做了。除了为了能自动创建家目录，需添加如下行到/etc/pam.d/common-session 即可

    session required        pam_mkhomedir.so umask=0022 skel=/etc/skel

### 配置 SSSD

编辑/etc/sssd/sssd.conf

```
[sssd]
config_file_version = 2
services = nss, pam, ssh, sudo
domains = example
debug_level = 3

[nss]
filter_users = root,ldap,named,avahi,haldaemon,dbus,radiusd,news,nscd

[domain/example]
debug_level = 9
ldap_id_use_start_tls = True
ldap_tls_reqcert = never
cache_credentials = True
ldap_schema = rfc2307
id_provider = ldap
auth_provider = ldap
chpass_provider = ldap
ldap_uri = ldaps://dir.example.com
ldap_search_base = dc=example,dc=com
ldap_user_ssh_public_key = sshPublicKey
sudo_provider = ldap
ldap_sudo_search_base = ou=sudoers,dc=example,dc=com
access_provider = simple
simple_allow_groups = operation,login
```

### 配置 SSHD

编辑/etc/ssh/sshd_config

```
AuthorizedKeysCommand /usr/bin/sss_ssh_authorizedkeys

```

## 客户端（Ansible）

具体请参考我的这个[Ansible Role](https://github.com/xdays/ansible/tree/master/roles/ldap)

# 参考链接

- http://www.zytrax.com/books/ldap/ch6/slapd-config.html
- https://wiki.gentoo.org/wiki/Centralized_authentication_using_OpenLDAP
- http://www.openldap.org/doc/admin24/
- http://web.mit.edu/kerberos/krb5-latest/doc/admin/index.html
- http://serverfault.com/questions/653792/ssh-key-authentication-using-ldap
- http://vaab.blog.kal.fr/2010/03/06/how-to-add-a-schema-in-openldap-24/
- http://www.ossramblings.com/using-ldap-to-store-ssh-public-keys-with-sssd
- https://lists.fedorahosted.org/pipermail/sssd-users/2013-March/000456.html
- http://linux.die.net/man/5/sudoers.ldap
- https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Identity_Management_Guide/users.html#homedir-pammod
- http://support.hp.com/us-en/document/c03737146
- http://thornelabs.net/2013/01/28/linux-restrict-server-login-via-ldap-groups.html
