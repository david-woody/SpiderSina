# encoding: utf-8
import re
from string import strip

from bs4 import BeautifulSoup

from sina import db_helper
from sina.dao import blog_dao


class HtmlParser(object):
    def __init__(self):
        self.userRecoder = list()
        self.dbhelper = db_helper.DBclient()
        self.base_url="http://weibo.com/"
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
                #淘宝推广会有两个赞标签
                if len(praiseCount)==1:
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
            # print  10 * " ", strip(forwardCount[0].next_sibling.text), strip(repeatCount[0].next_sibling.text), strip(
            #     praiseCount[0].next_sibling.text)
            # print  strip(selfforwardCount[0].next_sibling.text), strip(selfrepeatCount[0].next_sibling.text), strip(
            #     selfpraiseCount[0].text)
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
        middleware1 = re.findall("domid\"\:\"Pl\_Core\_UserInfo(.*)\)\<", blog_html)
        print middleware1
        middleware2 = re.findall("\"html\":\"(.*)\"}", middleware1[0])
        resultHtml = middleware2[0].replace("\\r\\n", "").replace("\\t", "").replace("\\", "")
        print resultHtml
        soup = BeautifulSoup(resultHtml, "html.parser")
        url = soup.find_all("a", class_="WB_cardmore S_txt1 S_line1 clearfix")[0].get("href")
        htmlUrl = "http://weibo.com/" + url
        return htmlUrl


    def parserPersonMoreData(self, personMoreHtml):
        return
