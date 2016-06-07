# encoding: utf-8
import os

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
    fansData, fansUrls, pageCount,urls = spider_object.htmlParser.parserFansBase(fansHtml)
    print fansData
    print fansUrls
    print pageCount
    # 保存粉丝数据
    spider_object.urlManager.add_new_urls(urls)
    # 分别下载所有粉丝界面
    htmls = spider_object.urlProcessor.getUrlsDatas(fansUrls)
    datas = spider_object.htmlParser.parserFans(htmls)
    print datas
    if datas is not None:
        print datas
    # while spider_object.urlManager.has_new_url():
    new_url = spider_object.urlManager.get_new_url()
    print new_url
    asda=spider_object.urlProcessor.getUrlData(new_url)
    print asda
    f_query1 = open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'log\\test.htm'), "w")
    f_query1.write(asda)
    f_query1.close()
