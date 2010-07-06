#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2010 Toomore Chiang, http://toomore.net/
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from datetime import datetime, timedelta
import urllib2, logging, csv, re

class goristock(object):

  def __init__(self,stock_no,data_num = 75):
    """
    stock_no: stock no.
    data_num: default fetch numbers.(Default is 75)
    """
    self.raw_data = []
    self.stock_name = ''
    self.stock_no = stock_no
    self.data_date = []
    starttime = 0

    try:
      while len(self.raw_data) < data_num:
        self.csv_read = self.fetch_data(stock_no, datetime.today() - timedelta(days = 30 * starttime))
        result = self.list_data(self.csv_read)
        self.raw_data = result['getr'] + self.raw_data
        self.data_date = result['data_date'] + self.data_date
        self.stock_name = result['stock_name']
        starttime += 1
    except:
      logging.info('Data not enough! %s' % stock_no)

    logging.info('Fetch %s' % stock_no)

  def covstr(self,s):
    """ convert string to int or float. """
    try:
      ret = int(s)
    except ValueError:
      ret = float(s)
    return ret

  def ckinv(self,oo):
    """ check the value is date or not """
    pattern = re.compile(r"[0-9]{2}/[0-9]{2}/[0-9]{2}")
    b = re.search(pattern, oo[0])
    try:
      b.group()
      return True
    except:
      return False

  def fetch_data(self, stock_no, nowdatetime):
    """ Fetch data from twse.com.tw """
    url = 'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report%(year)d%(mon)02d/%(year)d%(mon)02d_F3_1_8_%(stock)s.php&type=csv' % {'year': nowdatetime.year, 'mon': nowdatetime.month,'stock': stock_no}
    print url
    logging.info(url)
    cc = urllib2.urlopen(url)
    csv_read = csv.reader(cc)
    return csv_read

  def list_data(self, csv_read):
    """ Put the data into the 'self.raw_data' """
    getr = []
    getdate = []
    otherinfo = []
    for i in csv_read:
      if self.ckinv(i):
        print i
        getr.append(self.covstr(i[6]))
        getdate.append(i[0])
      else:
        otherinfo.append(i[0])

    stock_name = otherinfo[0].split(' ')[2].decode('big5').encode('utf-8')
    data_date = getdate
    return_value = {
      'getr': getr,
      'stock_name': stock_name,
      'data_date': data_date
    }
    print otherinfo
    print stock_name
    return return_value

  @property
  def num_data(self):
    """ Number of data. """
    return len(self.raw_data)

  @property
  def sum_data(self):
    """ Sum of data. """
    return sum(self.raw_data)

  @property
  def avg_data(self):
    """ Average of data. """
    return float(self.sum_data/self.num_data)

  def MA(self,days):
    """ Moving Average with days. """
    return float(sum(self.raw_data[-days:]) / days)

  def MAC(self,days):
    """ Comparing yesterday is high or low. """
    yesterday = self.raw_data[:]
    yesterday.pop()
    yes_MA = float(sum(yesterday[-days:]) / days)
    today_MA = self.MA(days)
    if today_MA > yes_MA:
      return '↑'
    elif today_MA < yes_MA:
      return '↓'
    else:
      return '-'
