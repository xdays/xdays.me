---
title: Docker基础教程之基本概念
date: 2016-11-14
author: admin
category: container
tags: ['docker']
slug: docker基础教程之基本概念
---

# 简介

本文是整个系列教程的第一篇，我将从一个使用者的角度向你展示其中几个技术：namespace, cgroups, veth, bridge, copy-on-write, image 和 container。整个容器技术的核心包括 namespace 和 cgroup 两个部分，其中 namespace 负责资源隔离，cgroups 负责资源限制。而 Docker 在这两个技术之上提出了几个重要概念让容器技术得以流行。

如果你刚接触 Docker 请参考我另外两篇文章:

- [Docker 初识](//docker初识/)
- [Docker 详解](//docker详解/)

# 安装

官方提供了很方便的安装脚本，只需运行如下命令即可安装完成：

    curl -s https://get.docker.com | bash

# namespace

Namespace 是 Linux 在内核级别的隔离技术，它可以让进城拥有自己独立的进程号，网络，文件系统（类似 chroot）等，不同 namespace 下的进程之间相互不可见。因为系统是通过底层的系统调用来提供 namespace 功能的，所以并没有用户态的管理 namespace 的工具，关于怎么创建具体类型的 namespace 可以参考酷壳的两篇文章[Docker 基础技术：Linux Namespace（上）](http://coolshell.cn/articles/17010.html)和[Docker 基础技术：Linux Namespace（下）](http://coolshell.cn/articles/17029.html)，但是等进程在 namespace 启动之后有时候我们需要进入到进程的运行环境来 debug 等操作。

目前的 Docker 版本已经可以通过 exec 子命令直接切换到进程所在的 namespace：

    docker run -d --name nginx nginx
    docker exec -it nginx ls
    docker exec -it nginx ip a
    docker exec -it nginx ps -ef

如果在早期的版本，或者其他容器引擎的话，可以通过 nsenter：

    yum install util-linux
    PID=$(docker inspect --format {{.State.Pid}} container_name
    nsenter --target $PID --mount --uts --ipc --net --pid

# cgroups

## 简介

有了资源隔离之后，如果不能对各个 namespace 下进程的资源使用做限制的话，那么隔离也没有意义了。所以 Docker 使用 cgroups 另一种内核技术，来实现对进程以及其子进程做资源限制。需要说明是，我们通过本地的文件系统来管理 cgroups 配置，就像修改/sys 目录下的文件内容可以修改内核参数一样。但是在 Docker 引擎这一层已经帮我们屏蔽了底层的细节，我们可以通过 docker 命令很方便的配置 cgroup 相关的参数。

首先查看当前开启的 cgroup 子系统：

```
# mount -t cgroup
# ls /sys/fs/cgroup/*/docker/
```

可以看到 docker 将 container 相关的 cgroup 配置放到了 docker 目录下。

## CPU 子系统

cgroups 提供了三种限制 CPU 资源的方式：cpuset， cpuquota 和 cpushares

### cpuset

cpuset 可以限制进程使用 CPU 的核心数，可以通过 `cpuset/cpuset.cpus` 来管理，对应的 docker 命令为：

        docker run --cpuset-cpus 0 -d --name nginx nginx

### cpuquota

cpuquota 可以以时间片的使用率来限制 CPU 资源，要比 cpuset 的细粒度大一些，只需要设置一个相对 100000 的值就可以达到限制一个百分比的效果, 通过 `cpu/cpu.cfs_period_us` （配置时间片单位，默认为 100000）和 `cpu/cpu.cfs_quota_us` (时间片占比)两个文件来管理， 对应的 docker 命令为:

        docker run --cpu-quota 50000 -d --name nginx nginx

### cpushares

cpushares 可以根据权重来分配 CPU 资源，比如如果只有一个进程权重为 1024，那么进程可以使用 100%的 CPU 资源，如果有两个进程且权重都是 1024，那么每个进程可以使用 50%的 CPU 资源 , 通过 `cpu/cpu.shares` 来管理，对应的 docker 命令为：

        docker run --cpu-shares 1024 -d --name nginx nignx

更多关于 cgroups 的 CPU 子系统的实践可以参考如下链接：

- [Cgroup - 从 CPU 资源隔离说起(一)](https://www.v2ex.com/t/246791)
- [Cgroup － 从 CPU 资源隔离说起（二）](https://www.v2ex.com/t/246792)
- [Cgroup － 从 CPU 资源隔离说起（三）](https://www.v2ex.com/t/246793)

## 内存子系统

cgroups 对内存的限制包括物理内存和 swap 两块，当进程使用内存达到上限的时候会背 kill 掉。关于内存的限制几个文件主要包括:

        memory.limit_in_bytes memory.soft_limit_in_bytes memory.memsw.limit_in_bytes

同样的 docker 帮我们去做底层的管理：

        docker run -m 100m -d --name nginx nginx

需要特殊说明的一点是 docker 默认会将 swap 的限制设置为 2 倍内存，这样你会发现进程实际使用的内存可能会大于 `-m` 设置的内存大小。

## blkio 子系统

blkio 子系统的功能是对块设备读写的速率限制，目前个人还没怎么在这块时间，具体介绍可参考 [Cgroup - Linux 的 IO 资源隔离](https://www.v2ex.com/t/251497)

# veth

veth 是一种特殊的 Linux 网络接口设备，它总是成对出现的，而且发到一端的数据包会从另一端发出来，下边我通过命令演示 docker 里 container 内的网络和 host 的网络是怎么联通的。

```
# 新建一个net namespace
➜  ~ ip netns add test
➜  ~ ip netns list
test
# 新建一对veth网络接口
➜  ~ ip link add veth0-0 type veth peer name veth0-1
➜  ~ ip link list
27: veth0-1@veth0-0: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN mode DEFAULT qlen 1000
    link/ether da:bd:24:5f:e6:a8 brd ff:ff:ff:ff:ff:ff
28: veth0-0@veth0-1: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN mode DEFAULT qlen 1000
    link/ether 36:0f:fc:64:1d:f0 brd ff:ff:ff:ff:ff:ff
# 将veth0-0放到第一步新建的namespace里
➜  ~ ip link set veth0-0 netns test
➜  ~ ip link
27: veth0-1@if28: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT qlen 1000
    link/ether da:bd:24:5f:e6:a8 brd ff:ff:ff:ff:ff:ff link-netnsid 4
# 给namespace里的网络接口配置ip
➜  ~ ip netns exec test ip addr add local 10.0.78.3/24 dev veth0-0
➜  ~ ip netns exec test ip link set veth0-0 up
➜  ~
# 给host上的的网络接口配置ip
➜  ~ ip addr add local 10.0.78.4/24 dev veth0-1
➜  ~ ip link set veth0-1 up
➜  ~ ip a
27: veth0-1@if28: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP qlen 1000
    link/ether da:bd:24:5f:e6:a8 brd ff:ff:ff:ff:ff:ff link-netnsid 4
    inet 10.0.78.4/24 scope global veth0-1
       valid_lft forever preferred_lft forever
    inet6 fe80::d8bd:24ff:fe5f:e6a8/64 scope link
       valid_lft forever preferred_lft forever
# 测试host和namespace网络的连通性
➜  ~ ping 10.0.78.3
PING 10.0.78.3 (10.0.78.3) 56(84) bytes of data.
64 bytes from 10.0.78.3: icmp_seq=1 ttl=64 time=0.115 ms
64 bytes from 10.0.78.3: icmp_seq=2 ttl=64 time=0.054 ms
^C
--- 10.0.78.3 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1000ms
rtt min/avg/max/mdev = 0.054/0.084/0.115/0.031 m

➜  ~ ip netns delete test
```

# bridge

bridge 是另一种 Linux 网络接口设备，你可以把他理解成一个交换机，所有加到这个 bridge 接口上的其他网络接口都在一个大的二层网络上，而 docker 要让同一台机器上所有的 container 相互通信，通过的方式就是将所有在 host 上的的 veth 接口加入到名为 docker0 的 bridge 接口上。

```
docker run -d --name nginx1 nginx
docker run -d --name nginx2 nginx
yum install bridge-utils
brctl show docker0
```

# copy-on-write

copy-on-write 是联合文件系统的机制，联合文件系统是将不同的文件系统的目录聚合在一起的文件系统。我竟让像比人这样解释联合文件系统：想象一下，现在你有几块透明的玻璃，然后你用笔在每块玻璃上写下一些文字，然后将这些玻璃按照一定的顺序叠加在一起，从上往下看去你就能看到所有的文字了；而当你要修改某个文字的时候，你所有的涂改都是在最上边的那块玻璃上发生了，下层的玻璃上的文字只是被覆盖住了而实际上没有任何修改。具体到 Linux 的联合文件系统上呢，当我们需要修改一个文件的内容的时候，操作系统会将这个文件拷贝一份新的放到最上层的目录上然后修改文件，实际上下层的目录并没有改动。

我以 overlayfs 文件系统为例演示下 copy-on-write 是如何工作的：

```
# 创建目录结构
# mkdir test
# cd test/
# mkdir lower upper work merged
# ls
lower  merged  upper  work
# 分别在上下两层创建两个文件
# echo lower > lower/lower.txt
# touch upper/upper.txt
# 挂在overlayfs文件系统到merged目录
# mount -t overlay overlay -olowerdir=./lower,upperdir=./upper,workdir=./work ./merged
# 查看挂载后的目录内容
# ls merged/
lower.txt  upper.txt
# 新创建的目录实际上位于uppper目录内
# touch merged/merged.txt
# ls upper/
merged.txt  upper.txt
# 对文件修改时实际上是将文件从lower目录拷贝到upper目录，然后修改其内容
# echo change lower > merged/lower.txt
# ls upper/
lower.txt  merged.txt  upper.txt
# cat upper/lower.txt
change lower
# cat lower/lower.txt
lower
```

# image

以上提到的所有技术都非 docker 首创，然后 docker 的牛逼之处在于将现有的技术组织起来，然后定义了一套规范让我们更方便的构建，传递和使用容器技术。image，顾名思义，是容器的模板，就像我们从镜像来启动虚拟机一样。关于 image 我们可以对比虚拟机镜像来看：

1. 他们都是模板的一种形式，我们从虚拟机镜像启动虚拟机，从 image 运行 container。image 一旦 build 好之后就不能修改了。
2. 一个 image 和虚拟机镜像最大的区别就是 image 不包含内核，它仅仅包含了一个程序本身和程序的所有依赖，所以相比虚拟机镜像，image 可以很小。
3. image 有自己的规范[OCI Image Specification](https://github.com/opencontainers/image-spec)，这就让 image 的构建和传播更方便，也就有了[Docker Hub](https://hub.docker.com/)的诞生。

个人认为，image 最牛逼的地方在于分享，传统的下载源码包，然后 configure，然后 make(可能涉及解决依赖问题)，最后 make install 的流程已经被 `docker run` 所取代。

# container

container 在我看来更像是将以上所有技术的一个包装，一个 container 有自己的各种 namespace，里的进程挂在 cgroups 的文件系统的某个层级上，有自己的网卡，然后 container 从 image 创建而来，在 image 之上加上一层可写的目录，基于 copy-on-write 的机制，所有对 container 的修改都会发生在这一层目录之上。同样的，我这里将 container 和虚拟机简单对比下：

1. 虚拟机里运行了一个完整的操作系统，而 container 只是通过 host 的内核运行了一个程序
2. 对虚拟机资源的变更通常设计虚拟机重启，而对 container 资源的变更可以在线操作，不影响程序的运行
3. 对虚拟机的调度目前都在分钟级，而对 container 的调度都在秒级
4. 虚拟机相比 container 来说隔离性好，所以更安全。
