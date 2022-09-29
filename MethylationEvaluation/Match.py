class Match:
    def __init__(self):
        pass

    def matchSampleName(self, betaData, phenoData):
        """
        :param betaData:
        :param phenoData:
        :return:
        """
        pass

    def deleteSampleName(self, betaData, metaData):
        """
        :param betaData:
        :param metaData:
        :return:
        """
        sampleList = metaData['ID']
        for name in list(betaData.columns.values):
            if name not in sampleList:
                betaData.drop([name], axis=1)
        self.matchSampleSeq(betaData)

    def matchSampleSeq(self, betaData, metaData):
        """
        :param betaData:
        :param metaData:
        :return:
        """
        sampleList = metaData['ID']
        betaData = betaData[[sampleList]]
        return betaData

