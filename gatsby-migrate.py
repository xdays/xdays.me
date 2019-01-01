#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import glob
import re


src = sys.argv[1]
dest = sys.argv[2]
meta = ['Title', 'Date', 'Author', 'Category', 'Tags', 'Slug']

for file_path in glob.glob(src):
    filename = os.path.basename(file_path)
    print 'start process %s' % filename
    with open(file_path) as f:
        s = f.readlines()
    s.insert(0, '---\n')
    for i in range(0, len(s)):
        if s[i].startswith('Slug'):
            s.insert(i+1, '---\n')
            print 'Find slug meta data'
        elif s[i].startswith('Date:'):
            s[i] = ' '.join(s[i].split(' ')[:-1]) + '\n'
            print 'Process date meta data %s' % s[i]
    t = ''.join(s)
    for m in meta:
        t = t.replace(m, m.lower(), 1)
    t = re.sub(r'{filename}(.*)\.md', r'/\1/', t).replace('{filename}', '')
    with open(os.path.join(dest, filename), 'w') as g:
        g.write(t)
