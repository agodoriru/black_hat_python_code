# -*- coding:utf-8 -*-

import urllib2
import urllib
import threading
import Queue

threads=50
target_url="http://testphp/vulnweb.com"
wordlist_file="tmp/all.txt"
resume=None

#user_agent="Mozilla"

def build_wordlist(wordlist_file):
    fd=open(wordlist_file,"rb")
    raw_words=fd.readline()
    fd.close()

found_resume=False
words=Queue.Queue()

for word in raw_words:
    word=word.rstrip()
    
    if resume is not None:
        if found_resume:
            words.put(word)
        else:
            found_resume=True
            print "Resuming wordlist from %s"%resume
    else:
        words.put(word)

return words
    


