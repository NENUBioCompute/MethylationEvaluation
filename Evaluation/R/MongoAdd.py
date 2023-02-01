import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['DNAmClocks']
col = mydb['datasets']


def addData(data):
    col.insert_one(data)
    print(data)

def getDataset():
    datasets = []
    for item in col.find():
        datasets.append(item)
    return datasets

print(getDataset())