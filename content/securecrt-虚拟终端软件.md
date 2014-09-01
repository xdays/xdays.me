Title: SecureCRT-虚拟终端软件
Date: 2010-11-28 12:13
Author: admin
Category: tool
Tags: securecrt, software
Slug: securecrt-虚拟终端软件

SecureCRT是windows下非常优秀的终端仿真程序，他有好多特性，主要的的有安全，便于管理，界面友好，自动重复指令，支持文件传输。

### 特性总结

1）退出时，自动关闭标签。

选项-全局选项-常规-默认会话-编辑默认配置-终端-勾选“断开时关闭”

2）SFTP下载路径

选项-全局选项-常规-默认会话-编辑默认配置-SFTP标签页

当通过ssh连接了linux主机时，可以右击标签页选择“连接SFTP标签页”，在打开的标签页下可以通过put，get命令上传下载文件，非常方便。

3）开启中键复制功能

选项-全局选项-终端-勾选“选中时复制”和“粘贴用\*键”。

4）脚本完成重复的工作

脚本-开始录制脚本；脚本-停止录制脚本；脚本-执行。

### 配置优化

SecureCRT可以把配置文件指定到一个目录内下，这样包括软件的global配置，还是针对某个connection的特定配置，以及所有的ssh
key都可以保存到一个目录下，这样在重装软件时可以很方便的转移。设置选项在option-global
option-general-configuration folder和option-global option-SSH Host
Keys-Host keys database location下。

参考文章<http://tech.ddvip.com/2009-02/1234422493108450.html>

官方主页<http://www.vandyke.com/products/securecrt/index.html>

绿色版下载地址<http://www.xdowns.com/soft/xdowns2009.asp?softid=23625&downid=5&id=23625>
