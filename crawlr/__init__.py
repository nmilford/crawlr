from tld import get_tld
import requests
import urlnorm
import time
import bs4

class Crawlr:
  def __init__(self, url):
    self.crawl_data = {}
    self.url = urlnorm.norm(url)
    self.tld = get_tld(url).encode('ascii','ignore')

  def url(self):
    return self.url

  def crawl(self):
    response = requests.get(self.url)
    soup = bs4.BeautifulSoup(response.text)
    self.crawl_data['crawled_at'] = int(time.time())
    self.crawl_data['title'] = soup.html.head.title.get_text().encode('ascii','ignore')
    self.crawl_data['body'] = '\n'.join([''.join(s.findAll(text=True))for s in soup.findAll('p')]).encode('ascii','ignore')
    self.crawl_data['internal_links'] = []
    self.crawl_data['outbound_links'] = []
    links = []
    for a in soup.findAll('a'):
      if a['href'].startswith('http'):
        links.append(urlnorm.norm(a['href']))

    links = list(set(links))

    for link in links:
      if self.tld in link.split('/')[2]:
        self.crawl_data['internal_links'].append(link)
      else:
        self.crawl_data['outbound_links'].append(link)

    return self.crawl_data
