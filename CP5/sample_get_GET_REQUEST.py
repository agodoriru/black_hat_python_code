#! /usr/bin/env python
# -*- coding:utf-8 -*-

import urllib2

body=urllib2.urlopen("http://www.tus.ac.jp")

print body.read()