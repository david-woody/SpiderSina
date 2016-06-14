# encoding: utf-8
import json

from sina import db_helper


class HtmlOutputer(object):
    def __init__(self):
        self.dbhelper = db_helper.DBclient()
        self.dbcollection = self.dbhelper.get_collection("blog")
        return

    def saveblogData(self, blogDatas):
        for blogData in blogDatas:
            self.dbhelper.insert_one_doc(self.dbcollection, blogData.__dict__)

    def saveUserInfo(self, userInfo):
        self.dbhelper.insert_multi_docs('user', userInfo)

    def saveUserDetailInfo(self, userDetailInfo):
        self.dbhelper.insert_multi_docs('userdetail', userDetailInfo)


    def saveUserDetailInfo(self, userDetailInfo):
        self.dbhelper.insert_one_doc(self.dbhelper.get_collection("userdetail"), userDetailInfo)
