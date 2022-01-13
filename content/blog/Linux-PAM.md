---
title: Linux-PAM
date: 2010-07-31
author: admin
category: linux
tags: ['linux', 'pam']
slug: linux-pam
---

### 概述

_Linux-PAM_ (Pluggable Authentication Modules for Linux)是一套供管理员选择的用来验证应用程序用户的共享库，它把权限控制与应用程序分离，你可以随意更改认证方式而不需要重新编译程序，具有很好的灵活性和课拓展性。

### 组成组件

- 模块文件：/lib/security/\*
- 模块配置文件：/etc/security/\*
- PAM 配置文件：/etc/pam.conf 和/etc/pam.d/\*
- 一些 PAM 相关命令如 pam-auth-update 等

### PAM 运行原理

```
 +----------------+
  | application: X |
  +----------------+       /  +----------+     +================+
  | authentication-[---->--\--] Linux-   |--<--| PAM config file|
  |       +        [----<--/--]   PAM    |     |================|
  |[conversation()][--+    \  |          |     | X auth .. a.so |
  +----------------+  |    /  +-n--n-----+     | X auth .. b.so |
  |                |  |       __|  |           |           _____/
  |  service user  |  A      |     |           |____,-----
  |                |  |      V     A
  +----------------+  +------|-----|---------+ -----+------+
                         +---u-----u----+    |      |      |
                         |   auth....   |--[ a ]--[ b ]--[ c ]
                         +--------------+
                         |   acct....   |--[ b ]--[ d ]
                         +--------------+
                         |   password   |--[ b ]--[ c ]
                         +--------------+
                         |   session    |--[ e ]--[ c ]
                         +--------------+
```

图的左边表示一个应用程序:X.  这应用程序有和 Linux-PAM  库的接口并且在认证方面没有什么特别之处. Linux-PAM  函数库  (图的中部)  查询 PAM 配置文件的内容并且装入适用于程序  X  的模块.  这些模块进入四个管理组(  图的中下部)中的一个,并且以它们出现在配置文件中的顺序堆叠起来  .  这些模组由 Linux-PAM 呼叫后,为应用程序执行不同的认证工作  .  需要用户提供或提供给用户的文本信息,可以通过使用应用程序提供的 conversation 函数来交换.

### PAM 管理组

下面是 manual 中简短说明：

```
Simply put, these groups take care of different aspects of a typical
user´s request for a restricted service:

account - provide account verification types of service: has the user´s
password expired?; is this user permitted access to the requested
service?

authentication - authenticate a user and set up user credentials.
Typically this is via some challenge-response request that theuser must
satisfy: if you are who you claim to be please enter your password. Not
all authentications are of this type, there exist,hardware based
authentication schemes (such as the use of smart-cards and biometric
devices), with suitable modules, these may be substituted seamlessly for
more standard approaches to authentication - such is the flexibility of
Linux-PAM.

password - this group´s responsibility is the task of updating
authentication mechanisms. Typically, such services are strongly coupled
to those of the auth group. Some authentication mechanisms lend
themselves well to being updated with such a function. Standard UN\*X
password-based access is the obvious example: please enter a replacement
password.

session - this group of tasks cover things that should be done prior to
a service being given and after it is withdrawn. Such tasks include the
maintenance of audit trails and the mounting of the user´s home
directory. The session management group is important as it provides both
an opening and closing hook for modules to affect the services available
to a user.
```

### 配置文件

在/etc/pam.conf 里：

```
service-name   module-type           control-flag   module-path   arguments
服务名称           模块类型（管理组）控制标志      模块路径       模块参数
```

这里仅讨论基本控制标志：

- required;  需要的,这表明此模块返回成功值对于整个 module-type 的成功是必要的.  此模块的返回失败并不会传回给用户，直到剩下的模块(同样 module-type)都执行过.
- requisite;  必要的,类似  required,  只不过,  当这类模块返回失败时,整个控制会立刻回到应用程序.  返回值同第一个需要的或必要的模块返回的失败相同.
- sufficient;  充分的,与 requisite 恰恰相反，这模块返回的成功会被认为已经   充分满足 Linux-PAM  库确认这类模块(module-type)是成功的条件.  如果没有先前的 requisite  模块返回了失败,那么不再会有其它'堆叠'  的模块被呼叫. (注意,  这种情况下,随后的 requisite  模块就不会   被呼叫.).  这模块返回的失败不会看作是致命的错误而至影响应用程序从这 module-type  得到成功的结果.
- optional;  可选的,正如这名字一样,此 control-flag  致使模块对最终的成功或失败的结果不会产生决定性的影响.
  通常用于显示信息，并不在应用方面.

在/etc/pam.d/的配置文件类似。

具体模块一起参数和配置文件

### 参考链接

参考文档：  
[The Linux-PAM System Administrators' Guide](http://debian.securedservers.com/kernel/pub/linux/libs/pam/Linux-PAM-html/Linux-PAM_SAG.html)  
[The Linux-PAM System Administrators' Guide(中文版)](http://www.chinaunix.net/jh/4/390136.html)
