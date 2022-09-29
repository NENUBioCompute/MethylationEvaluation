class FillNAValue:
    def __init__(self):
        pass

    def fill(self, betaData):
        pass

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
        print(betaData)
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
