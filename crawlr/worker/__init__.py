from celery import Celery
from crawlr import Crawlr

app = Celery('crawlr', broker='redis://localhost')

@app.task
def crawl(url):
  new = Crawlr(url)
  return new.crawl()

def start():
  app.start(argv=['celery', '--concurrency=10 ', 'worker', '-l', 'info'])

# call via
#from crawlr.worker import crawl
#result = crawl('http://www.clockworkfoundry.com/')