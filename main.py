#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import xmpp

#from google.appengine.api import urlfetch
from datetime import datetime
import urllib2,md5,logging,csv,re,math

def ckinv(oo):
  """ check the value is date or not """
  pattern = re.compile(r"[0-9]{2}/[0-9]{2}/[0-9]{2}")
  b = re.search(pattern, oo[0])
  try:
    b.group()
    return True
  except:
    return False

def covstr(s):
  """ convert string to int or float. """
  try:
    ret = int(s)
  except ValueError:
    ret = float(s)
  return ret

############## webapp Models ###################
class MainPage(webapp.RequestHandler):
  def get(self):
    #url = 'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY_AVG/STOCK_DAY_AVG2.php?STK_NO=2363&myear=2010&mmon=06&type=csv'
    ''' 日期/成交股數/成交金額/開盤價/最高價/最低價/收盤價/漲跌價差/成交筆數 '''
    url = 'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report2010%(mon)02d/2010%(mon)02d_F3_1_8_%(stock)s.php&type=csv' % {'mon': datetime.today().month,'stock': '2363'}
    cc = urllib2.urlopen(url)
    csv_read = csv.reader(cc)

    self.response.out.write('Go Ri Stock')
    #csv_read.next
    getr = []
    for i in csv_read:
      print i
      if ckinv(i):
        getr.append(covstr(i[6]))
    print getr
    print "- Sum: %s" % math.fsum(getr)
    print "- Num: %s" % len(getr)
    print "- Avg: %.2f" % float(math.fsum(getr)/len(getr))
    print "- MA5: %.2f" % float(math.fsum(getr[-5:])/len(getr[-5:]))

############## main Models ###################
def main():
  """ Start up. """
  application = webapp.WSGIApplication(
                                      [
                                        ('/', MainPage)
                                      ],debug=True)
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
