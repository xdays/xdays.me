Title: linux 中文乱码
Date: 2010-09-26 12:20
Author: admin
Category: linux
Tags: linux
Slug: linux-中文乱码

开这篇文章主要目的是来总结一下自己在linux下遇到的各种问题及其解决办法，其实归根结底都是字符编码的问题，不同系统的不同字符编码之间相互显示就会出现乱码，要做的就是把编码统一就行了。windows采用的gb2312而linux用的utf8，所以两者之间经常出现编码不一致

远程登录putty的中文显示？

打开putty主程序，选择window-〉Appearance-〉Font
settings-〉Change...,选择Fixedsys字体,字符集选择CHINESE\_GB2312。  
在window-〉Appearance-〉Translation中，Received data assumed to be in
which character set 中,把Use font encoding改为UTF-8.
如果经常使用,把这些设置保存在session里面。  
经过这两步设置就可以显示中文了。

登录vsftp服务器，中文文件列表显示乱码？

还是一开始提到了，linux用uft8而想flashfxp这样的客户端软件用gb2312编码，所以产生乱码。至于解决办法可以这样考虑能更改的地方有四个：linux和windows系统，vsftp，flashfxp。对于服务器而言，让客户去更改设置是不明智的，所以能更改的地方就只有linux和vsftp，但是vsftp我在配置文件中没有找到相关选项，所以干脆直接把linux系统默认的locale改成gb2312吧。对于redhat系统，编辑/etc/sysconfig/i18n文件改为LANG="zh\_CN.gb2312"，logout再login一切就正常了。
