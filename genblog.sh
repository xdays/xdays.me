#!/bin/sh
# -*- coding: utf-8 -*-
 
export LANG=zh_CN.UTF-8 && pelican -s pelicanconf.py content/ -t theme/ 
