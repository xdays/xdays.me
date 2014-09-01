Title: linux 账户设置
Date: 2010-06-05 10:11
Author: admin
Category: linux
Tags: linux, user
Slug: linux账户设置

### 概述

有关用户帐户的配置文件主要有：/etc/passwd  /etc/shadow  /etc/group
/etc/gshadow，因为里面的一些栏目较多不容易记忆，这里总结一下以作备用。

### /etc/passwd

截取两行:

    root:x:0:0:root:/root:/bin/bash
    bin:x:1:1:bin:/bin:/sbin/nologin

解释如下：  
用户名
：UID：GID（初始用户组，有效用户组用groups查看）：详细信息：家目录：shell类型

### /etc/shadow

截取两行：

    sabayon:!!:14728:0:99999:7:::
     ease:$1$jp36MzdS$VjeTYbbtxe45vbkr9QK581:14728:0:99999:7:::

解释如下：

用户名：密码（如!!是没有设密码，如!是被锁定）：更改密码日期：密码不可更改天数：密码需要重新更改天数：密码更改期限前的警告期限：密码过期的宽限时间：帐号失效日期：保留

注意：这里的日期是一个相对天数，相对于1970.1.1这一天。（通常用chage
－ldmMIE 显示和设置）

### /etc/group

截取两行：

    ease:x:500:
    oprofile:x:16:

解释如下：  
组名：密码：GID：组内成员

### /etc/gshadow

截取两行：

    gdm:x::
    sabayon:x::

解释如下：

组名：密码（!表示不能登录）：管理员：组内成员

另外再说明初始用户组和有效用户组的区别：初始用户组在/etc/passwd中说明；有效用户组用groups查看，建立文档时用有效用户组，更改有效用户组用newgrp命令。
