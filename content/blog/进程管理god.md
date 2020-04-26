---
title: God进程管理
date: 2014-10-18
author: admin
category: server
tags: ['ha', 'server']
slug: god进程管理
---

# 功能

优点

- 配置即 ruby 代码，灵活
- 可管理后台进程
- 可动态加载配置
- 可根据进程消耗资源重启进程
- 丰富的通知功能，如邮件，campfire 等
- 支持 poll 和 event 两种检测模式

缺点

- 配置复杂，需要 ruby 背景
- 文档太少

# 配置

poll 模式：

```
RAILS_ROOT = "/Users/tom/dev/gravatar2"

%w{8200 8201 8202}.each do |port|
  God.watch do |w|
    w.name = "gravatar2-mongrel-#{port}"
    w.start = "mongrel_rails start -c #{RAILS_ROOT} -p #{port} \
      -P #{RAILS_ROOT}/log/mongrel.#{port}.pid  -d"
    w.stop = "mongrel_rails stop -P #{RAILS_ROOT}/log/mongrel.#{port}.pid"
    w.restart = "mongrel_rails restart -P #{RAILS_ROOT}/log/mongrel.#{port}.pid"
    w.pid_file = File.join(RAILS_ROOT, "log/mongrel.#{port}.pid")
    w.behavior(:clean_pid_file)

    w.start_if do |start|
      start.condition(:process_running) do |c|
        c.interval = 5.seconds
        c.running = false
      end
    end

    w.restart_if do |restart|
      restart.condition(:memory_usage) do |c|
        c.above = 150.megabytes
        c.times = [3, 5] # 3 out of 5 intervals
      end

      restart.condition(:cpu_usage) do |c|
        c.above = 50.percent
        c.times = 5
      end
    end

    # lifecycle
    w.lifecycle do |on|
      on.condition(:flapping) do |c|
        c.to_state = [:start, :restart]
        c.times = 5
        c.within = 5.minute
        c.transition = :unmonitored
        c.retry_in = 10.minutes
        c.retry_times = 5
        c.retry_within = 2.hours
      end
    end
  end
end
```

event 模式：

```
RAILS_ROOT = "/Users/tom/dev/gravatar2"

God.watch do |w|
  w.name = "local-3000"

  w.start = "mongrel_rails start -c #{RAILS_ROOT} -P #{RAILS_ROOT}/log/mongrel.pid -p 3000 -d"
  w.stop = "mongrel_rails stop -P #{RAILS_ROOT}/log/mongrel.pid"
  w.restart = "mongrel_rails restart -P #{RAILS_ROOT}/log/mongrel.pid"

  w.pid_file = File.join(RAILS_ROOT, "log/mongrel.pid")
  # clean pid files before start if necessary
  w.behavior(:clean_pid_file)

  # determine the state on startup
  w.transition(:init, { true => :up, false => :start }) do |on|
    on.condition(:process_running) do |c|
      c.running = true
    end
  end

  # determine when process has finished starting
  w.transition([:start, :restart], :up) do |on|
    on.condition(:process_running) do |c|
      c.running = true
    end

    # failsafe
    on.condition(:tries) do |c|
      c.times = 5
      c.transition = :start
    end
  end

  # start if process is not running
  w.transition(:up, :start) do |on|
    on.condition(:process_exits)
  end

  # restart if memory or cpu is too high
  w.transition(:up, :restart) do |on|
    on.condition(:memory_usage) do |c|
      c.interval = 20
      c.above = 50.megabytes
      c.times = [3, 5]
    end

    on.condition(:cpu_usage) do |c|
      c.interval = 10
      c.above = 10.percent
      c.times = [3, 5]
    end
  end

  # lifecycle
  w.lifecycle do |on|
    on.condition(:flapping) do |c|
      c.to_state = [:start, :restart]
      c.times = 5
      c.within = 5.minute
      c.transition = :unmonitored
      c.retry_in = 10.minutes
      c.retry_times = 5
      c.retry_within = 2.hours
    end
  end
end
```

# 操作

```
god status 查看被监控进程状态
god start|stop|restart 启动关闭重启进程
god load 动态加载配置
god signal 给进程发信号
</pre>
```
