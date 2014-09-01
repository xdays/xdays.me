Title: linux 特殊权限
Date: 2010-08-01 20:56
Author: admin
Category: linux
Tags: linux, 权限
Slug: linux-特殊权限

在linux系统里除了常见的三组权限外，还有一组特殊权限它们分别是  
1）suid  
2）sgid  
3）sticky bit或者称为sbit

这組权限主要用在一些别叫细微的条件下，也可见linxu系统的严谨之处。

由于特殊权限对于文件和目录是不同的，我们这里分开讨论。

对于文件的特殊权限  

suid：对二进制文件有效，当用户执行具有该权限的文件时将具有文件拥有者的权限，例如查看/etc/shadow文件发现如下权限：-r--------
1 root root 1047 May  3 11:57
/etc/shadow，也就是说只有root用户强制写入才能更改该文件，但是每个用户在执行passwd命令的时候却成功的更新了自己的密码，原因就在/usr/bin/passwd这个文件上，来看一下它的权限：-rwsr-xr-x
1 root root 22960 Jul 17  2006
/usr/bin/passwd，看到有s权限，这样就解释了上面的问题。  
sgid：与suid类似只不过执行时拥有文件拥有者所属组的权限。  
sbit：对文件无效。

对于目录的特殊权限：  
suid：对目录无效。  
sgid：在该目录下建立的文件的拥有者所属组与目录的相同，例如：  
drwxrwsrwx 2 root root 4096 May  7 21:05 tst  
-rw-rw-r-- 1 ease root 0 May  7 21:05 easefile  
都是root用户组。  

sbit：拥有这个权限的目录有这样的特点，在这个目录下建立的文件只有文件拥有者和root可以删除，其他的用户不可删除，即使ta拥有w的权限。
