# encoding: utf-8
import base64
import binascii
import cookielib
import json
import re
import sys
import urllib
import urllib2

import rsa

import html_downloader
import html_outputer
import html_parser
import url_manager

reload(sys)
sys.setdefaultencoding("utf-8")
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


# 封装一个用于get的函数，新浪微博这边get出来的内容编码都是-8，所以把utf-8写死在里边了，真实项目中建议根据内容实际编码来决定
def getData(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    text = response.read().decode('utf-8')
    return text


def get_servertime():
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


def get_pwd(pwd, servertime, nonce):
    global pubkey
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd)  # 拼接明文js加密文件中得到
    passwd = rsa.encrypt(message, key)  # 加密
    passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
    return passwd


def get_user(username):
    username_ = urllib.quote(username)
    username = base64.encodestring(username_)[:-1]
    return username


def login():
    username = '18051352830'
    pwd = 'lshdxw0801'
    url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    try:
        servertime, nonce, rsakv = get_servertime()
    except:
        return
    global postdata
    postdata['servertime'] = servertime
    postdata['nonce'] = nonce
    postdata['rsakv'] = rsakv
    postdata['su'] = get_user(username)
    postdata['sp'] = get_pwd(pwd, servertime, nonce)
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
    print login_url
    print 30 * "*"
    try:
        result1 = urllib2.urlopen(login_url).read()
        fres = open("loginResult.html", "w")
        fres.write(result1)
        fres.close()
        print u"登录成功!"  # 是否登录成功还要看result1的内容是否是别的什么，
        url2 = "http://weibo.com"
        req = urllib2.Request(url2)
        html = urllib2.urlopen(req).read()
        # tpl?containerid=1005052573805580_-_FOLLOWERS
        # 读取文件获得字符串
        # 获取自己的uid
        lst = re.findall("CONFIG\['uid'\]='(.*)'", html)
        uid = lst[0]
        # 拼接成粉丝列表url  http://weibo.com/2573805580/fans?rightmod=1&wvr=6
        fansUrl = "http://weibo.com/" + uid + "/fans?rightmod=1&wvr=6";
        # 获取粉丝列表中数据
        hts = getUrlData(fansUrl)
        f_query1 = open("fans.htm", "w")
        f_query1.write(hts)
        f_query1.close()
    except Exception, e:
        print 'Login error!'
        print e


def getUrlData(url):
    req = urllib2.Request(url)
    html = urllib2.urlopen(req).read()
    return html


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self):
        return


if __name__ == "__main__":
    obj_spiner = SpiderMain()
    login()
