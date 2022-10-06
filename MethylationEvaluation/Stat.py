import pandas as pd


class Stat:
    def __init__(self):
        pass

    def MissingValue(self, file):
        data = pd.DataFrame(file)
        num = data.isnull().sum()
        pos = [[1, 2], [2, 3], [4, 5]]
        return num, pos


    def MissingElements(self, file):
        pass

    def ErrValues(self, file):
        pass
