#python ./crawlr_worker.py  --concurrency=10 worker -l info
from celery import Celery
from crawlr import Crawlr

app = Celery('crawlr', broker='redis://localhost')

@app.task
def crawl(url):
  new = Crawlr(url)
  return new.crawl()

if __name__ == '__main__':
    app.start()
