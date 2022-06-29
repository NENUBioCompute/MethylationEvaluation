import csv
import pandas as pd


class CsvIterReader:
    @staticmethod
    def iterRead(file, count=10000):
        """
        逐行读取文件
        :param file: str 文件名
        :param count: int 需要一次读取的行数
        :return: list 返回需要行数的数据
        """
        fileContext = []
        a = 0
        with open(file) as f:
            reader = csv.reader(f)
            for line in reader:
                fileContext.append(line)
                if len(fileContext) < count:
                    continue
                yield fileContext
                fileContext.clear()
        if fileContext:
            yield fileContext
        f.close()

    def splitExpressionMatrix(self, file, row=(1, 5), col=(0, 5)):
        """
        按照传入的行列范围分割表达矩阵
        :param file: str 文件名
        :param row: tuple 需要切割的行范围
        :param col: tuple 需要切割的列范围
        :return: dataframe 切割后的表达矩阵
        """
        # _, expressionMatrix = self.splitFile(file)
        rowList = list(row)  # 切割的行范围
        rowLeft = rowList[0]  # 切割的列范围
        rowRight = rowList[1]  #
        colList = list(col)  # 切割的列范围
        data = []  # 存放切割后的数据
        ID_REF = []  # 表达矩阵GSM_ID序列
        cpg = []  # 表达矩阵cpgs序列
        for lines in self.iterRead(file):
            for i, line in enumerate(lines):
                if i == 0:
                    ID_REF = line[colList[0]:colList[1] + 1]
                else:
                    if rowLeft <= i <= rowRight:
                        cpg.append(line[0])
                        data.append(self.fillMissingValues(line)[colList[0]:colList[1] + 1])
            if rowRight > len(lines):
                rowLeft = 0
                rowRight -= len(lines)
            else:
                break
        newExpressionMatrix = pd.DataFrame(data, index=cpg, columns=ID_REF)
        # 甲基化数据处理
        if 'ID' in newExpressionMatrix.index.values:
            newExpressionMatrix.drop(index='ID', inplace=True)
        if 'ID' in newExpressionMatrix.columns.tolist():
            newExpressionMatrix.drop(columns='ID', inplace=True)
        return newExpressionMatrix

    @staticmethod
    def fillMissingValues(data):
        """
        :param data: list 需要填补的数据
        :return: list 填补缺失值后的数据
        """
        newData = []  # 存放填补缺失值后的数据
        dataSum = 0  # 所有元素和，用于计算均值
        count = 0  # 空值个数
        if 'ID' == data[0]:
            return data
        print(data)
        for i in range(1, len(data)):
            if data[i] != '' and data[i] != 'NA':
                count += 1
                dataSum += eval(data[i])
        newData.append(data[0])
        for i in range(1, len(data)):
            if data[i] == '' or data[i] != '"NA"' or eval(data[i]) <= 0 :
                newData.append(dataSum / count)
            else:
                newData.append(eval(data[i]))
        return newData


if __name__ == '__main__':
    csvRead = CsvIterReader()
    csvRead.splitExpressionMatrix('../RawData/GSE72777_datBeta.csv', row=(0, 5), col=(0, 5))
