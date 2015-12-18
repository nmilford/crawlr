from crawlr import Crawlr
from crawlr.screenshot import ScreenShot
import crawlr.worker
import crawlr.server
import crawlr
import sys

def crawl(url):
  new = Crawlr(url)
  return new.crawl()

def grab_screenshot(url, keywords = []):
  new = ScreenShot(url, keywords)
  filename = new.write_screenshot()
  print 'Screenshot written to: %s' % filename

def version():
  print "Crawlr %s" % crawlr.__version__

def usage():
  usage = """
  usage: %s cmd [arg ...]

  Commands:

    crawl       Crawls the URLs specified after the command (separated by spaces).
    api         Spawns a Crawlr REST API server.
    worker      Spawns a Crawlr worker.
    screenshot  Crawls a page and returns a screenshot of it. Optionally, highlights
                keywords listed after the url.
    usage       Prints this message.
    version     Prints the version.
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
  elif sys.argv[1] == 'screenshot':
    if len(sys.argv) == 2:
      usage()
      sys.exit(-1)
    elif len(sys.argv) == 3:
      grab_screenshot(sys.argv[2])
    else:
      grab_screenshot(sys.argv[2], sys.argv[3:])
  elif sys.argv[1] == 'version':
    version()
  else:
    usage()
    sys.exit(-1)


