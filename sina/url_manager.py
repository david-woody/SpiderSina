# encoding: utf-8
from sina import db_helper


class UrlManager(object):
    def __init__(self):
        self.BASEURL = "http://weibo.com";
        self.newfansUrl = set()
        self.oldfansUrl = set()
        self.userId = set()
        self.dbhelper = db_helper.DBclient()
        self.collections=self.dbhelper.get_collection("url")
        for item in self.dbhelper.get_urls():
            self.newfansUrl.add(item.__getitem__("url"))
        return

    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.newfansUrl and url not in self.oldfansUrl:
            self.newfansUrl.add(url)

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)
            urlDao = {}
            urlDao["url"] = url
            self.dbhelper.insert_one_doc(self.collections, urlDao)

    def has_new_url(self):
        return len(self.newfansUrl) != 0

    def get_new_url(self):
        new_url = self.newfansUrl.pop()
        self.oldfansUrl.add(new_url)
        return new_url
