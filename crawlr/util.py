import tld
import urlnorm
import mmh3

def normalize_url(url):
  return urlnorm.norm(url)

def get_url_id(url):
  return mmh3.hash64(normalize_url(url))[0]

def get_tld(url):
  return tld.get_tld(url).encode('ascii','ignore')


