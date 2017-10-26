#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Misc
SITEURL = 'http://xdays.me'
AUTHOR = u'xdays'
SITENAME = u'xdays'
KEYWORD = '架构，运维，开发, 生活随想'
STATIC_PATHS = ['wp-content']
EXTRA_PATH_METADATA = {
    'wp-content/static/robots.txt': {'path': 'robots.txt'},
    'wp-content/static/favicon.ico': {'path': 'favicon.ico'},
}
PATH = 'content'
OUTPUT_PATH = 'public'
DIRECT_TEMPLATES = ['index', 'categories', 'authors', 'archives']
RELATIVE_URLS = True

# Time
TIMEZONE = 'Asia/Shanghai'
DEFAULT_LANG = u'zh'

# Feed
FEED_DOMAIN = SITEURL
FEED_ATOM = 'feeds/atom.xml'
FEED_RSS = 'feeds/rss.xml'
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Menu
MENUITEMS = (('首页', '/'), ('归档', 'archives.html'))
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False

# Pagination
DEFAULT_PAGINATION = 20

# Output
DELETE_OUTPUT_DIRECTORY = True

# Theme
SOCIAL = (('Twitter', 'https://twitter.com/easedays'),
          ('Github', 'https://github.com/xdays'))

# Comment
DISQUS_SITENAME = 'xdays'

# Github
GITHUB_USER = 'xdays'
GITHUB_REPO_COUNT = 5 

# CacheMoment
CACHEMOMENT_REFER = True

# Goole Custom Search
GOOGLE_CSE_CODE = '008104676222079813428:xcoyettaqmw'

# Google Analyze
GOOGLE_ANALYTICS = 'UA-96220381-1'

# Google Adsense
GOOGLE_ADSENSE = True

PLUGINS = []

LINKS = [
    ('李爽', 'http://www.iamle.com'),
    ('培强', 'http://peiqiang.net'),
    ('钿田', 'http://blog.54im.com'),
    ('三斗室', 'http://chenlinux.com'),
    ('张斌', 'http://opslinux.com'),
    ('老徐', 'http://laoxu.blog.51cto.com'),
    ('邓磊', 'http://dl528888.blog.51cto.com'),
    ('沈灿', 'http://www.shencan.net'),
    ('胡阳', 'http://www.the5fire.com'),
    ('峰云', 'http://xiaorui.cc'),
    ('安静', 'http://www.80aj.com'),
    ('刘志', 'http://orangleliu.info/'),
    ('字母哥', 'http://n4mine.github.io/'),
    ('丰杰', 'https://www.zhoufengjie.cn/')
]
