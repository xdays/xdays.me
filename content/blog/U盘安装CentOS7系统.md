---
title: U盘安装CentOS7系统
date: 2016-02-23
author: admin
category: linux
tags: pxe,centos
slug: U盘安装CentOS7系统
---
 
# 需求

* U盘安装
* 小规模
* 自动安装

# 工具

* system-config-kickstart
* kickstart
* livecd-iso-to-disk

# 配置过程

1. 将iso文件写入U盘`sudo livecd-iso-to-disk  --format --reset-mbr ./CentOS-6.4-x86_64-minimal.iso /dev/sdb`
2. 用system-config-kickstart创建ks文件，注意修改以下两点：
    * `harddrive --partition=sda1 --dir=/` 这里是制定安装介质的存放目录
    * `bootloader --location=mbr --driveorder=sdb,sda` 指定grub的安装磁盘，如果不指定会写到U盘上去的
3. 将ks.cfg拷贝只U盘根目录下
4. 修改U盘上的grub引导菜单syslinux/extlinux.conf，添加内核参数ks=hd:sda1:/ks.cfg

# 安装

* 设备设置U盘第一启动，启动菜单第一个即可

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
