# encoding: utf-8
import re
from bs4 import BeautifulSoup


class HtmlParser(object):
    def __init__(self):
        self.userRecoder = list()
        return

    def parserFansUrl(self, myHomepage):
        # 获取自己的uid
        lst = re.findall("CONFIG\['uid'\]='(.*)'", myHomepage)
        uid = lst[0]
        # 拼接成粉丝列表url  http://weibo.com/2573805580/fans?rightmod=1&wvr=6
        fansUrl = "http://weibo.com/" + uid + "/fans?rightmod=1&wvr=6";
        return fansUrl

    def parserFansBase(self, fansHtml):
        middleware1 = re.findall("pl\.relation\.fans\.index(.*)", fansHtml)
        middleware2 = re.findall("\"html\":\"(.*)\"}\)", middleware1[0])
        resultHtml = middleware2[0].replace("\\r\\n", "").replace("\\n", "").replace("\\", "")
        soup = BeautifulSoup(resultHtml, "lxml")
        allHref = soup.find_all("a", class_="S_txt1", target="_blank")
        member = {}
        datas = []
        fanUrls = []
        urls = []
        baseUrl = "http://weibo.com"
        for href in allHref:
            userId = re.findall("\/u\/(.*)\?", href.get('href'))[0]
            if userId not in self.userRecoder:
                self.userRecoder.append(userId)
                member["name"] = href.string
                url1 = baseUrl + href.get('href')
                strinfo = re.compile('refer_flag=(.*)')
                member["url"] = strinfo.sub("profile_ftype=1&is_all=1#_0", url1)
                urls.append(member["url"])
                datas.append(member)
        pageHref = soup.find_all("a", class_="page")
        pages = list()
        for page in pageHref:
            pages.append(page.text)
        maxPage = int(pages[len(pages) - 2])
        if (maxPage >= 2):
            basePageUrl = baseUrl + str(pageHref[len(pages) - 2].get("href"))
            for pageNum in range(2, maxPage + 1):
                strinfo = re.compile('page=(.*)\#')
                fanUrl = strinfo.sub("page=" + str(pageNum) + "#", basePageUrl)
                fanUrls.append(fanUrl)
        else:
            basePageUrl = ""

        return datas, fanUrls, maxPage,urls

    def parserFans(self, htmls):
        member = {}
        dataSet = []
        for html in htmls:
            middleware1 = re.findall("pl\.relation\.fans\.index(.*)", html)
            print middleware1
            middleware2 = re.findall("\"html\":\"(.*)\"}\)", middleware1[0])
            resultHtml = middleware2[0].replace("\\r\\n", "").replace("\\n", "").replace("\\", "")
            soup = BeautifulSoup(resultHtml, "lxml")
            allHref = soup.find_all("a", class_="S_txt1", target="_blank")
            member = {}
            datas = []
            fanUrls = []
            baseUrl = "http://weibo.com"
            for href in allHref:
                member["name"] = href.string
                url1= baseUrl + href.get('href')
                strinfo = re.compile('refer_flag=(.*)')
                member["url"] = strinfo.sub("profile_ftype=1&is_all=1#_0", url1)
                datas.append(member)
            if datas is None or len(datas) == 0:
                print "反垃圾关注规则已过滤"
            else:
                dataSet.append(datas)
        if dataSet is None or len(dataSet) == 0:
            return
        else:
            return dataSet
