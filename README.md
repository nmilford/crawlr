A Crawlr worker pulls a URL off of the Celery/Redis queue.

It first normalizes the url, then MurmurHashes the url.  The Hash of the url will

It checks Cssandra if the URL exists
  if it does find it, it checks
    the last crawl date and does not crawl it if now is less than X hours
    the failure count, if the failure count is greater Y it skips it and exponentially backs off 
    
  if it doesnt it crawls it
    if it fails it adds it to the failure count in Cassandra
    if it succeeds
