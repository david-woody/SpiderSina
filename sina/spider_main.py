# encoding: utf-8

from sina import url_processor, url_manager, html_parser, html_outputer, db_helper


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

    while spider_object.urlManager.has_new_url():
        # try:  # 爬取用户的博客记录
        blog_url = spider_object.urlManager.get_new_url()
        print 70 * " "
        print 70 * " "
        print 30 * "*", "读取博客数据开始", 30 * "*"
        # userIds = re.findall("\/u\/(.*)\?", blog_url)
        # if userIds is None or userIds.__len__() == 0:
        #     userId = re.findall("m\/(.*)\?", blog_url)[0]
        # else:
        #     userId = userIds[0]
        blog_html = spider_object.urlProcessor.getUrlData(blog_url)
        allBlogDatas = spider_object.htmlParser.parserBlog(blog_url, blog_html)
        # 获取博客总数
        blogCount, domianId, pageId, oid = spider_object.htmlParser.parserBlogParams(blog_html)
        if blogCount > 15:
            print "第一页第一次上滑刷新"
            firstPaginationUrl = spider_object.htmlParser.parserFirstPaginationUrl(domianId, pageId, oid, 1, 0)
            firstPaginationData = spider_object.urlProcessor.getUrlData(firstPaginationUrl)
            blogData1 = spider_object.htmlParser.parserPaginationData(oid, firstPaginationData)
            allBlogDatas = allBlogDatas + blogData1
            print ''
        if blogCount > 30:
            print "第一页第二次上滑刷新"
            secondPaginationUrl = spider_object.htmlParser.parserFirstPaginationUrl(domianId, pageId, oid, 1, 1)
            secondPaginationData = spider_object.urlProcessor.getUrlData(secondPaginationUrl)
            blogData2 = spider_object.htmlParser.parserPaginationData(oid, secondPaginationData)
            allBlogDatas = allBlogDatas + blogData2
            urls = spider_object.htmlParser.parserPageUrls(secondPaginationData)
        print "博客总数=", blogCount
        if int(blogCount) < 140:
            print "没有走进"
            count = 1
            for url in urls:
                blog_main_html = spider_object.urlProcessor.getUrlData(url)
                blogData3 = spider_object.htmlParser.parserBlog(blog_url, blog_main_html)
                allBlogDatas = allBlogDatas + blogData3
                count = count + 1
                blogCount, domianId, pageId, oid = spider_object.htmlParser.parserBlogParams(blog_main_html)
                # 读取第一次分页
                print "count 页数=",count
                firstPaginationUrl = spider_object.htmlParser.parserFirstPaginationUrl(domianId, pageId, oid, count, 0)
                firstPaginationData = spider_object.urlProcessor.getUrlData(firstPaginationUrl)
                blogData1 = spider_object.htmlParser.parserPaginationData(oid, firstPaginationData)
                allBlogDatas = allBlogDatas + blogData1
                isPagination = spider_object.htmlParser.parserNextPagination(firstPaginationData)
                if isPagination:
                    # 读取第二次分页
                    secondPaginationUrl = spider_object.htmlParser.parserFirstPaginationUrl(domianId, pageId, oid,
                                                                                            count, 1)
                    secondPaginationData = spider_object.urlProcessor.getUrlData(secondPaginationUrl)
                    blogData2 = spider_object.htmlParser.parserPaginationData(oid, secondPaginationData)
                    allBlogDatas = allBlogDatas + blogData2
        # http://weibo.com/p/aj/v6/mblog/mbloglist?
        # ajwvr=6&domain=100606&is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1
        # &page=1&pagebar=0&pl_name=Pl_Official_MyProfileFeed__25
        # &id=1006062371375560&script_uri=/p/1006062371375560/home&feed_type=0
        # &pre_page=1&domain_op=100606&__rnd=1465957911461
        # 获取分页所需要的数据

        print 30 * "*", "存储博客数据开始", 30 * "*"
        spider_object.htmlOutPuter.saveblogData(allBlogDatas)
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
        # 爬取用户的个人资料网页链接
        personMoreUrl = spider_object.htmlParser.parserPersonMoreUrl(blog_html)
        # 爬取用户的个人资料网页
        personMoreHtml = spider_object.urlProcessor.getUrlData(personMoreUrl)
        # 解析用户的个人资料
        personMoreData = spider_object.htmlParser.parserPersonMoreData(personMoreUrl, personMoreHtml)
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
