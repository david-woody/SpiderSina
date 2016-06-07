# encoding: utf-8
import os
import re
from bs4 import BeautifulSoup

# BASE_DIR = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
# print BASE_DIR
# file_path = os.path.join(BASE_DIR, 'log')
# print file_path
# file=os.path.join(file_path, 'text.txt')
# print file
# BASE_DIR = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
# filePath=str(BASE_DIR)+"/log/text.txt";
# currentPathName=os.getcwd() #当前路径
# file=os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'log\\test.htm')
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
file=os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'log\\test.htm')
# print file
fres = open(file, "r").read()
print fres
middleware1 = re.findall("domid\"\:\"Pl\_Official\_MyProfileFeed(.*)\)\<", fres)
#class="WB_text W_f14" node-type="feed_list_content"

print middleware1[0]
# print middleware1[1]
middleware2 = re.findall("\"html\":\"(.*)\"}", middleware1[0])
print middleware2
resultHtml = middleware2[0].replace("\\r\\n", "").replace("\\n", "").replace("\\", "")
print resultHtml
soup = BeautifulSoup(resultHtml, "lxml")
allHref = soup.find_all(class_="WB_text W_f14",attrs={"node-type": "feed_list_content"})
for href in allHref:
    print href.text
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