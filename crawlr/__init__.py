from cassandra.util import datetime_from_timestamp
from cassandra.query import dict_factory
from cassandra.cluster import Cluster
#import crawlr.db
import crawlr.util
import requests
import time
import bs4

__version__ = '0.0.1'

class Crawlr:
  def __init__(self, url):
    self.url = crawlr.util.normalize_url(url)
    self.tld = crawlr.util.get_tld(url)

    self.crawl_data = {}
    self.crawl_data['failure'] = False
    self.crawl_data['url'] = self.url
    self.crawl_data['id'] = crawlr.util.get_url_id(self.url)

    self.cassandra_cluster = ['127.0.0.1']
    self.keyspace = 'crawlr'
    self.cluster = Cluster(self.cassandra_cluster)
    self.session = self.cluster.connect(self.keyspace)
    self.session.row_factory = dict_factory

    # Prepared Cassandra queries.
    self.check_prepped_stmt = self.session.prepare(
      """
        SELECT id FROM pages WHERE id = ?;
      """)
    self.add_fail_prepped_stmt = self.session.prepare(
      """
        UPDATE failure_counts SET failures = failures + 1 WHERE id = ?;
      """)
    self.del_fail_prepped_stmt = self.session.prepare(
      """
        DELETE failures FROM failure_counts where id = ?;
      """)
    self.add_crawl_prepped_stmt = self.session.prepare(
      """
        INSERT INTO pages (
          id,
          url,
          crawled_at,
          failure,
          title,
          body,
          internal_links,
          outbound_links)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      """)

  def parse_links(self):
    links = []
    internal_links = []
    outbound_links = []

    for a in self.soup.findAll('a'):
      if a['href'].startswith('http'):
        links.append(crawlr.util.normalize_url(a['href']))

    # Remove dupe urls as we normalize them upon adding them to the list.
    links = list(set(links))

    for link in links:
      # The 3rd '/' in a normalized url seperates the domain from the path.
      if self.tld in link.split('/')[2]:
        internal_links.append(link)
      else:
        outbound_links.append(link)

    # I'm too lazy to fix this to get Cassandra to use a list. I can use .split(',') for now.
    self.crawl_data['internal_links'] = ','.join(internal_links)
    self.crawl_data['outbound_links'] = ','.join(outbound_links)

    return self.crawl_data['internal_links'], self.crawl_data['outbound_links']

  def parse_title(self):
    self.crawl_data['title'] = self.soup.html.head.title.get_text()
    return self.crawl_data['title']

  def parse_body(self):
    self.crawl_data['body'] = '\n'.join([''.join(s.findAll(text=True))for s in self.soup.findAll('p')])
    return self.crawl_data['body']

  def get_url(self):
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
      self.soup = bs4.BeautifulSoup(response.text)

  def crawl(self):
    self.crawl_data['crawled_at'] = int(time.time())
    self.get_url()
    if self.crawl_data['failure'] == False:
      self.parse_title()
      self.parse_body()
      self.parse_links()
    return self.crawl_data

  def add_crawl_failure(self):
    bound_stmt = self.add_fail_prepped_stmt.bind([self.crawl_data['id']])
    self.session.execute(bound_stmt)

  def reset_crawl_failures(self):
    bound_stmt = self.del_fail_prepped_stmt.bind([self.crawl_data['id']])
    self.session.execute(bound_stmt)

  def crawled_before(self):
    bound_stmt = self.check_prepped_stmt.bind([self.crawl_data['id']])
    rows = self.session.execute(bound_stmt)
    # Is empty if false, no record of crawl.
    return bool(rows)

  def write_crawl_data(self):
    bound_stmt = self.add_crawl_prepped_stmt.bind([
      self.crawl_data['id'],
      self.crawl_data['url'],
      datetime_from_timestamp(self.crawl_data['crawled_at']),
      self.crawl_data['failure'],
      self.crawl_data['title'],
      self.crawl_data['body'],
      self.crawl_data['internal_links'],
      self.crawl_data['outbound_links']])
    self.session.execute(bound_stmt)
