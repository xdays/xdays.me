#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Misc
SITEURL = 'http://xdays.me'
AUTHOR = u'xdays'
SITENAME = u'xdays'
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
FEED_ATOM = None
FEED_ATOM = None

# Menu
MENUITEMS = (('首页', '/'),)
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False

# Pagination
DEFAULT_PAGINATION = 20

# Output
DELETE_OUTPUT_DIRECTORY = True

DISQUS_SITENAME = 'xdays'

# Github
GITHUB_USER = 'xdays'
GITHUB_REPO_COUNT = 5 

# Goole Custom Search
CSE_CODE = '008104676222079813428:xcoyettaqmw'

PLUGINS = []
