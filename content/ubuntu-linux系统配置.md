Title: wget
Date: 2010-06-05 09:53
Author: admin
Category: tool
Tags: wget
Slug: ubuntu-linux系统配置

方便的网络下载工具wget  
wget是一个强力方便的命令行方式下的下载工具。本文介绍了wget的基本用法。  

网络用户有时候会遇到需要下载一批文件的情况，有时甚至需要把整个网站下载下来或者制作网站的镜像。在Windows下的用户都比较熟悉
Teleport，
webzip等等网站下载工具，实际上Linux中也完全可以做到这样的功能，那就是利用wget工具。wget是一个命令行工具，用来下载网络文件或者
整个网站，它具有自动重试、断点续传、支持代理服务器等等强大的功能。它可以完全替代ftp客户端。wget是在Linux下开发的开放源代码的软件，作
者是 Hrvoje Niksic，后来被移植到包括Windows在内的各个平台上。  
wget虽然功能强大，但是使用起来还是比较简单的，基本的语法是：wget
[参数列表] URL。下面就结合具体的例子来说明一下wget的用法。  
1、下载整个http或者ftp站点。  
wget <http://place.your.url/here>  
这个命令可以将<http://place.your.url/here>
首页下载下来。使用-x会强制建立服务器上一模一样的目录，如果使用-nd参数，那么服务器上下载的所有内容都会加到本地当前目录。  
wget -r <http://place.your.url/here>  

这个命令会按照递归的方法，下载服务器上所有的目录和文件，实质就是下载整个网站。这个命令一定要小心使用，因为在下载的时候，被下载网站指向的所有地址
同样会被下载，因此，如果这个网站引用了其他网站，那么被引用的网站也会被下载下来！基于这个原因，这个参数不常用。可以用-l
number参数来指定下载的层次。例如只下载两层，那么使用-l 2。  
要是您想制作镜像站点，那么可以使用－m参数，例如：  
wget -m <http://place.your.url/here>  

这时wget会自动判断合适的参数来制作镜像站点。此时，wget会登录到服务器上，读入robots.txt并按robots.txt的规定来执行。  
2、断点续传。  

当文件特别大或者网络特别慢的时候，往往一个文件还没有下载完，连接就已经被切断，此时就需要断点续传。wget的断点续传是自动的，只需要使用-c参数，例如：  
wget -c <http://the.url.of/incomplete/file>  

使用断点续传要求服务器支持断点续传。-t参数表示重试次数，例如需要重试100次，那么就写-t
100，如果设成-t
0，那么表示无穷次重试，直到连接成功。-T参数表示超时等待时间，例如-T
120，表示等待120秒连接不上就算超时。  
3、批量下载。  

如果有多个文件需要下载，那么可以生成一个文件，把每个文件的URL写一行，例如生成文件download.txt，  
然后用命令：  
wget -i download.txt  

这样就会把download.txt里面列出的每个URL都下载下来。（如果列的是文件就下载文件，如果列的是网站，那么下载首页）  
4、选择性的下载。  
可以指定让wget只下载一类文件，或者不下载什么文件。例如：  
wget -m --reject=gif <http://target.web.site/subdirectory>  

表示下载<http://target.web.site/subdirectory>，但是忽略gif文件。--accept=LIST
可以接受的文件类型，--reject=LIST拒绝接受的文件类型。  
5、密码和认证。  
wget只能处理利用用户名/密码方式限制访问的网站，可以利用两个参数：  
--http-user=USER设置HTTP用户  
--http-passwd=PASS设置HTTP密码  
对于需要证书做认证的网站，就只能利用其他下载工具了，例如curl。  
6、利用代理服务器进行下载。  

如果用户的网络需要经过代理服务器，那么可以让wget通过代理服务器进行文件的下载。此时需要在当前用户的目录下创建一个.wgetrc文件。文件中可以设置代理服务器：  
http-proxy = 111.111.111.111:8080  
ftp-proxy = 111.111.111.111:8080  

分别表示http的代理服务器和ftp的代理服务器。如果代理服务器需要密码则使用：  
--proxy-user=USER设置代理用户  
--proxy-passwd=PASS设置代理密码  
这两个参数。  
使用参数--proxy=on/off 使用或者关闭代理。  
wget还有很多有用的功能，需要用户去挖掘。

转自：<http://hi.baidu.com/52hack/blog/item/fb927e090d52ada62eddd48e.html>
