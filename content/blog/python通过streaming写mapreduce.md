---
title: Python写MapReduce
date: 2013-03-17
author: admin
category: python
tags: hadoop, mapreduce, python
slug: python通过streaming写mapreduce
---

说明
====

本文以一个没有Java开发经验的运维角度从宏观上去理解Hadoop的云计算（也就是MapReduce）框架模型的一些思想和运行流程；主要目的是在对MapReduce有一定了解后能用Python通过streaming工具来写MapReduce。

MapReduce工作流程
=================

如下图所示：

![MapReduce
Flow](/wp-content/uploads/2013/03/mapreduce_flow.png)

概括整个过程如下：

1.  客户端启动一个作业；
2.  客户端向JobTracker请求一个job id；
3.  客户端将运行作业所需的资源复制到HDFS上；
4.  客户端将作业提交给JobTracker；
5.  JobTracker初始化作业对象，获取输入数据进行拆分作业；
6.  JobTracker与TaskTracker保持心跳，将子作业下发给TaskTracker；
7.  Tasktracker从HDFS获取数据进行MapTask和ReduceTask

具体的流程介绍可参考[这篇文章](http://weixiaolu.iteye.com/blog/1474172)或者《Hadoop权威指南》

Shuffle机制
===========

Shuffle意思是洗牌或搞乱，在整个MapReduce工作流程中Shuffle指的是map开始之后至Reduce完成之前的这个环节。理解其内部运行机制后，你会对那句形容Shuffle的话理解更深刻：排序是Hadoop的灵魂。

具体Shuffle的介绍参考[这篇文章](http://langyu.iteye.com/blog/992916)，好文，作者分析的通俗易懂，这里鄙人表示感谢。

MapReduce数据流
===============

理解数据流对写MapReduce很重要。总结来说就是：数据始终以key/value形式从input流向output，在input端map有相应的转换方式定义如何将数据转换为key/value形式（针对我们这里说的以行计的日志，Hadoop会将行的偏移量作为key，以一行的实际内容作为value），中间的Shuffle阶段也是针对key进行一个排序，尽可能的减少磁盘IO和网络带宽，最后的output段，reduce程序也是以key/value形式输出结果到HDFS。

具体数据流可大致参考[这篇文章](http://www.cnblogs.com/spork/archive/2010/01/11/1644342.html)

用Streaming写MapReduce
======================

这里我用Python来写map和recduce程序，其他语言也类似。

mapper.py
---------

    #!/usr/bin/env python

    import sys

    hosts = ['221.176.86.150', '221.182.235.210', '221.182.238.74']

    for line in sys.stdin:
        line = line.strip()
        segs = line.split('|')
        if segs[1] in hosts:
            print '%s;%s,%s' % (segs[1], segs[2], 1)

reducer.py
----------

    #!/usr/bin/env python

    from operator import itemgetter
    import sys

    current_key = None
    current_vlaue = 0
    key = None

    for line in sys.stdin:
        line = line.strip()
        segs = line.split(',', 1)
        key = segs[0]
        value = segs[1]

        try:
            value = int(value)
        except ValueError:
            continue

        if current_key == key:
            current_value += value
        else:
            if current_key:
                print '%s,%s' % (current_key, current_value)
            current_key = key
            current_value= value

    if current_key == key:
            print '%s,%s' % (current_key, current_value)

运行命令
--------

    hadoop jar 
    $HADOOP_HOME/contrib/streaming/hadoop-streaming-1.0.3.jar 
    -file /path/to/mapper.py -mapper /path/to/mapper.py 
    -file /path/to/reducer.py -reducer /path/to/reducer.py 
    -input  /hadoop/path/*.gz 
    -output /hadoop/output/ 
    -jobconf stream.non.zero.exit.is.failure=false 
    -jobconf stream.recordreader.compression=gzip

说明：

-   file制定对应的map和reduce程序；
-   input制定input数据路径；
-   output制定output结果路径；
-   `stream.non.zero.exit.is.failure=false`避免程序返回值不为0导致的任务失败；
-   `stream.recordreader.compression=gzip`指明处理的数据为压缩格式。

