from sina import db_helper

dbhelper = db_helper.DBclient()
dbcollection = dbhelper.get_collection("user")
for item in dbhelper.get_urls():
    print item.__getitem__("url")
dbhelper.removeUrl("http://weibo.com/u/3045049884?profile_ftype=1&is_all=1#_0")