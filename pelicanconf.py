#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Misc
AUTHOR = u'xdays'
SITENAME = u'xdays'
SITEURL = 'http://www.xdays.info'
KEYWORD = '架构，运维，开发, 生活随想'
PATH = 'content'
STATIC_PATHS = ['wp-content']
EXTRA_PATH_METADATA = {
    'wp-content/static/robots.txt': {'path': 'robots.txt'},
    'wp-content/static/favicon.ico': {'path': 'favicon.ico'},
}

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

# Goole Custom Search
CSE_CODE = '008104676222079813428:xcoyettaqmw'

PLUGINS = []
