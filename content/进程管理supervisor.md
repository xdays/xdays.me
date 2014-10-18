Title: Supervisor进程管理
Date: 2014-10-18 21:36
Author: admin
Category: 
Tags: 
Slug: supervisor进程管理
 
# 功能
优点

* 配置简单
* 管理精准
* 进程组管理
* RPC扩展
* API支持
* FastCGI进程管理
* 事件支持（如定时任务）

缺点

* 被管理进程必须前台运行
* 退出后会使被监管的进程也退出

# 配置

<pre>
[unix_http_server]
file=/var/run/supervisor.sock
chmod=0700

[supervisord]
logfile=/var/log/supervisor/supervisord.log
pidfile=/var/run/supervisord.pid
childlogdir=/var/log/supervisor

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///var/run/supervisor.sock

[program:cow]
command=/web/root/bin/cow -rc="/web/root/etc/cow.conf"
autostart=true
autorestart=true
redirect_stderr=true
stderr_logfile=NONE


[include]
files = /etc/supervisor/conf.d/*.conf
</pre>

# 操作

<pre>
supervisorctl status 查看进程状态
supervisorctl reload 重启supervisord
supervisorctl start|stop|restart 启动关闭重启进程
</pre> 
