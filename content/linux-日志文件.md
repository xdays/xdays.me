Title: linux 日志文件
Date: 2010-09-26 12:23
Author: admin
Category: linux
Tags: linux, log
Slug: linux-日志文件

### 概述

日志文件的概念很好理解，就是什么时间，谁，在哪里里，做了什么事。专门有一个叫做syslog(ubuntu采用的拓展的rsyslog)的程序来负责收集系统产生的这些信息，然后按照规则把他们写道特定的地方，这些地方包括文件，控制台，打印机，远程主机等。由于日志文件记录信息逐渐增多，就需要有程序管理日志文件，这就是logrotate。对于这两个程序的认识主要对配置文件的了解。但是最重要的不是这些，而是要能看懂日志信息，这就要对系统，对服务等有个全面的认识，这样才能知道日志文件里说的是怎么一回事。

### syslog配置

#### 语法

语法：服务名称 [运算符] 信息等级         记录信息的位置

#### 服务名称

服务名称：该服务产生的讯息会被纪录的意 思。syslog
认识的服务主要有底下这些：

-   auth, authpriv：主要与认证有关的机制，例如telnet, login, ssh
    等需要认证的服务都是使用此一机制；
-   cron：例行性命令 cron/at 等产生讯息记录的地方；
-   daemon：与各个 daemon 有关的讯息；
-   kern：核心 (kernel) 产生讯息的地方；
-   lpr：打印相关的讯息！
-   mail：只要与邮件收发有关的讯息纪录都属于这个；
-   news：与新闻群组服务器有关的东西；
-   syslog：syslogd 这支程序本身产生的信息啊！
-   user, uucp, local0 \~ local7：与 Unix like 机器本身有关的一些讯息。

#### 运算符

运算符限制了记录信息的范围

-   . ：代表比后面还要高的等级(含该等级)都被记录下来的意思，
    例如：mail.info 代表只要是 mail 的信息，而且该信息等级高于 info
    (含info )时，就会被记录下来；
-   .=：代表所需要的等级就是后面接的等级而已；
-   .!：代表不等于。

#### 信息等级

信息等级：总共分成下列几种等级：

-   info ： 提示一些讯息数据；
-   notice ： 注意！需要比较留意的讯息；
-   waring 或 warn ：
    警示的讯息，以上三个讯息都还是没有错误的情况，虽然是需要留意，但是还没有到错误的情况；
-   err 或 error ： 呀！错误讯息出现了！该要检验错误的问题发生原因了；
-   crit ： 临界点了！再不处理可就伤脑筋了！
-   alert ： 错误讯息一再地警告警告！你将要完蛋了！
-   emerg 或 panic ： 阿！系统已经进入混乱的阶段！真的是完蛋了～～
-   特殊等级：例如 debug （显示较多的信息！）及 none
    （不要记录该服务的内容！）等

#### 记录日志位置

记录信息的位置

-   档案的绝对路径：通常就是放在 /var/log
    里头的档案啦！如果绝对路径后跟“-”表示**异步写入**，这样能提升性能。
-   打印机或其它设备：例如 /dev/lp0 这个打印机装置，/dev/console指控制台
-   使用者名称：如root，显示给使用者啰！另外如果是\*就是告诉所有用户
-   远程主机：例如 @test.adsldns.org

#### 配置文件示例

    # Log all kernel messages to the console.
    # Logging much else clutters up the screen.
    #kern.*                                                 /dev/console

    # Log anything (except mail) of level info or higher.
    # Don't log private authentication messages!
    *.info;mail.none;authpriv.none;cron.none                /var/log/messages

    # The authpriv file has restricted access.
    authpriv.*                                              /var/log/secure

    # Log all the mail messages in one place.
    mail.*                                                  -/var/log/maillog

    # Log cron stuff
    cron.*                                                  /var/log/cron

    # Everybody gets emergency messages
    *.emerg                                                 *

    # Save news errors of level crit and higher in a special file.
    uucp,news.crit                                          /var/log/spooler

    # Save boot messages also to boot.log
    local7.*                                                /var/log/boot.log

### logrotate配置

/etc/logrotate.conf和/etc/logrotate.d/\*

这是一个默认配置文件，也就是如果具体的服务没有具体设置就采用此默认项

    # see "man logrotate" for details
    # rotate log files weekly
    weekly
    # keep 4 weeks worth of backlogs
    rotate 4
    # create new (empty) log files after rotating old ones
    create
    # uncomment this if you want your log files compressed
    #compress
    # RPM packages drop log rotation information into this directory
    #具体程序的配置文件在下面这个目录内，语法规则类似
    include /etc/logrotate.d
    # no packages own wtmp -- we'll rotate them here
    /var/log/wtmp {
    monthly
    minsize 1M
    create 0664 root utmp
    rotate 1
    }
    # system-specific logs may be also be configured here.

### 参考链接

-   鸟哥的站：http://linux-vbird.bluedata.org/linux\_base/0570syslog.htm
-   man syslog.conf 最好的最权威的
-   维基百科 <http://en.wikipedia.org/wiki/Syslog>

