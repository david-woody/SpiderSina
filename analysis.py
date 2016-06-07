# encoding:utf-8
import re
import PyV8
from bs4 import BeautifulSoup

# 拼接成粉丝列表url
# fansUrl="http://weibo.com/"+uid+"/fans?rightmod=1&wvr=6";
# print  "fansUrl==",fansUrl

# 读取文件获得字符串

f_query1 = open("fans.htm", "r")
html = f_query1.read();
# 获取第一页的粉丝列表
middleware1 = re.findall("pl\.relation\.fans\.index(.*)", html)
middleware2 = re.findall("\"html\":\"(.*)\"}\)", middleware1[0])
resultHtml = middleware2[0].replace("\\r\\n", "").replace("\\n", "").replace("\\", "")
soup = BeautifulSoup(resultHtml, "lxml")
allHref = soup.find_all("a", class_="S_txt1", target="_blank")
member = {}
datas = []
userIds = list()
baseUrl = "http://weibo.com"
for href in allHref:
    userId = re.findall("\/u\/(.*)\?", href.get('href'))[0]
    if userId not in userIds:
        userIds.append(userId)
        member["name"] = href.string
        member["url"] = baseUrl + href.get('href')
        datas.append(member)
pageHref = soup.find_all("a", class_="page")
print pageHref
pages = list()
for page in pageHref:
    pages.append(page.text)
    print page.get("href")
maxPage = int(pages[len(pages) - 2])
# print maxPage
if (maxPage >= 2):
    basePageUrl = str(pageHref[len(pages) - 2].get("href"))
    for pageNum in [2, maxPage]:
        strinfo = re.compile('page=(.*)\#')
        b = strinfo.sub("page=" + str(3) + "#", basePageUrl)
        print b
for pageNum in range(1, maxPage):
    print "dsad"
# /2573805580/fans?pids=Pl_Official_RelationFans__103&cfs=600&relate=fans&t=1&f=1&type=&Pl_Official_RelationFans__103_page=2#Pl_Official_RelationFans__103
# tes1sa = re.findall(r'(?<=\<a\>).*?(?=\<\/a\>)', text[0])
# for tes in tes1sa:
# http://weibo.com/u/3045049884?refer_flag=1005050005_
# <a  target=\"_blank\" title=\"女孩胡小娟\" href=\"\/u\/3045049884?refer_flag=1005050005_\">
# 第一页关注的好友

# 计算其中的页数


# http://weibo.com/p/1005053043662742/follow?pids=Pl_Official_HisRelation__64&relate=fans&page=2#Pl_Official_HisRelation__64
# http://weibo.com/2573805580/fans?cfs=600&relate=fans&t=1&f=1&type=&Pl_Official_RelationFans__103_page=2#Pl_Official_RelationFans__103














# 获取自己的uid
# lst = re.findall("CONFIG\['uid'\]='(.*)'", html_cont)
# uid=lst[0]
