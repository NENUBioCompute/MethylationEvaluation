import pymongo
from Mongo.MongoBase import MongoDBBase

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['dnam_clocks']
col = mydb['users']


class User:
    def __init__(self):
        self.mongo = MongoDBBase(host='127.0.0.1', port=27017, username='root', password='admin', db_name='dnam_clocks')

    # 注册
    def add_user(self, register_info: dict):
        """
        :param register_info: 注册信息
        :return:
        """
        res = self.mongo.insert_one('users', register_info)
        if res:
            return True
        else:
            return False

    # 登录验证
    def get_user(self, email: str, password: str):
        """
        :param email: 登录邮箱
        :param password: 登录密码
        :return: 登录信息正误
        """
        query = {'email': email}
        log_user = self.mongo.find_one('users', query)
        if log_user is None or log_user['status'] is False:
            return False
        userInfo = {
            'name': log_user['firstName'] + ' ' + log_user['lastName'],
            'email': log_user['email']
        }
        if password != log_user['password']:
            return False
        return userInfo

    # 修改密码
    def update_psw(self, email: str, new_psw: str):
        """
        :param email: 登录邮箱
        :param new_psw: 新密码
        :return: 修改成功
        """
        query = {'email': email}
        # new = {'$set': {'password': new_psw}}
        new = {'password': new_psw}
        print(new)
        self.mongo.update_one('users', query, new)
        return True

    # 检查邮箱是否存在
    def check(self, email: str):
        """
        :param email: 邮箱
        :return:
        """
        query = {'Email': email}
        user_check = self.mongo.find_one('users', query)
        if user_check is None:
            return False
        else:
            return True


if __name__ == '__main__':
    user = User()
    print(user.get_user('zongxizeng@gmail.com', '123456'))
