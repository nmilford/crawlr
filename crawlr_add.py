#!/usr/bin/env python
from crawlr_worker import crawl
import sys
for url in sys.argv[1:]: 
  print "Crawling: " + url
  data = crawl(url)
  print data['title']
