---
title: Hadoop集群搭建
date: 2013-03-09
author: admin
category: server
tags: ['hadoop', 'server']
slug: hadoop集群搭建
---

# 简介

目前我对 hadoop 的认识主要是如下两点：

- 类似 raid 模式的存储系统，基于软件的容灾；
- 分布式计算，这个是其牛逼之处。

# 安装配置

## 新建用户并配置免密码登录

所有设备上都需要 hadoop 帐号。

    useradd hadoop
    passwd hadoop

配置 ssh 无密码登陆

以 hadoop 用户执行如下命令:

    su - hadoop
    cd
    mkdir .ssh
    ssh-keygen –t rsa
    cd ~/.ssh
    cp id_rsa.pub authorized_keys
    scp authorized_keys ccos-m1:/home/hadoop/.ssh
    scp authorized_keys ccos-m2:/home/hadoop/.ssh

## 安装 JDK

JDK 在每台设备上都要安装。

安装 rpm 包:

    rpm -ivh jdk-6u23-linux-amd64.rpm

编辑/etc/profile.d/java.sh，内容如下:

    export JAVA_HOME=/usr/java/jdk1.6.0_23
    export JRE_HOME=$JAVA_HOME/jre
    export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib:$CLASSPATH
    export PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH
    export HADOOP_HOME=/opt/hadoop
    export PATH=$HADOOP_HOME/bin:$PATH

## 更改 hosts 文件

修改/etc/hosts 内容如下:

    192.168.110.100  centos5-m1
    192.168.110.11 ccos-m1
    192.168.110.12 ccos-m2

## 解压 hadoop 程序

    tar xzf hadoop-1.0.3.tar.gz -C /opt/
    cd /opt/ && ln -s hadoop-1.0.3 hadoop
    chown hadoop:hadoop hadoop-1.0.3 -R

## 配置 hadoop

### 修改运行环境

修改 conf/hadoop-env.sh 如下:

    export JAVA_HOME=/usr/java/jdk1.6.0_23

### 修改核心配置

修改 conf/core-site.xml:

    <?xml version="1.0"?>
    <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

    <!-- Put site-specific property overrides in this file. -->

    <configuration>

    <property>
    <name>hadoop.tmp.dir</name>
    <value>/hadoop</value>
    <description>A base for other temporary directories.</description>
    </property>

    <property>
    <name>fs.default.name</name>
    <value>hdfs://centos5-m1:9000</value>
    <description>The name of the default file system.  A URI whose
    scheme and authority determine the FileSystem implementation.  The
    uri's scheme determines the config property (fs.SCHEME.impl) naming
    the FileSystem implementation class.  The uri's authority is used to
    determine the host, port, etc. for a filesystem.</description>
    </property>

    <property>
    <name>dfs.name.dir</name>
    <value>/hadoop/name</value>
    <description>Determines where on the local filesystem the DFS name node should store the name table. If this is a comma-delimited list of directories then the name table is replicated in all of the directories, for redundancy. </description>
    </property>

    </configuration>

### 修改 HDFS 配置

修改 conf/hdfs-site.xml:

    <?xml version="1.0"?>
    <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

    <!-- Put site-specific property overrides in this file. -->

    <configuration>

    <property>
    <name>dfs.data.dir</name>
    <value>/hadoop/data</value>
    <description>Determines where on the local filesystem an DFS data node should store its blocks. If this is a comma-delimited list of directories, then data will be stored in all named directories, typically on different devices. Directories that do not exist are ignored.</description>
    </property>

    <property>
    <name>dfs.replication</name>
    <value>2</value>
    <description>Default block replication. The actual number of replications can be specified when the file is created. The default is used if replication is not specified in create time.</description>
    </property>

    </configuration>

### 修改 MapReduce 配置

修改 conf/mapred-site.xml:

    <?xml version="1.0"?>
    <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

    <!-- Put site-specific property overrides in this file. -->

    <configuration>

    <property>
    <name>mapred.job.tracker</name>
    <value>centos5-m1:9001</value>
    <description>The host and port that the MapReduce job tracker runs at. If "local", then jobs are run in-process as a single map and reduce task.</description>
    </property>

    </configuration>

## 修改 masters 和 slaves

masters 内容如下:

    centos5-m1

slaves 内容如下：

    ccos-m1
    ccos-m2

## 分发程序文件

拷贝包括 hadoop 程序和 hosts 这些文件；并在所有 datanode 上创建/hadoop/data 目录并指定 hadoop 用户组权限。

## 运行 hadoop

### 格式化 HDFS

    hadoop namenode -format

### 启动守护进程

    start-all.sh

### 查看运行的进程

    jps

## 验证

namenode 地址：http://centos5-m1:50070
jobtracker 地址：http://centos5-m1:50030
