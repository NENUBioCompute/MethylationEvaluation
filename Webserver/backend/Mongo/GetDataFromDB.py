from Mongo.MongoBase import MongoDBBase


class GetData:
    def __init__(self):
        self.mongo = MongoDBBase(host='127.0.0.1', port=27017, username='', password='', db_name='dnam_clocks')

    def get_dataset_data(self):
        """
        获取数据集结果数据
        :return: 数据集结果数据
        """
        datasets = []
        # 查找
        result = self.mongo.find('datasets', {})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            datasets.append(item)
        return datasets

    def get_disease_data(self):
        """
        获取疾病结果数据
        :return: 疾病结果数据
        """
        disease = []
        # 查找
        result = self.mongo.find('diseases', {})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            item['Diseases'] = item['Disease'][0]
            disease.append(item)
        return disease

    def get_race_data(self):
        """
        获取种族结果数据
        :return: 种族结果数据
        """
        race = []
        # 查找
        result = self.mongo.find('races', {})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            item['Races'] = item['Race'][0]
            race.append(item)
        return race

    def get_tissue_data(self):
        """
        获取组织结果数据
        :return: 组织结果数据
        """
        tissues = []
        # 查找
        result = self.mongo.find('tissues', {})
        for index, item in enumerate(result):
            item.pop('_id')
            item['id'] = index + 1
            item['Tissues'] = item['Tissue'][0]
            tissues.append(item)
        return tissues


if __name__ == '__main__':
    getd = GetData()
    a = getd.get_tissue_data()[-2]
    print(set(a['Dataset']))
    # for i in getd.get_tissue_data():
    #     print(i)
    b = ['GSE32148', 'GSE32149', 'GSE40005', 'GSE40279', 'GSE41169', 'GSE42861', 'GSE43414',
            'GSE50660', 'GSE53128', 'GSE53740', 'GSE55763', 'GSE57285', 'GSE59509', 'GSE59685',
         'GSE60132', 'GSE61496', 'GSE65638', 'GSE67444', 'GSE67705', 'GSE72773', 'GSE72775',
         'GSE72777', 'GSE73103', 'GSE77445', 'GSE83334', 'GSE87571', 'GSE99624']
