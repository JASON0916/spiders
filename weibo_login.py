# coding: utf-8
# @Date    : 2014-11-20 12:35:39
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


import urllib
import urllib2
import cookielib
import base64
import re
import json
import rsa
import binascii


class crawler(object):

    def __init__(self, username, pwd):
        self.username = username
        self.pwd = pwd
        self.initial_cookie()
        self.login()

    def initial_cookie(self):
        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

    def login(self):
        postdata={
           'cdult': '3',
           'entry': 'account',
           'gateway': '1',
           'from': '',
           "savestate": '30',
           'userticket': '0',
           'pagerefer': '',
           'geteway': '1',
           'rsakv': '1330428213',
           'prelt': '317',
           'su': '',
           'service': 'sso',
           'servertime': '',
           'nonce': '',
           'pwencode': 'rsa2',
           'sp': '',
           'encoding': 'UTF-8',
           'domain': 'sina.com.cn',
           'returntype': 'TEXT',
           'vsnf': '1'
        }
        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.3.18)'
        try:
            servertime, nonce = self.get_servertime()
            # print servertime,nonce
        except Exception, e:
            print 'call get_servertime() error'
            print e.message
            return None

        postdata['servertime'] = servertime
        postdata['nonce'] = nonce
        postdata['su'] = self.get_user(self.username)
        postdata['sp'] = self.get_pwsd(self.pwd, servertime, nonce)
        postdata = urllib.urlencode(postdata)

        headers = {'User-Agent':'Mozilla/5.0 (X11;Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}
        req = urllib2.Request(
            url=url,
            data=postdata,
            headers=headers
            )
        result = urllib2.urlopen(req)
        text = result.read()
        print text
        dic = json.loads(text)
        print dic
        # print dic['crossDomainUrlList'][0]
        # print dic['crossDomainUrlList'][1]
        # p =re.compile('location\.replace\"(.∗?)\"')

        try:
            # login_url=p.search(text).group(1)
            login_url = dic['crossDomainUrlList'][0]
            urll = urllib2.urlopen(login_url).read()
            # for index, cookie in enumerate(cj):
            #    print '[',index, ']',cookie;
            urll2 = urllib2.urlopen(dic['crossDomainUrlList'][1]).read()
            print "login succesfully!", urll
            print urll2

        except Exception, e:
            print'Login error!'
            print e.message
            return None

    @staticmethod
    def get_servertime():
        url = 'http://login.sina.com.cn/sso/prelogin.php?' \
               'entry=weibo&callback=sinaSSOController.preloginCallBack&' \
               'su=dW5kZWZpbmVk&client=ssologin.js(v1.3.18)%lih211@sina.com'

        data = urllib2.urlopen(url).read()
        p = re.compile('(sinaSSOController\.preloginCallBack\()(\S.*)(\))')

        try:
            json_data = p.search(data).group(2)
            print json_data
            data = json.loads(json_data)
            servertime = str(data['servertime'])
            nonce = str(data['nonce'])
            return servertime, nonce
        except Exception, e:
            print'get servertime error'
            print e.message
            return None

    @staticmethod
    def get_pwsd(pwd, servertime, nonce):
        # pwd1=hashlib.sha1(pwd).hexdigest()
        # pwd2=hashlib.sha1(pwd1).hexdigest()
        # pwd3_ =""+pwd2 + servertime +nonce
        # pwd3=hashlib.sha1(pwd3_).hexdigest()
        # return pwd3

        pubkey = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB' \
                 '2D245A87AC253062882729293E5506350508E7F9AA3BB77F43' \
                 '33231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB78' \
                 '4ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6' \
                 '739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
        rsaPublickey = int(pubkey, 16)
        pub_key = rsa.PublicKey(rsaPublickey, int('10001', 16))
        pwd = '%s\t%s\n%s' % (servertime, nonce, pwd)
        pwd1 = rsa.encrypt(pwd, pub_key)
        pwd1 = binascii.b2a_hex(pwd1)
        return pwd1

    @staticmethod
    def get_user(username):
        username1 = urllib.quote(username)
        username = base64.encodestring(username1)[:-1]
        return username

if __name__ == '__main__':
    cm = crawler('jason0916phoenix@126.com', 'chenminghaolihai')