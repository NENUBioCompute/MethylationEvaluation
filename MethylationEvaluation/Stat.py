import pandas as pd


class Stat:
    def __init__(self):
        pass

    def MissingValue(self, file):
        data = pd.DataFrame(file)
        num = data.isnull().sum()

        miss = {
            'missValue': {
                'num': num,
                'position': [[1, 2], [3, 4], [3, 5]]
            },
            'missElements': {
                'num': 1000,
                'position': [[], [], []]
            },
            'errValue': {
                'num': 1000,
                'position': [[], [], []]
            }
        }
        return miss


    def MissingElements(self, file):
        pass

    def ErrValues(self, file):
        pass