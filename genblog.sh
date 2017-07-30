#!/bin/bash
# -*- coding: utf-8 -*-
 
THEME_PATH=/tmp/attila
git clone https://github.com/zutrinken/attila.git $THEME_PATH
pelican-themes -U $THEME_PATH
export LANG=zh_CN.UTF-8 && pelican content/ $@
rm -rf $THEME_PATH
