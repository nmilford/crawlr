from crawlr import Crawlr
import crawlr.worker
import crawlr.server
import crawlr
import sys

def crawl(url):
  new = Crawlr(url)
  return new.crawl()

def version():
  print "Crawlr %s" % crawlr.__version__

def usage():
  usage = """
  usage: %s cmd [arg ...]

  Commands:

    crawl     Crawls the URLs specified after the command (separated by spaces).
    api       Spawns a Crawlr REST API server.
    worker    Spawns a Crawlr worker.
    usage     Prints this message.
    version   Prints the version.
  """ % sys.argv[0]

  print usage

def main():
  if len(sys.argv) == 1:
    usage()
    sys.exit(-1)

  if sys.argv[1] == 'crawl':
    if len(sys.argv) == 2:
      usage()
      sys.exit(-1)
    else:
      for url in sys.argv[2:]:
        print "Crawling: " + url
        payload = crawl(url)
        print payload['id']
  elif sys.argv[1] == 'api':
    crawlr.server.start()
  elif sys.argv[1] == 'worker':
    crawlr.worker.start()
  elif sys.argv[1] == 'version':
    version()
  else:
    usage()
    sys.exit(-1)


