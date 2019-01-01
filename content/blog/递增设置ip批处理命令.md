---
title: 递增设置ip批处理命令
date: 2010-10-22
author: admin
category: windows
tags: cmd, windows
slug: 递增设置ip批处理命令
---

刷票是件体力活，但是运用好点小知识还是能减小运动量的，一般刷票都需要更改IP地址，手动更改又费事，下面的批处理命令就是我自己参考在线资料做的脚本，还是挺好用的。

    @ echo off
    echo *****ip自动更改器*****
    echo n
    echo 提示：请按提示输入起始和结束ip地址
    echo 等待提示“按任意键继续时”就可以按F5刷新浏览器开始投票了”
    rem 设置变量
    set nic=内部连接
    rem 设置起始地址
    set /p s=起始地址：
    set /a add=s
    rem 设置结束地址
    set /p e=结束地址：
    set /a end=e
    set /a end+=1
    rem 网关地址
    set gat=192.168.1.1
    rem 执行循环
    :loop
    rem //是否达到结束IP地址
    if %add%==%end% (
    goto exit
    )
    echo 耐心等待几秒~
    rem //更改IP
    netsh interface ip set address name=%nic% source=static addr=192.168.1.%add% mask=255.255.255.0 %gat% 1 >nul
    rem //更改DNS
    netsh interface ip set dns name=%nic% source=static addr=210.44.176.1 primary >nul
    echo 目前ip地址:%add%
    set /a add+=1
    @pause
    goto loop
    :exit
    rem 循环结束
    echo 工作完成！
    @pause

    @ echo off
