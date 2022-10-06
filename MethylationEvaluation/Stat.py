import pandas as pd


class Stat:
    def __init__(self):
        pass

    def MissingValue(self, file):
        data = pd.DataFrame(file)
        num = data.isnull().sum()
        pos = [[], [], []]
        return num, pos


    def MissingElements(self, file):
        pass

    def ErrValues(self, file):
        pass