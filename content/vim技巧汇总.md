Title: vim技巧汇总
Date: 2011-07-28 10:37
Author: admin
Category: tool
Tags: software, vim
Slug: vim技巧汇总

移动
====

-   注意w和W的区别：word是字母数字和下划线组成，而WORD是空格分隔的；跳过一个IP时可以用W。
-   \^跳到第一个非空字符，g\_跳到最后一个非空字符
-   在一个很长的行内移动，gj移动到下个可视行，其他组合类似
-   命令行参数，比如定位到40行就写+40
-   

修改
====

-   r!command可将命令输出插入进来
-   .可以重复上次对文件做修改的命令
-   ayy将行存入命令寄存器中
-   录制宏q后跟宏名称，最后以q结束
-   设置`:vnoremap < <gv`可一多次块缩进
-   指令K可以跳出当前字符的man手册，也可以定制查询命令

编码技巧
========

-   通过ctrl+{A|X}来来加减数字
-   \~可改变字符大小写

外观
====

-   -p可以将文件以标签形式打开

取消备份功能或备份到特定目录
============================

windows下编辑软件个目录下的\_vimrc文件，在最后添加set
nobackup可取消自动备份，添加set
backupdir=\$VIMbackup即可自动备份到特定目录；Linux下编辑家目录下的.vim/.vimrc添加对应选项即可。

我的gvim配置文件
================

    " ---- Global Setting ----
    " set pwd dirs
    let g:Source=""
    " set color style
    colo torte 
    " hide toolbar menu
    set guioptions-=T
    set guioptions-=m
    " turn off autobackup
    set nu nobackup
    " change pwd to path of current file
    set autochdir
    " setting for python
    set ts=8 et sw=4 sts=4
    " setting for encode
    " set encoding=utf-8
    set fileencodings=utf-8,chinese,latin-1
    if has("win32")
    set fileencoding=chinese
    else
    set fileencoding=utf-8
    endif
    " ---- end of Global Setting ----

    " ---- Plugin Settings ----
    " shortcut for NERDTree
    " map  :NERDTreeMirror
    " map  :NERDTreeToggle
    " ---- end of Plugin Settin
