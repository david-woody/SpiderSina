# encoding: utf-8
import json

from sina import db_helper


class HtmlOutputer(object):
    def __init__(self):
        self.dbhelper = db_helper.DBclient()
        self.dbcollection = self.dbhelper.get_collection("sina_blog")
        return

    def saveblogData(self, blogDatas):
        print 30 * "*", "保存博客开始", 30 * "*"
        for blogData in blogDatas:
            self.dbhelper.insert_one_doc(self.dbcollection, blogData.__dict__)
        print 30 * "*", "保存博客结束", 30 * "*"

