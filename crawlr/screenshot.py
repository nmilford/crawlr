from selenium import webdriver
import crawlr.util

class ScreenShot:
  def __init__(self, url, keywords=[]):
    self.url = crawlr.util.normalize_url(url)
    self.id = crawlr.util.get_url_id(self.url)
    self.keywords = keywords
    self.filename = str(self.id) + '.png'
    self.browser = webdriver.PhantomJS()
    self.browser.set_window_size(1024, 768)
    self.browser.get(url)

  def highlight_keywords(self):
    for keyword in self.keywords:
      js = """
        var from = "%s";
        var to = "<span style='background-color: #FFFF00; color:black;'>" + from + "</span>";
        document.body.innerHTML = document.body.innerHTML.replace(/from/g, to);
      """ % keyword

      self.browser.execute_script(js)

  def write_screenshot(self):
    if self.keywords:
      self.highlight_keywords()

    self.browser.save_screenshot(self.filename)





