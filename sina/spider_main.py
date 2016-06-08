# encoding: utf-8
import os

import re

from sina import url_processor, url_manager, html_parser, html_outputer, user_recorder


class SpiderMain(object):
    def __init__(self):
        self.urlProcessor = url_processor.UrlProcesser()
        self.urlManager = url_manager.UrlManager()
        self.htmlParser = html_parser.HtmlParser()
        self.htmlOutPuter = html_outputer.HtmlOutputer()
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
    # 保存粉丝数据
    spider_object.urlManager.add_new_urls(urls)
    if pageCount >= 2:
        # 分别下载所有粉丝界面
        htmls = spider_object.urlProcessor.getUrlsDatas(fansUrls)
        datas = spider_object.htmlParser.parserFans(htmls)
        if datas is not None:
            print datas
    # try:
    while spider_object.urlManager.has_new_url():
        # 爬取用户的博客记录
        blog_url = spider_object.urlManager.get_new_url()
        print 30 * "*", "读取博客数据开始", 30 * "*"
        blog_html = spider_object.urlProcessor.getUrlData(blog_url)
        userIds = re.findall("\/u\/(.*)\?", blog_url)
        if userIds is None or userIds.__len__() == 0:
            userId = re.findall("\/(.*)\?", blog_url)[0]
        else:
            userId = userIds[0]
        file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)),
                            'tlogs\\' + userId + '_log.html')
        fres = open(file, "w").write(blog_html)
        blogDatas = spider_object.htmlParser.parserBlog(blog_url, blog_html)
        spider_object.htmlOutPuter.saveblogData(blogDatas)
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
            datas = spider_object.htmlParser.parserOhterFans(htmls)
            if datas is not None:
                print datas
        print 30 * "*", "读取粉丝数据结束", 30 * "*"
        print 30 * "*", "读取博客数据结束", 30 * "*"
        # except Exception, e:
        #     print e
