---
title: Python实现手机控制PC
date: 2013-05-25
author: admin
category: python
tags: develop, python
slug: python实现手机控制pc
---

背景
====

最初想法起因是这样的：晚上睡觉前看电视剧看困了就不想起来关电脑了，所以需要通过手机远程在PC上执行命令。

组件
====

-   服务端提供接受指令和下发指令的两个API
-   手机端用Qpython写脚本向服务端提交指令
-   PC端写一个小daemon程序，获取指令并在本机执行

代码
====

服务端代码
----------

以Django编写，后端用redis存储。

### views.py

    from django.http import Http404, HttpResponse
    from django.shortcuts import render
    from django.views.decorators.csrf import csrf_exempt, csrf_protect
    from xbox.control.forms import order
    from redis_cache import get_redis_connection
    import time
    import json

    @csrf_exempt
    def put_order(request): #用于接收浏览器发来指令的view函数
        flag = True
        date = time.strftime("%Y%m%d%H%M%S", time.localtime())
        if request.method == 'POST':
            con = get_redis_connection('default')
            form = order(request.POST)
            if form.is_valid():
                o = form.cleaned_data['o']
                con.set('0:' + date, o) #0表示带下发指令
            else:
                flag = False
        else:
            flag = False
        return render(request, 'control.html', {'f':order()})

    @csrf_exempt
    def json_order(request): #用于接收手机端发来指令的view函数
        flag = True
        date = time.strftime("%Y%m%d%H%M%S", time.localtime())
        if request.method == 'POST':
            con = get_redis_connection('default')
            print request.raw_post_data
            raw = json.loads(request.raw_post_data)
            con.set('0:' + date, raw['o'])
        else:
            flag = False
        return HttpResponse(flag)

    def get_order(request):
        con = get_redis_connection('default')
        lo =  con.keys('0:*')
        if lo:
            o = con.get(lo[0])
            n = lo[0].replace('0', '1', 1) #1表示已下发的历史命令
            con.rename(lo[0], n)
            return HttpResponse(o)
        else:
            return HttpResponse('echo None')

### forms.py和control.html

略（用于通过浏览器下发指令）

手机端代码
----------

    import urllib2
    import json

    s = 'http://localhost:8000/control/json_order/'
    d = {u'o':u'touch /tmp/foobar.txt'}
    retval = urllib2.urlopen(s, data=json.dumps(d)).read()
    print retval

PC端代码
--------

### PC端daemon.py

这个类写的简单明了，源代码请[参考这里](http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/ "Daemon")

daemon.py代码如下：  
\#!/usr/bin/env python

    import sys, os, time, atexit
    from signal import SIGTERM 

    class Daemon:
        """
        A generic daemon class.

        Usage: subclass the Daemon class and override the run() method
        """
        def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
            self.stdin = stdin
            self.stdout = stdout
            self.stderr = stderr
            self.pidfile = pidfile

        def daemonize(self):
            """
            do the UNIX double-fork magic, see Stevens' "Advanced 
            Programming in the UNIX Environment" for details (ISBN 0201563177)
            http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
            """
            try: 
                pid = os.fork() 
                if pid > 0:
                    # exit first parent
                    sys.exit(0) 
            except OSError, e: 
                sys.stderr.write("fork #1 failed: %d (%s)n" % (e.errno, e.strerror))
                sys.exit(1)

            # decouple from parent environment
            os.chdir("/") 
            os.setsid() 
            os.umask(0) 

            # do second fork
            try: 
                pid = os.fork() 
                if pid > 0:
                    # exit from second parent
                    sys.exit(0) 
            except OSError, e: 
                sys.stderr.write("fork #2 failed: %d (%s)n" % (e.errno, e.strerror))
                sys.exit(1) 

            # redirect standard file descriptors
            sys.stdout.flush()
            sys.stderr.flush()
            si = file(self.stdin, 'r')
            so = file(self.stdout, 'a+')
            se = file(self.stderr, 'a+', 0)
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())

            # write pidfile
            atexit.register(self.delpid)
            pid = str(os.getpid())
            file(self.pidfile,'w+').write("%sn" % pid)

        def delpid(self):
            os.remove(self.pidfile)

        def start(self):
            """
            Start the daemon
            """
            # Check for a pidfile to see if the daemon already runs
            try:
                pf = file(self.pidfile,'r')
                pid = int(pf.read().strip())
                pf.close()
            except IOError:
                pid = None

            if pid:
                message = "pidfile %s already exist. Daemon already running?n"
                sys.stderr.write(message % self.pidfile)
                sys.exit(1)

            # Start the daemon
            self.daemonize()
            self.run()

        def stop(self):
            """
            Stop the daemon
            """
            # Get the pid from the pidfile
            try:
                pf = file(self.pidfile,'r')
                pid = int(pf.read().strip())
                pf.close()
            except IOError:
                pid = None

            if not pid:
                message = "pidfile %s does not exist. Daemon not running?n"
                sys.stderr.write(message % self.pidfile)
                return # not an error in a restart

            # Try killing the daemon process    
            try:
                while 1:
                    os.kill(pid, SIGTERM)
                    time.sleep(0.1)
            except OSError, err:
                err = str(err)
                if err.find("No such process") > 0:
                    if os.path.exists(self.pidfile):
                        os.remove(self.pidfile)
                else:
                    print str(err)
                    sys.exit(1)

        def restart(self):
            """
            Restart the daemon
            """
            self.stop()
            self.start()

        def run(self):
            """
            You should override this method when you subclass Daemon. It will be called after the process has been
            daemonized by start() or restart().
            """

### PC端control.py

control.py代码如下：

    #!/usr/bin/env python

    import sys, time
    import subprocess
    import urllib
    from daemon import Daemon

    class MyDaemon(Daemon):
        def run(self):
            while True:
                order = urllib.urlopen('http://server-get-api/').read()
                subprocess.call(order, shell=True)
                time.sleep(30)

    if __name__ == "__main__":
        daemon = MyDaemon('/tmp/daemon-example.pid')
        if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                daemon.start()
            elif 'stop' == sys.argv[1]:
                daemon.stop()
            elif 'restart' == sys.argv[1]:
                daemon.restart()
            else:
                print "Unknown command"
                sys.exit(2)
            sys.exit(0)
        else:
            print "usage: %s start|stop|restart" % sys.argv[0]
            sys.exit(2)
