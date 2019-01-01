---
title: rsync文件同步服务
date: 2012-10-17
author: admin
category: server
tags: rsync, server
slug: rsync文件同步服务
---

### 简介

rsync是一个文件同步工具，简单来说，它的功能就是在两个位置（可能是本地的两个目录或者本地目录和远程目录）之间拷贝文件；但是相比cp或者scp等命令，rsync优势在于其强大的增量拷贝（高效）和过滤条件（灵活）上。

### 功能特点

-   支持特殊文件，文件常见属性的拷贝
-   可以借助常见的ssh，rsh等来传输
-   强大的过滤机制
-   通过著名的delta-transfer算法来实现高效传输
-   基于服务的匿名和认证传输

### 客户端使用

#### 运行模式

##### 本地模式

    rsync [OPTION...] SRC... [DEST]

如果源和目标都是本地路径则和cp类似。

##### shell模式

    Pull: rsync [OPTION...] [USER@]HOST:SRC... [DEST]
    Push: rsync [OPTION...] SRC... [USER@]HOST:DEST

通过shell连接时在主机名和路径之间用一个":"，用户名可选。

##### daemon模式

    Pull: rsync [OPTION...] [USER@]HOST::SRC... [DEST] 或者 rsync [OPTION...] rsync://[USER@]HOST[:PORT]/SRC... [DEST]
    Push: rsync [OPTION...] SRC... [USER@]HOST::DEST 或者 rsync [OPTION...] SRC... rsync://[USER@]HOST[:PORT]/DEST

通过daemon模式（daemon配置参照最后一部分）连接时在主机和路径之间用两个":"，用户名可选。

##### 混合模式

这里混合模式指的通过shell模式来使用daemon模式的一些特性。只要制定外部shell即可。

    rsync -av --rsh=ssh host::module /dest

#### 命令行选项

     -v, --verbose 增强可读性
     -q, --quiet 忽略非错误信息
     --no-motd 忽略daemon模式的MOTD信息 (see manpage caveat)
     -c, --checksum 基于checksum校验，而非mod-time和size
     -a, --archive 归档模式，和-rlptgoD (不要使用 -H,-A,-X)参数相同
     --no-OPTION 关闭一些显式的OPTION (比如 --no-D)
     -r, --recursive 递归目录
     -R, --relative 使用相对路径
     --no-implied-dirs 不发送制定目录的属性，避免在目标使用--relative删除连接重新传输文件，
     -b, --backup 备份 (查看 --suffix & --backup-dir)
     --backup-dir=DIR 基于DIR来创建备份的目录结构
     --suffix=SUFFIX 制定备份的后最 (default ~ w/o --backup-dir)
     -u, --update 跳过接受端较新的文件
     --inplace 直接在文件上更新(SEE MAN PAGE)
     --append 直接追加文件
     --append-verify 和--append很像, 只是用文件的较旧的那部份做checksum
     -d, --dirs 仅传输文件而非递归
     -l, --links 将软链接当作软链接来拷贝
     -L, --copy-links 拷贝链接对应的文件或者目录而非链接本身
     --copy-unsafe-links 仅不安全的链接才被拷贝
     --safe-links 忽略那些链接到目录树外的链接
     -k, --copy-dirlinks 将链接翻译成其链接的目录
     -K, --keep-dirlinks 将目录链接在接收端转换成目录
     -H, --hard-links 保留硬链接
     -p, --perms 保留权限
     -E, --executability 保留文件的可执行性
     --chmod=CHMOD 改变文件或者目录的权限
     -A, --acls 保留ACLs (implies --perms)
     -X, --xattrs 保留扩展属性
     -o, --owner 保留所有者(super-user only)
     -g, --group 保留组
     --devices 保留设备文件 (super-user only)
     --specials 保留特殊文件
     -D 和 --devices --specials一样
     -t, --times 保留修改时间
     -O, --omit-dir-times 在--times选项里忽略目录的时间
     --super 允许接受方执行那个一些超级用户的活动
     --fake-super 通过xattrs来存储和回复权限
     -S, --sparse 高效处理稀疏文件
     -n, --dry-run 只运行，不做改变
     -W, --whole-file 拷贝整个文件(without delta-xfer algorithm)
     -x, --one-file-system 不跨越文件系统
     -B, --block-size=SIZE 强制指定checksum的块大小
     -e, --rsh=COMMAND 指定要使用的远程shell
     --rsync-path=PROGRAM 指定远程要运行的rsync路径
     --existing 如果接收端不存在文件就不创建
     --ignore-existing 如果接收端存在就不更新文件
     --remove-source-files 发送端删除已经同步的文件 (non-dirs)
     --del an alias for --delete-during
     --delete 删除接收端上在发送端不存在的文件
     --delete-before 接收端在发送前删除，而不是发送过程中
     --delete-during 接收端在发送过程中删除
     --delete-delay 在发送过程中寻找文件，在发送完成后删除
     --delete-after 接收端在发送完成后删除
     --delete-excluded 在接收端删除排除的文件
     --ignore-errors 即使有I/O错误也删除
     --force 即使目录不是空的也删除
     --max-delete=NUM 最多删除文件的数目
     --max-size=SIZE 最大传输文件的大小
     --min-size=SIZE 最小传输文件的大小
     --partial 保持部分传输的文件
     --partial-dir=DIR 制定部分传输文件的存放目录
     --delay-updates 先传输，最后再更新，保持原子性
     -m, --prune-empty-dirs 接收端删除空目录
     --numeric-ids 接收端不要将uid/gid映射为用户名和组名
     --timeout=SECONDS 设置I/O超时时间，s为单位
     --contimeout=SECONDS 设置链接服务端的时间
     -I, --ignore-times 即使mtime和size都相同也不跳过
     --size-only 只要大小相同就跳过
     --modify-window=NUM 比对时间时制定精确范围，范围内都认为时间相同
     -T, --temp-dir=DIR 指定创建临时文件的目录
     -y, --fuzzy 文件在接收端不存在的情况下，在当前目录下寻找一个基础文件，以加快传输
     --compare-dest=DIR 接收端除了和发送端对比还和这里指定的目录对比，适合备份上次备份改变的文件
     --copy-dest=DIR 和--compare-dest类似，只是接收端会用本地拷贝来复制那些未改变的文件
     --link-dest=DIR 和--compare-dest类似，只是接收端会建立那些未改变文件的硬链接
     -z, --compress 传输过程中压缩
     --compress-level=NUM 指定压缩等级
     --skip-compress=LIST 不压缩指定后缀的文件
     -C, --cvs-exclude 以CSV的方式自动忽略文件
     -f, --filter=RULE 新增一个file-filtering规则
     -F same as --filter='dir-merge /.rsync-filter' repeated: --filter='- .rsync-filter'
     --exclude=PATTERN 排除规则PATTERN
     --exclude-from=FILE 从文件中读取排除规则
     --include=PATTERN 不要排除指定规则的文件
     --include-from=FILE 从文件中读取包含的规则
     --files-from=FILE 从文件中读取文件列表
     -0, --from0 all *-from/filter files are delimited by 0s
     -s, --protect-args 参数不许要空格分割; only wildcard special-chars
     --address=ADDRESS 绑定监听的地址
     --port=PORT 制定端口号
     --sockopts=OPTIONS 制定TCP选项
     --blocking-io 在远程shell中使用blocking I/O
     --stats 给出文件统计信息
     -8, --8-bit-output 输出时不对高位字符转义
     -h, --human-readable 以易于阅读的方式打印数字
     --progress 显示传输进度
     -P same as --partial --progress
     -i, --itemize-changes 打印更新的总结信息
     --out-format=FORMAT 以特定的格式打印更新信息
     --log-file=FILE 日志文件
     --log-file-format=FMT 日志文件格式
     --password-file=FILE 密码文件
     --list-only 仅列出文件
     --bwlimit=KBPS 限制带宽; KBytes per second
     --write-batch=FILE 将批量更新写入文件
     --only-write-batch=FILE 和 --write-batch类似 but w/o updating destination
     --read-batch=FILE 从文件中读取批量更新任务
     --protocol=NUM 使用旧版本的协议
     --iconv=CONVERT_SPEC 要求文件名字符转义
     -4, --ipv4 prefer IPv4
     -6, --ipv6 prefer IPv6
     --version 打印帮助信息
    (-h) --help 打印这个帮组信息 (-h 仅在单独使用时与 --help 同意)

#### 常见用法

归档模式备份

    rsync -Cavz . localhost:backup

镜像服务器站点

    rsync -az -e ssh --delete local/path remotehost:/remote/path

### 服务端配置

#### 命令选项

    Usage: rsync --daemon [OPTION]...
     --address=ADDRESS 绑定地址
     --bwlimit=KBPS 限速; KBytes per second
     --config=FILE 指定配置文件，默认是/etc/rsyncd.conf
     --no-detach 不跑后台
     --port=PORT 监听端口
     --log-file=FILE 日志文件路径
     --log-file-format=FMT 日志格式
     --sockopts=OPTIONS 指定TCP选项
     -v, --verbose 增强可读性
     -4, --ipv4 prefer IPv4
     -6, --ipv6 prefer IPv6
     --help show this help screen

#### 配置选项

##### 全局选项

    motd file 提示信息文件
    log file 日志文件路径
    pid file 进程文件路径
    port 绑定端口
    address 绑定地址
    socket options 指定TCP选项

##### 模块选项

    comment 注释信息
    path 模块对应路径
    use chroot 使用chroot
    max connections 最大连接数
    max verbosity 服务端的详细程度
    lock file lock文件路径
    read only 是否允许上传
    write only 是否允许下载
    list 是否显示列表
    uid 指定用户uid
    gid 制定用户gid
    filter 制定过滤器
    exclude 排除
    exclude from 从文件内容中排除
    include 包含
    include from 从文件内容中包含
    incoming chmod 修改上传权限
    outgoing chmod 修改下载权限
    auth users 用户名
    secrets file 密码文件
    strict modes 严格模式
    host allow 允许主机列表
    host deny 拒绝主机列表
    ignore errors 忽略I/O错误
    ignore nonreadable 忽略不可读的文件
    transfer logging 记录文件传输日志
    log format 日志格式
    timeout I/O超时时间
    refuse options 指定拒绝选项
    dont compress 指定不压缩文件
    pre-xfer exec, post-xfer exec 指定在文件传输前后执行的命令

#### 配置示例

编辑配置文件vim /etc/rsyncd.conf

    motd file = /etc/rsyncd.motd
    uid=root
    gid=root
    use chroot=no
    log file=/var/log/rsyncd.log
    pid file=/var/run/rsyncd.pid
    lock file=/var/run/rsyncd.lock
    [rsyncd]
    max connections=36
    path=/root
    comment = vmachine1 backup
    ignore errors = yes
    read only = no
    secrets file = /etc/rsyncd.secrets
    hosts allow = 192.168.110.0/24
    hosts deny = *

然后启动rsync

rsync --daemon
