import pymongo


class DBclient(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        self.db = self.client['woody'];
        return

    # def get_db(self):
    #     client = pymongo.MongoClient(host="10.244.25.180", port=27017)
    #     db = client['example']
    #     return db

    def get_collection(self, name):
        coll = self.db[name]
        return coll

    def create_collection(self, name):
        coll = self.db.create_collection(name)
        return coll

    def insert_one_doc(self, coll,information):
        information_id = coll.save(information)
        print information_id

    def insert_multi_docs(db):
        coll = db['informations']
        information = [{"name": "xiaoming", "age": "25"}, {"name": "xiaoqiang", "age": "24"}]
        information_id = coll.insert(information)
        print information_id

    def get_one_doc(db):
        coll = db['informations']
        print coll.find_one()
        print coll.find_one({"name": "quyang"})
        print coll.find_one({"name": "none"})

    def get_one_by_id(db):
        coll = db['informations']
        obj = coll.find_one()
        obj_id = obj["_id"]

        print coll.find_one({"_id": obj_id})
        print coll.find_one({"_id": str(obj_id)})
        from bson.objectid import ObjectId

        print coll.find_one({"_id": ObjectId(str(obj_id))})

    def get_many_docs(db):
        coll = db['informations']
        for item in coll.find().sort("age", pymongo.DESCENDING):
            print item

        count = coll.count()

        count = coll.find({"name": "quyang"}).count()
        print "quyang: %s" % count

    def clear_all_datas(db):
        db["informations"].remove()

        # if __name__ == '__main__':
        #     db = get_db()
        #     my_collection = get_collection(db)
        #     post = {"author": "Mike", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"],
        #             "date": datetime.datetime.utcnow()}
        #     my_collection.insert(post)
        #     insert_one_doc(db)
        #     print my_collection.find_one({"x": "10"})
        #     for iii in my_collection.find():
        #         print iii
        #     print my_collection.count()
        #     my_collection.update({"author": "Mike"},
        #                          {"author": "quyang", "text": "My first blog post!",
        #                           "tags": ["mongodb", "python", "pymongo"],
        #                           "date": datetime.datetime.utcnow()})
        #     for jjj in my_collection.find():
        #         print jjj
        #     get_one_doc(db)
        #     get_one_by_id(db)
        #     get_many_docs(db)
        # clear_all_datas(db)