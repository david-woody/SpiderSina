# encoding: utf-8
import os
import re
from string import strip
import json
from bs4 import BeautifulSoup

# BASE_DIR = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
# print BASE_DIR
# file_path = os.path.join(BASE_DIR, 'test')
# print file_path
# file=os.path.join(file_path, 'text.txt')
# print file
# BASE_DIR = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
# filePath=str(BASE_DIR)+"/test/text.txt";
# currentPathName=os.getcwd() #当前路径
# file=os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'test\\testBlog.htm')
# # print file
# fres = open(file, "r").read()
# middleware1 = re.findall("pl\.relation\.fans\.index(.*)", fres)
# # print middleware1
# middleware2 = re.findall("\"html\":\"(.*)\"}\)", middleware1[0])
# # print middleware2
# resultHtml = middleware2[0].replace("\\r\\n", "").replace("\\n", "").replace("\\", "")
# # print resultHtml
# soup = BeautifulSoup(resultHtml, "lxml")
# allHref = soup.find_all("a", class_="S_txt1", target="_blank")
# for href in allHref:
#     print href.string
# fres.write(str)
# if result.__contains__("true"):
#     print "true"
# else:
#     print  "false"
import db_helper
from sina.dao import blog_dao
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
blog = {
    'post_from': '',
    'post_content': '',
    'forward': {
        "forward_reference": '',
        "forward_content": '',
        "forward_from": '',
        "forward_count": 0,
        "repeat_count": 0,
        "praise_count": 0
    },
    'forward_count': 0,
    'repeat_count': 0,
    'praise_count': 0,
}
dbhelper = db_helper.DBclient()
dbcollection = dbhelper.get_collection("sina_blog")
file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'tlogs\\3280269014_log.html')
fres = open(file, "r").read()
print fres
middleware1 = re.findall("domid\"\:\"Pl\_Official\_MyProfileFeed(.*)\)\<", fres)
middleware2 = re.findall("\"html\":\"(.*)\"}", middleware1[0])
resultHtml = middleware2[0].replace("\\r\\n", "").replace("\\n", "").replace("\\", "")
soup = BeautifulSoup(resultHtml, "html.parser")
divs = soup.find_all(class_="WB_cardwrap WB_feed_type S_bg2 ")
for div2 in divs:
    blog = blog_dao.BlogDao()
    div = div2.find_all(class_="WB_detail")[0]
    divhandle = div2.find_all(class_="WB_feed_handle")[0]
    time = div.find_all(class_="WB_from S_txt2")
    blog.post_from = strip(time[0].text)
    print strip(time[0].text)
    content = div.find_all(class_="WB_text W_f14")
    blog.post_content = strip(content[0].text)
    print  strip(content[0].text)
    forward = div.find_all(class_="WB_feed_expand")
    if len(forward) != 0:
        warn=forward[0].find_all(class_="W_icon icon_warnS")
        if len(warn) != 0:
            print  "warn"
        forwardPeople = forward[0].find_all(class_="WB_info")
        forwardContent = forward[0].find_all(class_="WB_text")
        forwardTime = forward[0].find_all(class_="WB_from S_txt2")
        forwardCount = forward[0].find_all(class_="W_ficon ficon_forward S_ficon")
        repeatCount = forward[0].find_all(class_="W_ficon ficon_repeat S_ficon")
        praiseCount = forward[0].find_all(class_=re.compile("praised"))
        blog.forward['forward_reference'] = strip(forwardPeople[0].text)
        print  10 * " ", strip(forwardPeople[0].text)
        blog.forward['forward_content'] = strip(forwardContent[0].text)
        print  10 * " ", strip(forwardContent[0].text)
        blog.forward['forward_from'] = strip(forwardTime[0].text)
        print  10 * " ", strip(forwardTime[0].text)
        if strip(forwardCount[0].next_sibling.text).__eq__('转发'):
            blog.forward['forward_count'] = 0
        else:
            blog.forward['forward_count'] = int(strip(forwardCount[0].next_sibling.text))
        if strip(repeatCount[0].next_sibling.text).__eq__('评论'):
            blog.forward['repeat_count'] = 0
        else:
            blog.forward['repeat_count'] = int(strip(repeatCount[0].next_sibling.text))
        if strip(praiseCount[0].next_sibling.text).__eq__('赞'):
            blog.forward['praise_count'] = 0
        else:
            blog.forward['praise_count'] = int(strip(praiseCount[0].next_sibling.text))
        print  10 * " ", strip(forwardCount[0].next_sibling.text), strip(repeatCount[0].next_sibling.text), strip(
            praiseCount[0].next_sibling.text)
    selfforwardCount = divhandle.find_all(class_="W_ficon ficon_forward S_ficon")
    selfrepeatCount = divhandle.find_all(class_="W_ficon ficon_repeat S_ficon")
    selfpraiseCount = divhandle.find_all(attrs={"action-type": "fl_like"})
    print  40 * " "
    print  40 * " "
    print  40 * " "
    if strip(selfforwardCount[0].next_sibling.text).__eq__('转发'):
        blog.forward_count = 0
    else:
        blog.forward_count=int(strip(selfforwardCount[0].next_sibling.text))
    if strip(selfrepeatCount[0].next_sibling.text).__eq__('评论'):
        blog.repeat_count = 0
    else:
        blog.repeat_count = int(strip(selfrepeatCount[0].next_sibling.text))
    if strip(selfpraiseCount[0].text).__eq__('赞'):
        blog.praise_count = 0
    else:
        blog.praise_count= int(strip(selfpraiseCount[0].text))
    # print  10 * " ", strip(forwardCount[0].next_sibling.text), strip(repeatCount[0].next_sibling.text), strip(
    #     praiseCount[0].next_sibling.text)
    # print  strip(selfforwardCount[0].next_sibling.text), strip(selfrepeatCount[0].next_sibling.text), strip(
    #     selfpraiseCount[0].text)
    print json.dumps(blog.__dict__)
    dbhelper.insert_one_doc(dbcollection,blog.__dict__)
    print  40 * "*"
    # allHref = soup.find_all(class_="WB_text W_f14",attrs={"node-type": "feed_list_content"})
    # for href in allHref:
    #     print href.text
    # for href in allHref:
    #     print href.string
    # str=http://weibo.com/u/3043662742?refer_flag=1005050005_
    # http://weibo.com/u/3043662742?profile_ftype=1&is_all=1#_0
    #
    # strinfo = re.compile('refer_flag=(.*)')
    # fanUrl = strinfo.sub("profile_ftype=1&is_all=1#_0", basePageUrl)
    # http://weibo.com/p/aj/v6/mblog/mbloglist?
    # ajwvr=6&
    # domain=100505&
    # from=page_100505_profile&
    # wvr=6&
    # mod=data&
    # is_all=1&
    # pagebar=0&
    # pl_name=Pl_Official_MyProfileFeed__24&
    # id=1005053045082420&
    # script_uri=/p/1005053045082420/home&
    # feed_type=0&
    # page=1&
    # pre_page=1&
    # domain_op=100505&
    # __rnd=1465295159377
    #
    #
    # http://weibo.com/p/aj/v6/mblog/mbloglist?
    # ajwvr=6&
    # domain=100505&
    # from=page_100505_profile&
    # wvr=6&
    # mod=data&
    # is_all=1&
    # pagebar=1&
    # pl_name=Pl_Official_MyProfileFeed__24&
    # id=1005053045082420&
    # script_uri=/p/1005053045082420/home&
    # feed_type=0&
    # page=1&
    # pre_page=1&
    # domain_op=100505&
    # __rnd=1465295767517
