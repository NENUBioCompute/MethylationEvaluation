from Mongo.MongoBase import MongoDBBase


class GetOther:
    def __init__(self):
        self.mongo = MongoDBBase(host='127.0.0.1', port=27017, username='root', password='admin', db_name='dnam_clocks')

    def get_task(self):
        """
        获取上传任务信息
        :return: 上传任务信息
        """
        tasks = []
        # 查找
        result = self.mongo.find('tasks', {})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            tasks.append(item)
        return tasks

    def insert_task(self, task_data):
        """
        新增上传任务信息
        :param task_data: 任务数据
        :return:
        """
        self.mongo.insert_one('tasks', task_data)
        return True

    def get_clocks(self):
        """
        获取时钟信息
        :return: 所有的时钟信息
        """
        clocks = []
        result = self.mongo.find('clocks', {})
        for clock in result:
            clock.pop('_id')
            clocks.append(clock)
        return clocks
