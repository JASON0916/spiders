#!/usr/bin/env python
# coding=utf-8
import urllib2
import os
import cookielib
import re

BASE_URL = 'http://s2.hxen.com/m2'


class Base_Crawler(object):
    """
    basic crawler
    """
    file_path = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, title, file_path=file_path):
        self.url = BASE_URL + title
        self.path = file_path
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                       'Accept-Encoding': 'gzip, deflate, sdch',
                       'Accept-Language': 'zh-CN,zh;q=0.8',
                       'Connection': 'keep-alive',
                       'Host': 's2.hxen.com',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36'
                       }
        self.initial_cookie()

    def initial_cookie(self):
        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

    def download(self):
        req = urllib2.Request(url=self.url, headers=self.header)
        try:
            result = urllib2.urlopen(req).read()
        except urllib2.HTTPError as e:
            print 'reason: {0}'.format(e.reason)
        with open(self.path + '/' + self.url.split('/')[-1], 'w') as file:
            file.write(result)


class Bbc_Crawler(Base_Crawler):
    """
    used to download bbc news mp3
    """
    from time import strftime, localtime, time
    file_path = os.path.dirname(os.path.abspath(__file__)) + '/BBC'
    localdate = strftime('%Y/%m/%d', localtime(time()))

    def __init__(self, date=localdate, file_path=file_path):
        date_list = date.split('/')
        if len(date_list) != 3:
            print 'date format wrong!!!'
            raise ValueError
        title = '/BBC/{year}/{month}/{date}BBC.mp3'.format(
            year=date_list[0], month=date_list[1], date=date.replace('/', ''))
        Base_Crawler.__init__(self, title, file_path)


class Cnn_Crawler(Base_Crawler):
    """
    used to download CNN news mp3
    """
    from time import strftime, localtime, time
    file_path = os.path.dirname(os.path.abspath(__file__)) + '/CNN'
    localdate = strftime('%Y/%m/%d', localtime(time()))

    def __init__(self, date=localdate, file_path=file_path):
        date_list = date.split('/')
        if len(date_list) != 3:
            print 'date format wrong!!!'
            raise ValueError
        title = '/cnn/{year}/{month}/{date}CNN.mp3'.format(
            year=date_list[0], month=date_list[1], date=date.replace('/', ''))
        Base_Crawler.__init__(self, title, file_path)


class Voa_Crawler(Base_Crawler):
    # voa: http://s2.hxen.com/m2/standard/2015/09/hxen.com_s20150903c.mp3
    """
    used to download Voa news mp3
    """
    from time import strftime, localtime, time
    file_path = os.path.dirname(os.path.abspath(__file__)) + '/voa'
    localdate = strftime('%Y/%m/%d', localtime(time()))

    def __init__(self, date=localdate, file_path=file_path):
        date_list = date.split('/')
        if len(date_list) != 3:
            print 'date format wrong!!!'
            raise ValueError
        # http://www.hxen.com/englishlistening/voaenglish/voastandardenglish/20150903/400865.html
        self.urls = self.preprocess(date)
        self.path = file_path
        Base_Crawler.__init__(self, '', file_path)


    @staticmethod
    def preprocess(
        localdate, url='http://www.hxen.com/englishlistening/voaenglish/voastandardenglish/'):
        base_page = urllib2.urlopen(url).read()
        date = localdate.replace('/', '')
        urls_to_process = re.findall('\/englishlistening\/voaenglish\/voastandardenglish\/'+str(date)+'\/\d*\.html', base_page)
        # http://s2.hxen.com/m2/standard/2015/09/hxen.com_s20150903c.mp3
        date_list = localdate.split('/')
        base_url_file = 'http://s2.hxen.com/m2/standard/{year}/{month}/hxen.com_s{date}'.format(year=date_list[0], month=date_list[1], date=date)
        url_to_download = [base_url_file+chr(i+97)+'.mp3' for i in range(len(urls_to_process))]
        return url_to_download

    def download(self):
        for url in self.urls:
            req = urllib2.Request(url=url, headers=self.header)
            try:
                result = urllib2.urlopen(req).read()
                with open(self.path + '/' + url.split('/')[-1], 'w') as file:
                    file.write(result)
            except urllib2.HTTPError as e:
                print 'error reason: {reason}'.format(reason=e.reason)
            

if __name__ == '__main__':
    a = Voa_Crawler()
    a.download()
