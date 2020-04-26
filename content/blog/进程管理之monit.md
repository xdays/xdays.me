---
title: Monit进程管理
date: 2014-10-18
author: admin
category: server
tags: ['ha', 'server']
slug: Monit进程管理
---

#功能
优点

- 性能高，占用内存少
- 邮件通知
- HTTP 界面
- 检测系统性能参数
- 检测文件属性
- 检测服务状态
- 检测文件系统
- 检测远程主机

缺点

- 没有 API
- 准确性
- 配置复杂

# 配置

```
set daemon 60 # check services at 1-minute intervals
set logfile /var/log/monit.log
set pidfile /var/run/monit.pid
set idfile /var/.monit.id
set statefile /var/.monit.state
set mailserver smtp.xdays.me port 25
  username "admin@xdays.me" password "password"
  #using tlsv1
set mail-format { from: admin@xdays.me }
set alert easedays@gmail.com # receive all alerts

set httpd port 2812 and
    use address localhost
    allow localhost

check system cloud.xdays.me
  if loadavg (1min) > 4 then alert
  if loadavg (5min) > 2 then alert
  if memory usage > 75% then alert
  if swap usage > 25% then alert
  if cpu usage (user) > 70% then alert
  if cpu usage (system) > 30% then alert
  if cpu usage (wait) > 20% then alert

check process nginx with pidfile /var/run/nginx.pid
  start program = "/usr/sbin/service nginx start"
  stop program = "/usr/sbin/service nginx stop"
  if cpu > 60% for 2 cycles then alert
  if cpu > 80% for 5 cycles then restart
  if totalmem > 200.0 MB for 5 cycles then restart
  if children > 250 then restart
  if loadavg(5min) greater than 10 for 8 cycles then stop
  if failed host www.xdays.me port 80 protocol http
    and request "/"
  then restart
  if failed port 443 type tcpssl protocol http
    with timeout 15 seconds
  then restart
  if 3 restarts within 5 cycles then timeout
```

# 操作

```
monit -t 检测配置文件语法
monit reload 重新加载配置文件
monit status 查看服务状态
monit start|stop|restart 启动和关闭服务
</pre>
```
