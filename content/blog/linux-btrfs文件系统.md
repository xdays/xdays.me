---
title: Linux-Btrfs文件系统
date: 2020-01-04
author: admin
category: linux
tags: ['linux', 'btrfs']
slug: linux-btrfs文件系统
---

# 简介

BtrFS（B-tree 文件系统，又称为 Butter FS 或 Better FS），2007 由 oracle 开源后，得到了 IBM、intel 等厂商的大力支持，其目标计划是替代 linux 目前的 ext3/4，成为下一代 linux 标准的文件系统。 支持写时复制（CoW）、快照、在线扩容缩容、数据 checksum、subvolume、磁盘阵列（raid）等，运行在 linux 上，并遵循 GPL 协议的强大文件系统。

1. CoW(Copy on Write)可以保证数据一致性，每次改动块都会创建新的文件
2. 基于 Cow 技术可以在 volume 和文件级别创建快照
3. 数据块和 inode 都可以动态分配
4. 可以给 metadata 和 data 块来创建多个副本

# 文件系统管理

## 创建

```bash
# 单个设备
mkfs.btrfs -L data /dev/sdb1
# 多个设备，metadata保留多个副本
mkfs.btrfs -d raid0 -m raid1 /dev/sdb1 /dev/sdc1
```

## 添加/删除设备

```bash
btrfs device add /dev/part3
btrfs device remove /dev/part3
```

## 修改数据快或者 meta 块的副本

```bash
btrfs balance start -dconvert=dup /srv/shared/
btrfs balance start -mconvert=dup /srv/shared/
```

## 创建挂载删除 subvolume

```bash
btrfs subvolume create /srv/shared/video
mount -o subvol=video /dev/sdb1 /mnt
umount /mnt
btrfs subvolume delete /srv/shared/video
```

## Quota 磁盘配额

适用于多用户场景，给每个用户分配固定的空间，还可以动态调整

```bash
# enable quota for subvolume
btrfs quota enable /srv/shared/video
# get limit
btrfs qgroup show -reF /srv/shared/video
# set limit
btrfs qgroup limit -e 10G 0/260 /srv/shared/video/
```

然后测试下配额是否生效

```
# dd if=/dev/zero of=/mnt/11G.bin bs=1M count=20480
dd: error writing '/mnt/11G.bin': Disk quota exceeded
10240+0 records in
10239+0 records out
10737377280 bytes (11 GB, 10 GiB) copied, 163.942 s, 65.5 MB/s
```

## 快照

建快照就是从当前状态下的 subvolume 新建一个 subvolume，你也可以直接挂载 snapshot

```bash
btrfs subvolume snapshot /srv/shared/video /srv/shared/video-backup
mount -o subvol=video-backup /dev/sdb1 /mnt
ls /mnt
umount /mnt
btrfs subvolume delete /srv/shared/video-backup
```

## 高能警告

目前社区有一些关于 btrfs 非常负面的评价，褒贬不一，使用前请想好退路，数据无价。看看官方的 [status](https://btrfs.wiki.kernel.org/index.php/Status) 页面，了解下各个功能当前是否稳定了。
