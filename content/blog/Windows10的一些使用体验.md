---
title: Windows10的一些使用体验
date: 2019-01-13
author: admin
category: windows
tags: ['windows']
slug: Windows10的一些使用体验
---

## 一点体会

自从 2014 年切换到 macOS 系统上就一直没有使用过 Windows 系统了，这期间 Win10 发布了，我对其理解也就是样子变了，并没有深入体验。最近需要在 MacBook 之外找一台更便携的辅助办公的设备，在 iPad Pro 和 Surface 之间调研了半天，最终因为 iPad Pro 的软件生态不行而选择了 Surface Pro 5，也在过去的两周深度的体验了下 Windows 10 系统。总提上感觉就是开启了一扇新的大门微软真改变了很多，就像是一个中年大叔变年轻了，最直接的提现就是能从起产品中看到很多新的技术，甚至开始顾及到 Linux 用户的体验了。以下列举了几个我觉得不错的功能。

## PowerShell

PowerShell 在 Windows 7 上也用过，但是比较初级，基本上就当做更好用的 CMD 来使用的，其实很多命令也不通用的。这一次发现 PowerShell 竟然开源了，而且是全平台支持的(看样子是随着.NET Core 开源后的事情)。基本上所有能用图形界面做的事情现在都可以用 PowerShell 来做了，这对我这种什么东西都想自动化的人来说简直是利器。

我再 macOS 环境下 90%的软件都是的 brew 来安装了，之前也听说 Windows 下同类型的工具 chocolatey，这次体验还可以。以管理员身份运行 PowerShell，然后执行如下命令即可

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```

日常使用看下帮助就能上手。这里也说下两点不足：

1. 国内的软件好多没有的，这可以归结为 Windows 生态的问题
2. 没有一个类似 bundle 的东西，可以批量导入已安装的软件及其版本的列表

## WSL

当时从 Windows 换到 macOS 体验最好的就是 macOS 可以同时获得优秀的桌面环境和 Linux 的命令行环境，而且 macOS 的软件生态也很好。现在 Windows 终于有了 WSL，可以同时享受到 Linux 的命令行环境，虽然 Windows 软件质量良莠不齐但是生态巨大，现在在通过 WSL 支持了 Linux 算是补齐了一个短板。

下边来说说 WSL 吧，WSL 其实是在 Windows 之上实现的兼容 Linux 内核的接口层，或者说微软实现了一个精简的 Linux 内核，这个内核可以兼容 Linux 的二进制程序。

首先开启 WSL 功能

```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
```

然后从 Microsoft Store 上搜索 Ubuntu 安装，之后可以运行`ubuntu`来启动 Linux 命令行

```bash
C:\Users\xdays>ubuntu config --default-user root

C:\Users\xdays>ubuntu
root@xdays-parallels:~# uname -a
Linux xdays-parallels 4.4.0-17763-Microsoft #253-Microsoft Mon Dec 31 17:49:00 PST 2018 x86_64 x86_64 x86_64 GNU/Linux
root@xdays-parallels:~# lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 18.04.1 LTS
Release:        18.04
Codename:       bionic
```

然后你就拥有了一个完整的 Ubuntu 版本，此外[预览版的 WSL 还支持了导出和导入的功能](https://docs.microsoft.com/en-us/windows/wsl/release-notes#build-18305)，现阶段可以用[Ubuntu 官方的备份方法](https://help.ubuntu.com/community/BackupYourSystem/TAR)来实现想想看，你配置了一个自己的开发环境然后导入一个备份儿，将来新换一个机器直接导入自己的开发环境，整体体验要比 Vagrant 和 Docker 还好，因为这两个工具对宿主机都有要求。因为 WSL 我都想拿 Surface 来作为主力办公的设备了:)

## Office 365

现在的 Office 365 也已经完全的云化了，以 OneDrive 为储存中心，Office 套件可以 Web，PC 和 macOS 无缝衔接。早年投身 Google Docs 就是因为可以云端同步，现在 Office 365 除了云端还有自己强大的本地程序更牛逼了，况且 Office 的云端同步虽然也不快，但是至少不需要翻墙就能打开。

再说一个我自己的需求，有时候我通过画图表给别人演示一个东西。这个需求包含两部分：第一是我这一端需要手写笔，Surface Pen 虽然不如 Apple Pencil 但也是除此之外最好的选择了；第二部分是我需要别人能直接实时查看我画的东西。OneNote 正好可以满足这个需求，主要问题是延迟，本地修改好长时间才能在页面上展示出来，不如 Google Docs 体验好，这块不知道是网络问题，还是微软没做好。其他的功能还有待学习啦。

# Surface

最后还是说下 Surface Pro 吧

不足目前还没有体会到，先说优点吧：

1. 轻便但是却很强大，移动办公
2. Windows Hello 登录体验棒
3. Surface Pen 随时以另一方式记录自己的想法
4. Windows 强大的生态
