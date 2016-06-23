# encoding: utf-8
import json
import os
import re
import sys
import time
import urllib
from string import strip

from bs4 import BeautifulSoup

from sina.dao import blog_dao

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

L1 = [1, 2, 3, 4, 5]
L2 = [20, 30, 40]
L1 = L1 + L2
print L1
file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)),
                    'test/Test_1466091593_log.html')
fres = open(file, "r").read()
print fres

BASEURL = "http://weibo.com/p/aj/v6/mblog/mbloglist?"
middleware1 = re.findall("domid\"\:\"Pl\_Core\_T8Cus(.*)\)\<", fres)  # print middleware1
middleware2 = re.findall("\"html\":\"(.*)\"}", middleware1[0])
resultHtml = middleware2[0].replace("\\r\\n", "").replace("\\t", "").replace("\\", "")
# print resultHtml
soup = BeautifulSoup(resultHtml, "html.parser")
count = soup.find_all("span", text="微博")[0].previous_element
blogpage = 1;
blogpages = int(count) / 45;
domians = re.findall("domain\'\]\=\'(.*)\'\;", fres)
if len(domians) == 0:
    exit()
domianId = domians[0]
print domianId
pageIds = re.findall("page\_id\'\]\=\'(.*)\'\;", fres)
if len(pageIds) == 0:
    exit()
pageId = pageIds[0]
print pageId
oids = re.findall("oid\'\]\=\'(.*)\'\;", fres)
if len(oids) == 0:
    exit()
oid = oids[0]
print oid

print blogpages
if count > 15:
    print "第一页第一次上滑刷新"
    postdata["domain"] = domianId
    postdata["domain_op"] = domianId
    postdata["id"] = pageId
    script_uri = "/u/" + oid
    postdata["script_uri"] = script_uri
    postdata["pagebar"] = 0
    postdata["page"] = 1
    postdata["pre_page"] = 1
    timeers = "%d" % (time.time() * 1000)
    postdata["__rnd"] = timeers
    datas = urllib.urlencode(postdata)
    fullUrl = BASEURL + datas
    print fullUrl
if count > 30:
    print "第一页第二次上滑刷新"
    postdata["domain"] = domianId
    postdata["domain_op"] = domianId
    postdata["id"] = pageId
    script_uri = "/u/" + oid
    postdata["script_uri"] = script_uri
    postdata["pagebar"] = 1
    postdata["page"] = 1
    postdata["pre_page"] = 1
    timeers = "%d" % (time.time() * 1000)
    postdata["__rnd"] = timeers
    datas = urllib.urlencode(postdata)
    fullUrl = BASEURL + datas
    print fullUrl
file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)),
                    'test/testfile')
fres = open(file, "r").read()
# print fres
s = json.loads(fres)
# print s['data']
soup = BeautifulSoup(s['data'], "html.parser")
divs = soup.find_all(class_="WB_cardwrap WB_feed_type S_bg2 ")
# 15条blog记录
blogs = []
count = 1;
for div2 in divs:
    print  "Analysis 第:", count, "条数据"
    blog = blog_dao.BlogDao()
    blog.user_id = oid;
    div = div2.find_all(class_="WB_detail")[0]
    divhandle = div2.find_all(class_="WB_feed_handle")[0]
    time = div.find_all(class_="WB_from S_txt2")
    blog.post_from = strip(time[0].text)
    # print strip(time[0].text)
    content = div.find_all(class_="WB_text W_f14")
    blog.post_content = strip(content[0].text)
    # print  strip(content[0].text)
    forward = div.find_all(class_="WB_feed_expand")
    if len(forward) != 0:
        warn = forward[0].find_all(class_="W_icon icon_warnS")
        if len(warn) != 0:
            continue
        forwardPeople = forward[0].find_all(class_="WB_info")
        forwardContent = forward[0].find_all(class_="WB_text")
        forwardTime = forward[0].find_all(class_="WB_from S_txt2")
        forwardCount = forward[0].find_all(class_="W_ficon ficon_forward S_ficon")
        repeatCount = forward[0].find_all(class_="W_ficon ficon_repeat S_ficon")
        praiseCount = forward[0].find_all(class_=re.compile("praised"))
        blog.forward['forward_reference'] = strip(forwardPeople[0].text)
        # print  10 * " ", strip(forwardPeople[0].text)
        blog.forward['forward_content'] = strip(forwardContent[0].text)
        # print  10 * " ", strip(forwardContent[0].text)
        blog.forward['forward_from'] = strip(forwardTime[0].text)
        # print  10 * " ", strip(forwardTime[0].text)
        if strip(forwardCount[0].next_sibling.text).__eq__('转发'):
            blog.forward['forward_count'] = 0
        else:
            blog.forward['forward_count'] = int(strip(forwardCount[0].next_sibling.text))
        if strip(repeatCount[0].next_sibling.text).__eq__('评论'):
            blog.forward['repeat_count'] = 0
        else:
            blog.forward['repeat_count'] = int(strip(repeatCount[0].next_sibling.text))
        # 淘宝推广会有两个赞标签
        if len(praiseCount) == 1:
            if strip(praiseCount[0].next_sibling.text).__eq__('赞'):
                blog.forward['praise_count'] = 0
            else:
                blog.forward['praise_count'] = int(strip(praiseCount[0].next_sibling.text))
        else:
            if strip(praiseCount[1].next_sibling.text).__eq__('赞'):
                blog.forward['praise_count'] = 0
            else:
                blog.forward['praise_count'] = int(strip(praiseCount[1].next_sibling.text))
                # print  10 * " ", strip(forwardCount[0].next_sibling.text), strip(
                #     repeatCount[0].next_sibling.text), strip(
                #     praiseCount[0].next_sibling.text)
    selfforwardCount = divhandle.find_all(class_="W_ficon ficon_forward S_ficon")
    selfrepeatCount = divhandle.find_all(class_="W_ficon ficon_repeat S_ficon")
    selfpraiseCount = divhandle.find_all(attrs={"action-type": "fl_like"})
    # print  40 * " "
    # print  40 * " "
    # print  40 * " "
    if strip(selfforwardCount[0].next_sibling.text).__eq__('转发'):
        blog.forward_count = 0
    else:
        blog.forward_count = int(strip(selfforwardCount[0].next_sibling.text))
    if strip(selfrepeatCount[0].next_sibling.text).__eq__('评论'):
        blog.repeat_count = 0
    else:
        blog.repeat_count = int(strip(selfrepeatCount[0].next_sibling.text))
    if strip(selfpraiseCount[0].text).__eq__('赞'):
        blog.praise_count = 0
    else:
        blog.praise_count = int(strip(selfpraiseCount[0].text))
    blogs.append(blog)
    count = count + 1
# print len(blogs)

divs = soup.find(class_="WB_cardwrap S_bg2")
# print divs
urls=[]
if divs != None:
    pageUrlList = divs.find('ul').find_all("a")
    for url in pageUrlList:
        print url.get("href")
        url = "http://weibo.com" + url.get("href")
        newurl = url.replace("pids=Pl_Official_MyProfileFeed__25&", "")
        if newurl.__contains__("&page=1") != True:
            urls.append(newurl)
        else:
            print "没有其余博客"
urls.reverse()
for url in urls:
    print url


# print s.keys()
# print s["name"]
# print s["type"]["name"]
# print s["type"]["parameter"][1]
# for blogpage in range(2, blogpages + 1):
#     # http://weibo.com/p/aj/v6/mblog/mbloglist?
#     # ajwvr=6&domain=100606
#     # &is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1
#     # &page=1&pagebar=0&pl_name=Pl_Official_MyProfileFeed__25
#     # &id=1006062371375560&script_uri=/p/1006062371375560/home&feed_type=0
#     # &pre_page=1&domain_op=100606&__rnd=1465957911461
#     postdata["domain"] = domianId
#     postdata["domain_op"] = domianId
#     postdata["id"] = pageId
#     script_uri = "/p/" + pageId + "/home"
#     postdata["script_uri"] = script_uri
#     postdata["pagebar"] = 0
#     postdata["page"] = 1
#     postdata["pre_page"] = 1
#     timeers = "%d" % (time.time() * 1000)
#     postdata["__rnd"] = timeers
#     datas = urllib.urlencode(postdata)
#     fullUrl = BASEURL + datas
#     print fullUrl

# & pagebar = 0
# & script_uri = / p / 1005053224112801 / home
# & page = 1
# & pre_page = 1
# http: // weibo.com / u / 1950632062?is_search = 0 & visible = 0 & is_all = 1 & is_tag = 0 & profile_ftype = 1 & page = 3  # feedtop
# http: // weibo.com / u / 1950632062?is_search = 0 & visible = 0 & is_all = 1 & is_tag = 0 & profile_ftype = 1 & page = 1  # feedto
