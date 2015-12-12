from tld import get_tld
import requests
import urlnorm
import time
import mmh3
import bs4

class Crawlr:
  """
  Crawls a given URL and returns a dict containing
  {
    'failures': integer of the number of failures,
    'url_id': MurmerHash3 of the normalized URL to use as an ID,
    'url': normalized URL,
    'crawled_at': integer of the unixtime of the crawl,
    'title': string of the URL's title,
    'body': string of the URL's text,
    'internal_links': list of links containing the original URL's TLD,
    'external_links': list of links not containing the original URL's TLD
  }
  """

  def __init__(self, url):
    self.url = urlnorm.norm(url)
    self.tld = get_tld(url).encode('ascii','ignore')

    self.crawl_data = {}
    self.crawl_data['failure'] = False
    self.crawl_data['url'] = self.url
    self.crawl_data['id'] = mmh3.hash128(self.url)

  def url(self):
    return self.url

  def id(self):
    return self.crawl_data['id']

  def crawl(self):
    self.crawl_data['crawled_at'] = int(time.time())

    headers = {'user-agent': 'crawlr/0.0.1'}

    try:
      response = requests.get(self.url, headers=headers)
    except requests.exceptions.Timeout:
      self.crawl_data['failure'] = True
      self.crawl_data['last_failure'] = 'Timeout'
    except requests.exceptions.ConnectionError:
      self.crawl_data['failure'] = True
      self.crawl_data['last_failure'] = 'ConnectionError'
    except requests.exceptions.HTTPError:
      self.crawl_data['failure'] = True
      self.crawl_data['last_failure'] = 'HTTPError'
    except requests.exceptions.TooManyRedirects:
      self.crawl_data['failure'] = True
      self.crawl_data['last_failure'] = 'TooManyRedirects'
    except requests.exceptions.RequestException as e:
      self.crawl_data['failure'] = True
      self.crawl_data['last_failure'] = e 

    if self.crawl_data['failure'] == False: 
      soup = bs4.BeautifulSoup(response.text)
      self.crawl_data['title'] = soup.html.head.title.get_text() #.encode('ascii','ignore')
      self.crawl_data['body'] = '\n'.join([''.join(s.findAll(text=True))for s in soup.findAll('p')]) #.encode('ascii','ignore')
      self.crawl_data['internal_links'] = []
      self.crawl_data['outbound_links'] = []
      links = []
      for a in soup.findAll('a'):
        if a['href'].startswith('http'):
          links.append(urlnorm.norm(a['href']))

      # Remove dupe urls as we normalize them upon adding them to the list.
      links = list(set(links))

      for link in links:
        # The 3rd '/' in a normalized url seperates the domain from the path.
        if self.tld in link.split('/')[2]:
          self.crawl_data['internal_links'].append(link)
        else:
          self.crawl_data['outbound_links'].append(link)

    return self.crawl_data
