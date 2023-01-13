import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

class FillNAValue:
    def __init__(self):
        pass

    def fill(self, betaData):
        methyLImp = importr('methyLImp')
        robjects.r.source('methyLImp.R')
        matrix = robjects.IntVector(betaData)
        mat_Int = robjects.r['matrix'](matrix, nrow = 2)
        res_MatInt = robjects.r.methyLImp(mat_Int)
        print(type(res_MatInt))
        print(res_MatInt)

    def average(self, betaData, rule='row'):
        """
        :param betaData: data that needs to be filled
        :param rule: row average or column average
        :return: data that filled
        """
        if rule == 'row':
            for index, row in betaData.iterrows():
                row.fillna(row.mean(), inplace=True)
        elif rule == 'column':
            for index, col in betaData.iteritems():
                col.fillna(col.mean(), inplace=True)
        return betaData

    def fixed(self, betaData, fixedValue=0.5):
        """
        :param betaData: data that needs to be filled
        :param fixedValue: fixed value of fill default 0.5
        :return: data that filled
        """
        betaData.fillna(fixedValue, inplace=True)
        return betaData

    def mode(self, betaData):
        """
        :param betaData: data that needs to be filled
        :return: data that filled
        """
        pass

if __name__ == '__main__':
    Fill = FillNAValue()
    Fill.fill([[1,2,3], [4,5,6]])