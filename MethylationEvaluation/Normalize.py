class Normalize:
    def __init__(self):
        # self.betaData = betaData
        pass

    def methylationFormula(self, betaData, meth=0, step=2):
        """
        :param betaData:
        :param meth: first meth col
        :param step:
        :return:
        """
        for i in range(meth, len(betaData), step):
            betaData[:, i] = betaData[:, i] / (betaData[:, i] + betaData[:, i + 1] + 100)
        return betaData

    def other(self):
        pass
