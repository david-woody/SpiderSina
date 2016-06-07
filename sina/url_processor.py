# encoding: utf-8
import base64
import cookielib
import json
import os
import sys
import urllib
import urllib2

import re

import binascii

import rsa

pubkey = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)
postdata = {
    'entry': 'weibo',
    'gateway': '1',
    'from': '',
    'savestate': '7',
    'userticket': '1',
    'ssosimplelogin': '1',
    'vsnf': '1',
    'su': '',
    'service': 'miniblog',
    'servertime': '',
    'nonce': '',
    'pwencode': 'rsa2',
    'sp': '',
    'pagerefer': 'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F',
    'raskv': '',
    'sr': '1440*900',
    'prelt': '94',
    'encoding': 'UTF-8',
    'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
    'returntype': 'META'
}


class UrlProcesser(object):
    def get_servertime(self):
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=dW5kZWZpbmVk&client=ssologin.js(v1.3.18)&_=1329806375939'
        data = urllib2.urlopen(url).read()
        p = re.compile('\((.*?)\)')
        try:
            json_data = p.search(data)
            text = json_data.group(0)
            text = text.replace("(", "")
            text = text.replace(")", "")
            data = json.loads(text)
            servertime = str(data['servertime'])
            nonce = data['nonce']
            rsakv = data['rsakv']
            return servertime, nonce, rsakv
        except:
            print 'Get severtime error!'
            return None

    def get_pwd(self, pwd, servertime, nonce):
        global pubkey
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd)  # 拼接明文js加密文件中得到
        passwd = rsa.encrypt(message, key)  # 加密
        passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
        return passwd

    def get_user(self, username):
        username_ = urllib.quote(username)
        username = base64.encodestring(username_)[:-1]
        return username

    def login(self, username, pwd):
        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        print  "用户名:", username
        print  "密  码:", pwd
        try:
            servertime, nonce, rsakv = self.get_servertime()
        except:
            return
        global postdata
        postdata['servertime'] = servertime
        postdata['nonce'] = nonce
        postdata['rsakv'] = rsakv
        postdata['su'] = self.get_user(username)
        postdata['sp'] = self.get_pwd(pwd, servertime, nonce)
        postdata = urllib.urlencode(postdata)
        headers = {
            'User-Agent': 'UCWEB/2.0 (Linux; U; Adr 2.3; zh-CN; MI-ONEPlus) U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile'}
        req = urllib2.Request(
            url=url,
            data=postdata,
            headers=headers
        )
        result = urllib2.urlopen(req)
        loginPre = result.read()
        lst = re.findall("location\.replace\('(.*)'", loginPre)
        login_url = lst[0]
        # print login_url
        print 30 * "*"
        try:
            result = urllib2.urlopen(login_url).read()
            file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)),
                                'log\\loginResult.htm')
            fres = open(file, "w")
            fres.write(result)
            fres.close()
            if result.__contains__("true"):
                return True
            else:
                return False
        except Exception, e:
            print e
            return False

    def getUrlData(self, url):
        req = urllib2.Request(url)
        html = urllib2.urlopen(req).read()
        return html

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding("utf-8")
        return

    def getUrlsDatas(self, fansUrls):
        htmls=[]
        for fanUrl in fansUrls:
            req = urllib2.Request(fanUrl)
            html = urllib2.urlopen(req).read()
            f_query1 = open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)),
                                'log\\test.htm'), "w")
            f_query1.write(html)
            f_query1.close()
            htmls.append(html)
        return htmls