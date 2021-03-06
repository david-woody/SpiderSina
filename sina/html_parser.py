# encoding: utf-8
import json
import os
import re
import time
import urllib
from string import strip

from bs4 import BeautifulSoup

from sina import db_helper
from sina.dao import blog_dao

paginationData = {
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


class HtmlParser(object):
    def __init__(self):
        self.userRecoder = list()
        self.dbhelper = db_helper.DBclient()
        self.base_url = "http://weibo.com/"
        for item in self.dbhelper.get_user_id():
            self.userRecoder.append(item.__getitem__("id"))
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
        datas = []
        fanUrls = []
        urls = []
        baseUrl = "http://weibo.com"
        for href in allHref:
            userIds = re.findall("\/u\/(.*)\?", href.get('href'))
            if userIds is None or userIds.__len__() == 0:
                userId = re.findall("\/(.*)\?", href.get('href'))[0]
            else:
                userId = userIds[0]
            if userId not in self.userRecoder:
                # 过滤掉新手指南
                if str(href.string).__eq__("新手指南"):
                    continue
                self.userRecoder.append(userId)
                member = {}
                member["name"] = href.string
                member["id"] = userId
                url1 = baseUrl + href.get('href')
                strinfo = re.compile('refer_flag=(.*)')
                member["url"] = strinfo.sub("profile_ftype=1&is_all=1#_0", url1)
                urls.append(member["url"])
                datas.append(member)
            else:
                print "用户已检索!"
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
        return datas, fanUrls, maxPage, urls

    def parserFans(self, htmls):
        dataSet = []
        for html in htmls:
            middleware1 = re.findall("pl\.relation\.fans\.index(.*)", html)
            middleware2 = re.findall("\"html\":\"(.*)\"}\)", middleware1[0])
            resultHtml = middleware2[0].replace("\\r\\n", "").replace("\\n", "").replace("\\", "")
            soup = BeautifulSoup(resultHtml, "lxml")
            allHref = soup.find_all("a", class_="S_txt1", target="_blank")
            member = {}
            datas = []
            fanUrls = []
            baseUrl = "http://weibo.com"
            for href in allHref:
                userIds = re.findall("\/u\/(.*)\?", href.get('href'))
                if userIds is None or userIds.__len__() == 0:
                    userId = re.findall("\/(.*)\?", href.get('href'))[0]
                else:
                    userId = userIds[0]
                if userId not in self.userRecoder:
                    # 过滤掉新手指南
                    if str(href.string).__eq__("新手指南"):
                        continue
                    self.userRecoder.append(userId)
                    member["name"] = href.string
                    url1 = baseUrl + href.get('href')
                    member["id"] = userId
                    strinfo = re.compile('refer_flag=(.*)')
                    member["url"] = strinfo.sub("profile_ftype=1&is_all=1#_0", url1)
                    datas.append(member)
                else:
                    print "用户已检索!"
            if datas is None or len(datas) == 0:
                print "反垃圾关注规则已过滤"
            else:
                dataSet.append(datas)
        if dataSet is None or len(dataSet) == 0:
            return
        else:
            return dataSet

    def parserBlog(self, blog_url, blog_html):
        userIds = re.findall("\/u\/(.*)\?", blog_url)
        if userIds is None or userIds.__len__() == 0:
            userId = re.findall("\/(.*)\?", blog_url)
        else:
            userId = userIds[0]
        middleware1 = re.findall("domid\"\:\"Pl\_Official\_MyProfileFeed(.*)\)\<", blog_html)
        middleware2 = re.findall("\"html\":\"(.*)\"}", middleware1[0])
        resultHtml = middleware2[0].replace("\\r\\n", "").replace("\\n", "").replace("\\", "")
        soup = BeautifulSoup(resultHtml, "html.parser")
        divs = soup.find_all(class_="WB_cardwrap WB_feed_type S_bg2 ")
        # 15条blog记录
        blogs = []
        count = 1;
        for div2 in divs:
            print  "Analysis 第:", count, "条数据"
            blog = blog_dao.BlogDao()
            blog.user_id = userId;
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
            print blog.__dict__
            blogs.append(blog)
            count = count + 1
        return blogs

    def parserFanUrl(self, blog_html):
        middleware1 = re.findall("domid\"\:\"Pl\_Core\_T8Cus(.*)\)\<", blog_html)
        # print middleware1
        middleware2 = re.findall("\"html\":\"(.*)\"}", middleware1[0])
        resultHtml = middleware2[0].replace("\\r\\n", "").replace("\\t", "").replace("\\", "")
        # print resultHtml
        soup = BeautifulSoup(resultHtml, "html.parser")
        url = soup.find_all("span", text="粉丝")[0].find_parent().get("href")
        return url

    def parserOtherFansBase(self, fansHtml):
        middleware1 = re.findall("domid\"\:\"Pl\_Official\_HisRelation\_\_(.*)", fansHtml)
        middleware2 = re.findall("\"html\":\"(.*)\"}\)", middleware1[0])
        resultHtml = middleware2[0].replace("\\r\\n", "").replace("\\t", "").replace("\\", "")
        soup = BeautifulSoup(resultHtml, "lxml")
        allHref = soup.find_all("a", class_="S_txt1", target="_blank")
        member = {}
        datas = []
        fanUrls = []
        urls = []
        baseUrl = "http://weibo.com"
        for href in allHref:
            userIds = re.findall("\/u\/(.*)\?", href.get('href'))
            if userIds is None or userIds.__len__() == 0:
                userId = re.findall("\/(.*)\?", href.get('href'))[0]
            else:
                userId = userIds[0]
            if userId not in self.userRecoder:
                # 过滤掉新手指南
                if str(href.string).__eq__("新手指南"):
                    continue
                self.userRecoder.append(userId)
                member["name"] = href.string
                url1 = baseUrl + href.get('href')
                strinfo = re.compile('refer_flag=(.*)')
                member["id"] = userId
                member["url"] = strinfo.sub("profile_ftype=1&is_all=1#_0", url1)
                urls.append(member["url"])
                datas.append(member)
            else:
                print "用户已检索!"
        pageHref = soup.find_all("a", class_="page")
        pages = list()
        for page in pageHref:
            pages.append(page.text)
        if pages.__len__() == 0:
            return datas, fanUrls, 0, urls
        maxPage = int(pages[len(pages) - 2])
        if (maxPage >= 2):
            basePageUrl = baseUrl + str(pageHref[len(pages) - 2].get("href"))
            if maxPage > 10:
                maxPage = 10
            for pageNum in range(2, maxPage + 1):
                strinfo = re.compile('page=(.*)\#')
                fanUrl = strinfo.sub("page=" + str(pageNum) + "#", basePageUrl)
                fanUrls.append(fanUrl)
        else:
            basePageUrl = ""
        return datas, fanUrls, maxPage, urls

    def parserOtherFans(self, htmls):
        dataSet = []
        count = 1;
        for html in htmls:
            print "Analysis Url", count, "Data........."
            middleware1 = re.findall("domid\"\:\"Pl\_Official\_HisRelation\_\_(.*)", html)
            if middleware1.__len__() == 0:
                print "反垃圾关注规则已过滤"
                continue
            middleware2 = re.findall("\"html\":\"(.*)\"}\)", middleware1[0])
            resultHtml = middleware2[0].replace("\\r\\n", "").replace("\\t", "").replace("\\", "")
            soup = BeautifulSoup(resultHtml, "lxml")
            allHref = soup.find_all("a", class_="S_txt1", target="_blank")
            fanUrls = []
            baseUrl = "http://weibo.com"
            for href in allHref:
                userIds = re.findall("\/u\/(.*)\?", href.get('href'))
                if userIds is None or userIds.__len__() == 0:
                    userId = re.findall("\/(.*)\?", href.get('href'))[0]
                else:
                    userId = userIds[0]
                if userId not in self.userRecoder:
                    # 过滤掉新手指南
                    if str(href.string).__eq__("新手指南"):
                        continue
                    self.userRecoder.append(userId)
                    member = {}
                    member["name"] = href.string
                    url1 = baseUrl + href.get('href')
                    member["id"] = userId
                    strinfo = re.compile('refer_flag=(.*)')
                    member["url"] = strinfo.sub("profile_ftype=1&is_all=1#_0", url1)
                    dataSet.append(member)
                else:
                    print "用户已检索!"
            if dataSet is None or len(dataSet) == 0:
                print "反垃圾关注规则已过滤"
            count = count + 1
        if dataSet is None or len(dataSet) == 0:
            return
        else:
            return dataSet

    def parserPersonMoreUrl(self, blog_html):
        try:
            middleware1 = re.findall("domid\"\:\"Pl\_Core\_UserInfo(.*)\)\<", blog_html)
            middleware2 = re.findall("\"html\":\"(.*)\"}", middleware1[0])
            resultHtml = middleware2[0].replace("\\r\\n", "").replace("\\t", "").replace("\\", "")
            soup = BeautifulSoup(resultHtml, "html.parser")
            url = soup.find_all("a", class_="WB_cardmore S_txt1 S_line1 clearfix")[0].get("href")
            htmlUrl = "http://weibo.com" + url
        except Exception, e:
            file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)),
                                'bugs\\Error_' + int(time.time()) + '_log.html')
            fres = open(file, "w")
            fres.write(blog_html)
            fres.close()
            print "解析用户URL失败,请查看log日志"
        return htmlUrl

    def parserPersonMoreData(self, personMoreUrl, personMoreHtml):
        try:
            middleware1 = re.findall("domid\"\:\"Pl\_Official\_PersonalInfo(.*)\)\<", personMoreHtml)
            middleware2 = re.findall("\"html\":\"(.*)\"}", middleware1[0])
            resultHtml = middleware2[0].replace("\\r\\n", "").replace("\\t", "").replace("\\", "")
            soup = BeautifulSoup(resultHtml, "html.parser")
            userDetail = {}
            nickResult = soup.find_all("span", text="昵称：")
            if len(nickResult) != 0:
                userDetail["nickname"] = nickResult[0].next_sibling.text
            sexResult = soup.find_all("span", text="性别：")
            if len(sexResult) != 0:
                userDetail["sex"] = sexResult[0].next_sibling.text
            birthResult = soup.find_all("span", text="生日：")
            if len(birthResult) != 0:
                userDetail["birthday"] = birthResult[0].next_sibling.text
            infoResult = soup.find_all("span", text="简介：")
            if len(infoResult) != 0:
                userDetail["info"] = infoResult[0].next_sibling.text
            registResult = soup.find_all("span", text="注册时间：")
            if len(registResult) != 0:
                userDetail["registime"] = registResult[0].next_sibling.text
        except Exception, e:
            file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)),
                                'bugs\\Error_' + int(time.time()) + '_log.html')
            fres = open(file, "w")
            fres.write(personMoreHtml)
            fres.close()
            print "解析用户URL失败,请查看log日志"
        return userDetail

    #

    def parserBlogParams(self, blog_html):
        middleware1 = re.findall("domid\"\:\"Pl\_Core\_T8Cus(.*)\)\<", blog_html)
        # print middleware1
        middleware2 = re.findall("\"html\":\"(.*)\"}", middleware1[0])
        resultHtml = middleware2[0].replace("\\r\\n", "").replace("\\t", "").replace("\\", "")
        # print resultHtml
        soup = BeautifulSoup(resultHtml, "html.parser")
        count = soup.find_all("span", text="微博")[0].previous_element
        domians = re.findall("domain\'\]\=\'(.*)\'\;", blog_html)
        if len(domians) == 0:
            exit()
        domianId = domians[0]
        print domianId
        pageIds = re.findall("page\_id\'\]\=\'(.*)\'\;", blog_html)
        if len(pageIds) == 0:
            exit()
        pageId = pageIds[0]
        print pageId
        oids = re.findall("oid\'\]\=\'(.*)\'\;", blog_html)
        if len(oids) == 0:
            exit()
        oid = oids[0]
        print oid
        return count, domianId, pageId, oid

    def parserFirstPaginationUrl(self, domianId, pageId, oid,page, pageBar):
        global paginationData
        paginationData["domain"] = domianId
        paginationData["domain_op"] = domianId
        paginationData["id"] = pageId
        script_uri = "/u/" + oid
        paginationData["script_uri"] = script_uri
        paginationData["pagebar"] = pageBar
        paginationData["page"] = page
        paginationData["pre_page"] = page
        timeers = "%d" % (time.time() * 1000)
        paginationData["__rnd"] = timeers
        urlData = urllib.urlencode(paginationData)
        fullUrl = "http://weibo.com/p/aj/v6/mblog/mbloglist?" + urlData
        print fullUrl
        return fullUrl

    def parserPaginationData(self, oid, firstPaginationData):
        s = json.loads(firstPaginationData)
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
            print "分页数据:",blog.__dict__
            count = count + 1
        return blogs

    def parserPageUrls(self, secondPaginationData):
        s = json.loads(secondPaginationData)
        soup = BeautifulSoup(s['data'], "html.parser")
        divs = soup.find(class_="WB_cardwrap S_bg2")
        urls = []
        if divs != None:
            pageUrlList = divs.find('ul').find_all("a")
            for url in pageUrlList:
                url = "http://weibo.com" + url.get("href")
                newurl = url.replace("pids=Pl_Official_MyProfileFeed__25&", "")
                if newurl.__contains__("&page=1") != True:
                    urls.append(newurl)
        else:
            print "没有其余博客"
        urls.reverse()
        for url in urls:
            print url
        return urls

    def parserNextPagination(self, resultData):
         s = json.loads(resultData)
         soup = BeautifulSoup(s['data'], "html.parser")
         divs = soup.find(class_="WB_cardwrap S_bg2")
         if divs!=None:
             return True
         else:
             return False
