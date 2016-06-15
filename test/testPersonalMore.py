# encoding: utf-8
import os
import re
from string import strip
import json
from bs4 import BeautifulSoup

file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'bugs/personnalMore_log.html')
fres = open(file, "r").read()
print fres
middleware1 = re.findall("domid\"\:\"Pl\_Official\_PersonalInfo(.*)\)\<", fres)
print middleware1
middleware2 = re.findall("\"html\":\"(.*)\"}", middleware1[0])
resultHtml = middleware2[0].replace("\\r\\n", "").replace("\\t", "").replace("\\", "")
print resultHtml
soup=BeautifulSoup(resultHtml,"html.parser")

result=soup.find_all("span",text="昵称：")
print result[0].next_sibling.text
result=soup.find_all("span",text="所在地：")
print result[0].next_sibling.text
result=soup.find_all("span",text="性别：")
print result[0].next_sibling.text
result=soup.find_all("span",text="生日：")
print result[0].next_sibling.text
result=soup.find_all("span",text="简介：")
print result[0].next_sibling.text
result=soup.find_all("span",text="注册时间：")
print result[0].next_sibling.text

# url=soup.find_all("a",class_="WB_cardmore S_txt1 S_line1 clearfix")[0].get("href")
# html="http://weibo.com/"+url
# print html