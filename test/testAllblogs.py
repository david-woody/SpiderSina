# encoding: utf-8
import os
import re
import sys

import time
import urllib

from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')
postdata = {
    'ajwvr': '6',
    'domain': '',
    'is_search': '0',
    'visible': '0',
    'is_all': '1',
    'is_tag': '0',
    'profile_ftype': '1',
    'page': '',
    'pagebar': '',
    'pl_name': 'Pl_Official_MyProfileFeed__25',
    'id': '',
    'script_uri': 'rsa2',
    'feed_type': '0',
    'pre_page': '',
    'domain_op': '',
    '__rnd': '',
}
file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)),
                    'test/Test_1466091593_log.html')
fres = open(file, "r").read()
print fres
middleware1 = re.findall("domid\"\:\"Pl\_Core\_T8Cus(.*)\)\<", fres)  # print middleware1
middleware2 = re.findall("\"html\":\"(.*)\"}", middleware1[0])
resultHtml = middleware2[0].replace("\\r\\n", "").replace("\\t", "").replace("\\", "")
# print resultHtml
soup = BeautifulSoup(resultHtml, "html.parser")
count = soup.find_all("span", text="微博")[0].previous_element
blogpage = 1;
blogpages = int(count) / 45;
print blogpages


for blogpage in range(1,blogpages+1):
    # http://weibo.com/p/aj/v6/mblog/mbloglist?
    # ajwvr=6&domain=100606
    # &is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1
    # &page=1&pagebar=0&pl_name=Pl_Official_MyProfileFeed__25
    # &id=1006062371375560&script_uri=/p/1006062371375560/home&feed_type=0
    # &pre_page=1&domain_op=100606&__rnd=1465957911461
    global postdata
    postdata["__rnd"]=str("%d" % (time.time()*1000))
    postdata = urllib.urlencode(postdata)
    print postdata


