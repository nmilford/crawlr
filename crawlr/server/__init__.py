from flask import Flask
from flask import jsonify
from flask import request
from crawlr import Crawlr

app = Flask(__name__)

@app.route('/crawl', methods=["POST"])
def crawl():
  url = request.get_json()['url']

  crawler = Crawlr(url)
  data = crawler.crawl()

  payload = {
    'status': 'OK',
    'url': data['url'],
    'id': data['id'],
    'crawled_at': data['crawled_at'],
    'title': data['title'],
    'body': data['body'],
    'internal_links': data['internal_links'],
    'outbound_links': data['outbound_links']
  }

  return jsonify(payload)

def start():
  app.run(host='0.0.0.0')

  # curl -H "Content-Type: application/json" -X POST -d '{"url":"http://www.clockworkfoundry.com"}' http://127.0.0.1:5000/crawl
