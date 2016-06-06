# encoding:utf-8
import re
import PyV8
from bs4 import BeautifulSoup

# 拼接成粉丝列表url
# fansUrl="http://weibo.com/"+uid+"/fans?rightmod=1&wvr=6";
# print  "fansUrl==",fansUrl

# 读取文件获得字符串
f_query1 = open("fans.htm", "r")
html_cont = f_query1.read();
lst = re.findall("pl\.relation\.fans\.index(.*)", html_cont)
text = re.findall("\"html\":\"(.*)\"}\)", lst[0])
print text[0]
rest = text[0].replace("\\r\\n", "").replace("\\n", "").replace("\\", "")
print rest
soup = BeautifulSoup(rest, "lxml")
baseUrl = "http://weibo.com"
# tes1sa = re.findall(r'(?<=\<a\>).*?(?=\<\/a\>)', text[0])
# for tes in tes1sa:
# http://weibo.com/u/3045049884?refer_flag=1005050005_
# <a  target=\"_blank\" title=\"女孩胡小娟\" href=\"\/u\/3045049884?refer_flag=1005050005_\">

allHref = soup.find_all("a", class_="S_txt1", target="_blank")
member = {}
datas = []
#第一页关注的好友
for href in allHref:
    member["name"] = href.string
    member["url"] = href.get('href')
    datas.append(member)
print datas
# 计算其中的页数
pageHref = soup.find_all("a", class_="page")
pages = list()
for page in pageHref:
    pages.append(page.text)
print int(pages[len(pages)-2])














# 获取自己的uid
# lst = re.findall("CONFIG\['uid'\]='(.*)'", html_cont)
# uid=lst[0]
