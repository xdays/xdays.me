---
title: U盘安装CentOS7系统
date: 2016-02-23
author: admin
category: linux
tags: ['pxe', 'linux']
slug: U盘安装CentOS7系统
---

# 需求

- U 盘安装
- 小规模
- 自动安装

# 工具

- system-config-kickstart
- kickstart
- livecd-iso-to-disk

# 配置过程

1. 将 iso 文件写入 U 盘`sudo livecd-iso-to-disk --format --reset-mbr ./CentOS-6.4-x86_64-minimal.iso /dev/sdb`
2. 用 system-config-kickstart 创建 ks 文件，注意修改以下两点：
   - `harddrive --partition=sda1 --dir=/` 这里是制定安装介质的存放目录
   - `bootloader --location=mbr --driveorder=sdb,sda` 指定 grub 的安装磁盘，如果不指定会写到 U 盘上去的
3. 将 ks.cfg 拷贝只 U 盘根目录下
4. 修改 U 盘上的 grub 引导菜单 syslinux/extlinux.conf，添加内核参数 ks=hd:sda1:/ks.cfg

# 安装

- 设备设置 U 盘第一启动，启动菜单第一个即可

# 参考

## ks.cfg

```
#platform=x86, AMD64, or Intel EM64T
#version=DEVEL
# Install OS instead of upgrade
install
# Keyboard layouts
keyboard 'us'
# Reboot after installation
reboot
# Root password
rootpw --iscrypted $1$CU9rtnsD$/V7sKSQAJrE3cLn.CO0
# System timezone
timezone Asia/Shanghai
# System language
lang en_US
# Firewall configuration
firewall --disabled
# System authorization information
auth  --useshadow  --passalgo=sha512
# Use CDROM installation media
harddrive --partition=sda1 --dir=/
# Use text mode install
text
firstboot --disable
# SELinux configuration
selinux --disabled

# System bootloader configuration
bootloader --location=mbr --driveorder=sdb,sda
# Clear the Master Boot Record
zerombr
# Partition clearing information
clearpart --all
# Disk partitioning information
part / --asprimary --fstype="ext4" --size=10240
</pre>
```
