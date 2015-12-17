A Crawlr worker pulls a URL off of the Celery/Redis queue.

[x] It first normalizes the url, then MurmurHashe128s the url.


The Hash of the url will be the primary ID for the url



It checks Cssandra if the URL exists


  if it does find it, it checks.


    the last crawl date and does not crawl it if now is less than X hours.


    the failure count, if the failure count is greater Y it skips it and exponentially backs off.

[x]  If it doesn't it crawls it


[x]    if it fails it adds it to the failure count in Cassandra and logs a reason.


[x]    if it succeeds it grabs the page and returns a dict with the fruit of the crawl.


Setup Environment
```
echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections
sudo add-apt-repository ppa:webupd8team/java
echo "deb http://debian.datastax.com/community stable main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
sudo apt-get update
sudo apt-get install oracle-java8-installer dsc30 cassandra-tools redis-server -y
sudo apt-get install build-essential python-pip python-bs4 python-requests python-celery python-dev libev4 libev-dev -y
sudo apt-get install nodejs-legacy npm -y
sudo pip install tld
sudo pip install mmh3
sudo pip install urlnorm
sudo pip install cassandra-driver
sudo npm -g install phantomjs
sudo pip install selenium

sudo /etc/init.d/cassandra start
cqlsh < crawlr.cql
```

from crawlr import Crawlr
a = Crawlr('http://www.fsdfd.om')
b = a.crawl()
