# -*- coding:utf-8 -*-

import urllib2

url=""

headers={}
headers['User-agent']="Googlebot"

request=urllib2.Request(url,headers=headers)
response=urllib2.urlopen(request)

print response.read()
response.close()