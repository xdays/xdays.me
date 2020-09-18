---
title: macOS命令行制作Windows10启动盘
date: 2019-06-20
author: admin
category: windows
tags: ['macos', 'windows']
slug: macos-create-windows10-usb-installer
---

# 缘起

标准的制作工具是[Boot Camp Assistant](https://www.windowscentral.com/how-create-windows-10-installer-usb-drive-mac)，但是最新版的 macOS 对 U 盘大小做了限制，这个方法不好使了。现在只能通过命令行来只做了。

# 步骤

## 格式化 U 盘

    diskutil eraseDisk MS-DOS "WINDOWS10" MBR disk2

注意添加 MBR 引导记录

## 挂载磁盘

    hdiutil mount ~/Downloads/Win10_1903_V1_EnglishInternational_x64.iso

命令会输出挂载路径，比如 `/Volumes/CCCOMA_X64FRE_EN-GB_DV9`

## 拷贝数据

    rsync -vha --exclude=sources/install.wim /Volumes/CCCOMA_X64FRE_EN-US_DV9/ /Volumes/WINDOWS10/
    brew install wimlib # 解决FAT32最大可保存4G文件
    wimlib-imagex split /Volumes/CCCOMA_X64FRE_EN-US_DV9/sources/install.wim /Volumes/WINDOWS10/sources/install.swm 4000

搞定！
