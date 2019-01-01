---
title: ubuntu 系统配置
date: 2010-08-01
author: admin
category: linux
tags: linux, ubuntu
slug: ubuntu-系统配置
---

<div id="blog_text">

​1. 更新源  
编辑/etc/apt/sources.list文件，源不列了，搜吧大把大把的。

2.firefox的flash插件中文乱码：  

编辑/etc/fonts/conf.d/49-sansserif.conf字体配置文件，将其中的sans-serif替换成AR
PL UKai CN（系统中安装的字体），重启firefox即可。

3.安装nvidia显卡驱动  
直接打开硬件驱动管理程序选择建议安装的驱动，下载完成重启即可。

​4. 允许root登录  
因为系统建立好后没有给root赋予密码，要想root登录先\$ sudo passwd root ,
这样root就可以文本终端登录了，然后设置 系统--系统管理--登录窗口
即可允许root在图形届满登录。

​5. 安装虚拟机virtualbox-ose  

具体安装设置都很简单，找个教程：<http://www.kafan.cn/edu/xuniji/200811012526.html>讲的很详细了，这里只是提一下几个需要特别注意的点：  
1）虚拟机的双向共享剪切板可以实现宿主机与客户机之间的拷贝粘贴。  
2）宿主机的虚拟光驱会作为客户机的物理光驱。  
3）分配共享空间后可以用net use x:
[\\vboxsvrsharename](file://vboxsvr/sharename)打开共享空间。  
4）系统安装完毕之后要安装增强功能，以实现鼠标捕捉及共享剪切板功能。  

补充：源内的2.1.4老了，还是用官方网站上的方法安装最新的版本吧，只是速度有点慢。  
官方安装：<http://www.virtualbox.org/wiki/Linux_Downloads>

​6. 安装stardic的词典

词典下载地址：  
cdict-gb dictionary(en - zh\_CN): <http://www.snowbird-linux.com/do>
... ct-gb-2.4.2.tar.bz2  
oxford-gb dictionary(en - zh\_CN) 牛津现代英汉双解词典:
<http://www.snowbird-linux.com/do> ... rd-gb-2.4.2.tar.bz2  
stardict1.3 dictionary(en - zh\_CN): <http://www.snowbird-linux.com/do>
... ct1.3-2.4.2.tar.bz2  
xdict-ec-gb dictionary(en - zh\_CN): <http://www.snowbird-linux.com/do>
... ec-gb-2.4.2.tar.bz2  
langdao-ec-gb dictionary(en - zh\_CN) 朗道英汉字典:
<http://www.snowbird-linux.com/do> ... ec-gb-2.4.2.tar.bz2  
21 century bidirectional dictionary 21世纪英汉汉英双向词典:
<http://www.snowbird-linux.com/do> ... idian-2.4.2.tar.bz2  
quick\_eng-zh\_CN: <http://www.snowbird-linux.com/do> ...
zh\_CN-2.4.2.tar.bz2  
21 century bidirectional science and technology dictionary
21世纪双语科技: <http://www.snowbird-linux.com/do> ...
idian-2.4.2.tar.bz2

安装的方法（以安装 stardict-oxford-gb-2.4.2.tar.bz2 为例）  
先下好安装的词典软件包， stardict-oxford-gb-2.4.2.tar.bz2  
在它的目录下面解压： tar -xjvf stardict-oxford-gb-2.4.2.tar.bz2  
再把解压后的文件夹放入到/usr/share/stardict/dic中：  
mv stardict-oxford-gb-2.4.2/usr/share/stardict/dic  
安装结束,重新启动星际译王加载词典

7。 配置桌面图标  

在终端下输入gconf-editor打开配置编辑器，依次展开/apps/nautilus/desktop/，勾选相应键即可。另外在/apps/nautilus/icon\_view/default\_zoom\_level可以设置图标大小。

​8. Flash插件不显示中文或者显示方框解决  
1）编辑/etc/fonts/conf.d/49-sansserif.conf字体配置文件  
2）将其中的sans-serif替换成AR PL UKai CN（系统中安装的中文字体）  
3）重启firefox即可

​9. 右键添加打开终端  
＃sudo apt-get install nautilus-open-terminal

10.sudo apt-get install unrar p7zip-rar p7zip-full cabextract

​11. lftp访问一些服务器出现乱码  

主要是因为客户端和服务器的编码不一支，在用户家目录下编辑文件\~/.lftprc或者\~/.lftp/rc，添加如下内容：  
debug 3  
set ftp:charset GBK  
set file:charset UTF-8  
\#set ftp:passtive-mode no  
\#alias utf8 " set ftp:charset UTF-8"  
\#alias gbk " set ftp:charset GBK"

​12. 删除旧内核  
方法一：用“新立得软件管理包”程序  

“系统”-\>“新立得软件管理包”，然后搜索“linux-image”，找到旧内核并进行删除；  
方法二：命令行操作  
\$ dpkg --get-selections | grep linux-image-2.6.27 | grep -v \$(uname
-r)  

先用这些命令的组合查看列出来的结果是不是要删除的内核，确认无误后，在上述命令行后继续加指令：  
\$ dpkg --get-selections | grep linux-image-2.6.27 | grep -v \$(uname
-r) | awk '{print \$1}' | xargs sudo apt-get -y purge

​13. 修改默认终端窗口大小  
1）\#sudo vi
/usr/share/vte/termcap/xterm，修改:co\#80:it\#8:li\#24:这一行就可以了。  
2）直接通过菜单修改配置文件，直观方便。

</div>
