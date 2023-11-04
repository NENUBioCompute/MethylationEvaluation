from pymongo import MongoClient


class MongoDBBase:
    def __init__(self, host: str, port: int, username: str, password: str, db_name: str):
        """
        初始化 MongoDB 连接参数
        :param host: mongodb 的 IP 地址
        :param port: mongodb 的 端口
        :param username: mongodb 的用户名
        :param password: mongodb 的密码
        :param db_name: 要连接的数据库名称
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_name = db_name

    def connect(self):
        """
        连接MongoDB
        :return: pymongo.MongoClient对象
        """
        client = MongoClient(host=self.host, port=self.port, username=self.username, password=self.password)
        db = client[self.db_name]
        return client
    # def connect(self):
    #     """
    #     连接MongoDB
    #     :return: pymongo.MongoClient对象
    #     """
    #     # 连接MongoDB数据库
    #     client = MongoClient(host=self.host, port=self.port)
    #     # 选择要连接的数据库
    #     db = client[self.db_name]
    #     # 如果有用户名和密码，则进行认证
    #     if self.username and self.password:
    #         db.authenticate(self.username, self.password)
    #     return client

    def insert_one(self, collection_name: str, data: dict):
        """
        插入一条记录
        :param collection_name: 要插入的集合名
        :param data: 要插入的数据，字典类型
        :return: 插入的记录_id
        """
        client = self.connect()
        collection = client[self.db_name][collection_name]
        result = collection.insert_one(data)
        return result.inserted_id

    def insert_many(self, collection_name: str, data_list: list):
        """
        插入多条记录
        :param collection_name: 要插入的集合名
        :param data_list: 要插入的数据列表，每个元素为一个字典类型
        :return: 插入的记录_id列表
        """
        client = self.connect()
        collection = client[self.db_name][collection_name]
        result = collection.insert_many(data_list)
        return result.inserted_ids

    def update_one(self, collection_name: str, update_filter: dict, update: dict):
        """
        更新一条记录
        :param collection_name: 要更新的集合名
        :param update_filter: 更新条件，字典类型
        :param update: 更新内容，字典类型
        :return: 更新结果，pymongo.UpdateResult对象
        """
        client = self.connect()
        collection = client[self.db_name][collection_name]
        result = collection.update_one(update_filter, {"$set": update})
        return result

    def update_many(self, collection_name: str, filter: dict, update: dict):
        """
        更新多条记录
        :param collection_name: 要更新的集合名
        :param filter: 更新条件，字典类型
        :param update: 更新内容，字典类型
        :return: 更新结果，pymongo.UpdateResult对象
        """
        client = self.connect()
        collection = client[self.db_name][collection_name]
        result = collection.update_many(filter, {"$set": update})
        return result

    def delete_one(self, collection_name: str, filter: dict):
        """
        删除一条记录
        :param collection_name: 要删除的集合名
        :param filter: 删除条件，字典类型
        :return: 删除结果，pymongo.DeleteResult对象
        """
        client = self.connect()
        collection = client[self.db_name][collection_name]
        result = collection.delete_one(filter)
        return result

    def delete_many(self, collection_name: str, filter: dict):
        """
        删除多条记录
        :param collection_name: 要删除的集合名
        :param filter: 删除条件，字典类型
        :return: 删除结果，pymongo.DeleteResult对象
        """
        client = self.connect()
        collection = client[self.db_name][collection_name]
        result = collection.delete_many(filter)
        return result

    def find_one(self, collection_name: str, filter: dict):
        """
        查找一条记录
        :param collection_name: 要查找的集合名
        :param filter: 查找条件，字典类型
        :return: 查找结果，字典类型
        """
        client = self.connect()
        collection = client[self.db_name][collection_name]
        result = collection.find_one(filter)
        return result

    def find(self, collection_name: str, find_filter: dict):
        """
        查找多条记录
        :param collection_name: 要查找的集合名
        :param find_filter: 查找条件，字典类型
        :return: 查找结果，pymongo.Cursor对象
        """
        client = self.connect()
        collection = client[self.db_name][collection_name]
        result = collection.find(find_filter)
        return result
