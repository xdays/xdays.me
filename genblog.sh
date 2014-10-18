#!/bin/sh
# -*- coding: utf-8 -*-
 
export LANG=zh_CN.UTF-8 && cd /web/blog && pelican -s pelicanconf.py content/ -t theme/ 
