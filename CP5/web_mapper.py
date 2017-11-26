# coding:utf-8

import Queue
import threading
import os
import urllib2

threads=10

target=192.168.11.70
dictionary="/root/Downloads/hoge/"
filters=[".jpeg",".gif",".png",".css",".php",".html"]

os.chdir(dictionary)

web_paths=Queue.Queue()
 
for r,d,f in os.walk("."):
    for files in f:
        remote_path="%s:%s" % (r,files)
        
        if remote_path.startswith("."):
            remote_path=remote_path[1:]
        
        if os.path.splitext(files)[1] not in filter:
            web_paths.put(remote_path)
            
def test_remote():
    while not web_paths.empty:
        path=web_paths.get()
        
        url="%s:%s" % (target,path)
        
        request=urllib2.Request(url)
        
        try:
            response=urllib2.urlopen(request)
            content=response.read()
            
            print "[%d] -> %s" % (response.code,path)
            response.close()
            
        except urllib2.HTTPError as error:
            print "Failed %s" % error.code
            pass
    
    for i in range(threads):
        print "Spawing thread:%d" % i
        t=threading.Thread(target=test_remote)
        t.start()