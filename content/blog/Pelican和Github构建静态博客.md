---
title: Pelican和Github构建静态博客
date: 2014-08-15
author: admin
category: devops
tags: ['blog', 'pelican', 'lua']
slug: Pelican和Github构建静态博客
---

#缘起
最近因为要换工作了，时间比较空闲，所以打算好好整理下自己的博客。想来博客写的越来越少也挺惭愧，好多东西都只停留在笔记的草稿阶段，没有写成博客，后续慢慢整理出来。回到正题，我开博客伊始一直用 wordpress（下文简称 WP），有点自然不必多说，成熟稳定，功能全面，主题丰富；但是我最近渐渐在思考我真的需要它么，我的日常操作不过是当我的笔记草稿足以成型为一篇博客，我把它粘贴到 WP 的编辑框，选择下分类，打上标签，点击发布，仅此而已；为此还安装插件让 WP 支持直接在编辑器里贴 markdown；所以我需要的只不过是能够渲染 markdown，生成静态 html 即可，不需要 php，也不需要数据库；此外，博客自动发布也是我需要的一个功能。

#计划
首先，选择静态博客生成器。目前 jekyll 的风头最大，但我没有选择他有两个原因：一是学习成本比较高，我只是想用你生成 html 你却让我学习那么多东西，不值得；二是我是 Python 党，我希望我用的工具能提升我的 Python 技能，嗯，这个也很重要。所以我选择用[Pelican](http://getpelican.com)，它足够简单，拿到就可以使用。

然后，迁移。基本所有的静态博客项目都提供了导入的功能，尤其从 WP 这样如此流行的项目，但是`pelican-import`这个工具在字符处理有一些坑，这个后边会详细提到。

再次，版本。既然所有的东西都是静态文本文件，那么自然而然想到可以用 Git 来管理所有 mardown 文本，托管在 Github。

最后，自动发布。其实自动发布是个可有可无的功能，自己封装个脚本在写好 markdown 之后运行下脚本即可，成本和在 WP 上点击下发布相当，但是既然已经用上 Github 那何不好好用用 Github 的[Webhook](https://developer.github.com/webhooks/)呢，这样就可以在新博客提交到 Github 时触发一个动作，剩下的就是响应这个动作来做博客构建了。博客构建是有逻辑的，而我不想为这一个需求再引入其他 php 或者 python 应用，考虑到静态博客唯一需要的就是一个 Web 服务器，我决定用 Ningx+Lua 的模式来处理这个 Webhook。

至此，所有需求都有了恰当的解决办法。

#实施
##pelican ###安装
pip install pelican markdown

###配置
pelican-quickstart

###使用
pelican 的配置文件就是一个 python 代码文件，一般在博客根目录下的 pelicanconf.py，主要定义一些博客本身的元信息，具体配置项可参考[这里](http://docs.getpelican.com/en/3.4.0/settings.html)。content 目录为 markdown 文件存放目录，每篇博客一个文件，在每篇文件得开头写一些 meta 信息，指定标题，作者，分类，tag 和 slug 等信息。

修改 pelicanconf.py，我的配置内容如下：

```
#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Misc
AUTHOR = u'xdays'
SITENAME = u'xdays'
SITEURL = 'http://xdays.me'
KEYWORD = '架构，运维，开发, 生活随想'
PATH = 'content'
STATIC_PATHS = ['wp-content']

# Time
TIMEZONE = 'Asia/Shanghai'
DEFAULT_LANG = u'zh'

# Feed
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Menu
MENUITEMS = (('首页', SITEURL),)
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False

# Pagination
DEFAULT_PAGINATION = 20

# Output
DELETE_OUTPUT_DIRECTORY = True

# Disqus
DISQUS_SITENAME = "xdays"

# Github
GITHUB_USER = 'xdays'
GITHUB_REPO_COUNT = 5
```

最后生成博客：

    pelican -s pelicanconf.py -t theme content

注意：`-t`可以指定主题路径

##pelican-import
首先要导出 wordpress 的文章为 xml 文件，需要安装一个叫`wordpress-importer`的插件。

安装`pelican-import`的依赖：

    apt-get install python-lxml pandoc
    pip install BeautifulSoup4

导出 markdown 文件：

    pelican-import --wpfile wordpress.xml -m markdown -o content

下边开始说坑，在每个 markdown 文件有个 slug 的 meta 标记，这个标记是生成的 html 的文件名，但是由于 pelican-import 对字符集处理的不是太好，所以需要自己手动将 slug 进行一次 unquote，然后用 unquote 之后的字符串来命名文件，废话少说，上代码：

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import unquote
import os
import sys

top = sys.argv[1]
out = sys.argv[2]
flist = sum([[os.path.join(base,file) for file in files] for base,dirs,files in os.walk(top)],[])

os.mkdir(out)

for i in flist:
    dirname = os.path.dirname(i)
    with open(i) as f:
        s = f.readlines()
        for l in s:
            if l.startswith('Slug'):
                index = s.index(l)
                p = l.strip().split()
                filename = unquote(p[-1])
                p[-1] = filename + '\n'
                s[index]=' '.join(p)
                with open('%s/%s.md'%(out, filename), 'w') as g:
                        g.write(''.join(s))
                break
```

这段代码接受两个参数：第一个是导出的 markdown 目录，第二个是处理后的 markdown 文件存放目录。

##Github
将整个博客目录交给 Git 管理：

```
git init
git add .
git commit -m 'first owesome commit'
git remote add origin git@github.com:xdays/xdays.me.git
git push -u origin master
```

然后配置 webhook，具体参考[Github 文档](https://developer.github.com/webhooks/)

##Nginx+Lua ###安装
安装过程涉及的环节比较多，也可以直接使用[openresty](http://openresty.org/)，下面脚本详细说明了安装过程：

```
apt-get install libpcre3-dev zlib1g-dev build-essential

cd ~
wget http://nginx.org/download/nginx-1.7.4.tar.gz
tar xzf nginx-1.7.4.tar.gz
wget http://luajit.org/download/LuaJIT-2.0.3.tar.gz
tar xzf LuaJIT-2.0.3.tar.gz
wget https://github.com/chaoslawful/lua-nginx-module/archive/v0.9.10.tar.gz
mv v0.9.10.tar.gz lua-nginx-module-0.9.10.tar.gz
tar xzf lua-nginx-module-0.9.10.tar.gz

cd ~/LuaJIT-2.0.3
make install PREFIX=/usr/local/xengine/luajit
cd ~/nginx-1.7.4
./configure --with-ld-opt="-Wl,-rpath,/usr/local/xengine/luajit/lib" --with-http_stub_status_module --add-module=/root/lua-nginx-module-0.9.10/ --prefix=/usr/local/xengine/nginx
make -j2
make install
```

###配置
在博客的的 server 配置里添加如下配置：

```
    location /example-url {
        content_by_lua_file /path/to/genblog.lua;
    }
```

再上 lua 代码：

```
os.execute('export LANG=zh_CN.UTF-8 && cd /blog/path && pelican -s pelicanconf.py content/ -t theme/')
ngx.header.content_type = "text/html"
ngx.print('success\n')

return ngx.exit(ngx.HTTP_OK)
```

###使用
对博客做一些修改，然后请求如下 url，看效果：

    curl localhost/example-url

返回`success`表示博客构建成功

###联动

最后就是给 Github 配置上上一小节配置的 webhook playload url 接口即可。
