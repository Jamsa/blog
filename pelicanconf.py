#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jamsa'
SITENAME = u'Jamsa的笔记'
SITEURL = ''

PATH = 'content'
STATIC_PATHS = ['devel','static','math','images','others']

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
#           ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = 'pelican-themes/pelican-fresh'

ORG_READER_EMACS_LOCATION = '/Users/zhujie/Applications/Emacs.app/Contents/MacOS/Emacs'
ORG_READER_BACKEND = "'html"
ORG_READER_EMACS_SETTINGS='org_reader_config.el'

PLUGIN_PATHS = ['pelican-plugins']

PLUGINS = [ "render_math","org_reader"]#"pelican-toc","org_pandoc_reader"



ORG_PANDOC_ARGS = ['--mathjax',
                   '--smart',
                   #'--toc',
                   #'--toc-depth=2',
                   '--standalone',
                   '--highlight-style=pygments',]


# MATH_JAX = {
#     'source':'https://cdn.bootcss.com/mathjax/2.7.0/MathJax.js'
#     }

#pelican_toc插件配置
TOC = {
    'TOC_HEADERS' : '^h[3-6]',  # What headers should be included in the generated toc
                                # Expected format is a regular expression

    'TOC_RUN'     : 'true'      # Default value for toc generation, if it does not evaluate
                                # to 'true' no toc will be generated
}
