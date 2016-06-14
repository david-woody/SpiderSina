# encoding: utf-8
import os

import re

from sina import url_processor, url_manager, html_parser, html_outputer, user_recorder, db_helper


class SpiderMain(object):
    def __init__(self):
        self.urlProcessor = url_processor.UrlProcesser()
        self.urlManager = url_manager.UrlManager()
        self.htmlParser = html_parser.HtmlParser()
        self.htmlOutPuter = html_outputer.HtmlOutputer()
        self.dbhelper = db_helper.DBclient()
        return


if __name__ == "__main__":
    spider_object = SpiderMain()
    if spider_object.urlProcessor.login("18051352830", "lshdxw0801") == False:
        print  u"登陆失败!"
        exit()
    print u"登录成功!"
    # 获取自己的博客首页
    myHomepage = spider_object.urlProcessor.getUrlData(spider_object.urlManager.BASEURL)
    # 解析出自己的粉丝URL
    fansUrl = spider_object.htmlParser.parserFansUrl(myHomepage)
    # 获得自己的粉丝页面
    fansHtml = spider_object.urlProcessor.getUrlData(fansUrl)
    # 解析出第一页的粉丝数据,粉丝页面基础url和粉丝页数
    fansData, fansUrls, pageCount, urls = spider_object.htmlParser.parserFansBase(fansHtml)
    if fansData.__len__() != 0:
        # 保存粉丝数据到数据库
        print 30 * "*", "存储粉丝数据开始", 30 * "*"
        spider_object.htmlOutPuter.saveUserInfo(fansData)
        print 30 * "*", "存储粉丝数据结束", 30 * "*"
    # 保存粉丝数据
    spider_object.urlManager.add_new_urls(urls)
    if pageCount >= 2:
        # 分别下载所有粉丝界面
        htmls = spider_object.urlProcessor.getUrlsDatas(fansUrls)
        datas = spider_object.htmlParser.parserFans(htmls)
        if datas is not None:
            print 30 * "*", "存储粉丝数据开始", 30 * "*"
            spider_object.htmlOutPuter.saveUserInfo(datas)
            print 30 * "*", "存储粉丝数据结束", 30 * "*"
    # try:
    while spider_object.urlManager.has_new_url():
        # 爬取用户的博客记录
        blog_url = spider_object.urlManager.get_new_url()
        print 70 * " "
        print 70 * " "
        print 30 * "*", "读取博客数据开始", 30 * "*"
        blog_html = spider_object.urlProcessor.getUrlData(blog_url)
        userIds = re.findall("\/u\/(.*)\?", blog_url)
        if userIds is None or userIds.__len__() == 0:
            userId = re.findall("m\/(.*)\?", blog_url)[0]
        else:
            userId = userIds[0]
        print userId
        # file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)),
        #                     'tlogs\\' + userId + '_log.html')
        # fres = open(file, "w").write(blog_html)
        blogDatas = spider_object.htmlParser.parserBlog(blog_url, blog_html)
        print 30 * "*", "存储博客数据开始", 30 * "*"
        spider_object.htmlOutPuter.saveblogData(blogDatas)
        # 删除url
        spider_object.dbhelper.removeUrl(blog_url)
        print 30 * "*", "存储博客数据结束", 30 * "*"
        # 爬取用户的粉丝数并加入爬取链接
        othterFansUrl = spider_object.htmlParser.parserFanUrl(blog_html)
        # 进入用户粉丝页面，获得自己的粉丝页面
        print 30 * "*", "读取粉丝数据开始", 30 * "*"
        otherFansHtml = spider_object.urlProcessor.getUrlData(othterFansUrl)
        # 解析出第一页的粉丝数据,粉丝页面基础url和粉丝页数
        fansData, fansUrls, pageCount, urls = spider_object.htmlParser.parserOtherFansBase(otherFansHtml)
        # 保存粉丝数据
        spider_object.urlManager.add_new_urls(urls)
        if pageCount >= 2:
            # 分别下载所有粉丝界面
            htmls = spider_object.urlProcessor.getUrlsDatas(fansUrls)
            print 30 * "*", "解析粉丝数据开始", 30 * "*"
            datas = spider_object.htmlParser.parserOtherFans(htmls)
            print 30 * "*", "解析粉丝数据结束", 30 * "*"
            if datas is not None:
                print 30 * "*", "存储粉丝数据开始", 30 * "*"
                spider_object.htmlOutPuter.saveUserInfo(datas)
                print 30 * "*", "存储粉丝数据结束", 30 * "*"
        print 30 * "*", "读取粉丝数据结束", 30 * "*"
        print 30 * "*", "解析用户数据开始", 30 * "*"
        # # 爬取用户的粉丝数并加入爬取链接
        personMoreUrl = spider_object.htmlParser.parserPersonMoreUrl(blog_html)
        # # 进入用户粉丝页面，获得自己的粉丝页面
        personMoreHtml = spider_object.urlProcessor.getUrlData(personMoreUrl)
        # file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)),
        #                     'tlogs\\personnalMore_log.html')
        # fres = open(file, "w").write(personMoreHtml)
        # # 进入用户粉丝页面，获得自己的粉丝页面
        personMoreData = spider_object.htmlParser.parserPersonMoreData(personMoreUrl,personMoreHtml)
        print 30 * "*", "存储用户数据开始", 30 * "*"
        spider_object.htmlOutPuter.saveUserDetailInfo(personMoreData)
        print 30 * "*", "存储用户数据结束", 30 * "*"
        print 30 * "*", "解析用户数据结束", 30 * "*"
        print 30 * "*", "读取博客数据结束", 30 * "*"
        print 70 * " "
        print 70 * " "
        print 70 * " "
        # except Exception, e:
        #     print e
