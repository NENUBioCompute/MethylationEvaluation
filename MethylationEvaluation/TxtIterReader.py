import re
import csv
import pandas as pd


class TxtIterReader:
    def __init__(self):
        pass

    @staticmethod
    def iterRead(file, count=10):
        """
        逐行读取文件
        :param file: str 文件名
        :param count: int 需要一次读取的行数
        :return: list 返回需要行数的数据
        """
        fileContext = []
        with open(file) as f:
            for line in f:
                fileContext.append(line.strip())
                if len(fileContext) < count:
                    continue
                yield fileContext
                fileContext.clear()
        if fileContext:
            yield fileContext
        f.close()

    def splitFile(self, file):
        """
        分割头文件和表达矩阵
        :param file: str 文件路径名
        :return: list 头文件和表达矩阵
        """
        phenoData = []  # 存放头文件
        expressionMatrix = []  # 存放表达矩阵
        tag = False
        for lines in self.iterRead(file, 10000):
            for line in lines:
                if tag:
                    if '!series_matrix_table_end' in line:
                        break
                    expressionMatrix.append(line.strip())
                else:
                    if '!series_matrix_table_begin' in line:
                        tag = True
                    phenoData.append(line.strip())
        # 保存头文件
        with open('phenoData.txt', 'w') as wf:
            for item in phenoData:
                wf.write(item)
                wf.write('\n')
        wf.close()
        # 保存表达矩阵
        with open('expressionMatrix.txt', 'w') as wf:
            for item in expressionMatrix:
                wf.write(item)
                wf.write('\n')
        wf.close()
        # 表达矩阵行数，用于切割表达矩阵
        exprMatrixLen = len(expressionMatrix)
        return phenoData, expressionMatrix, exprMatrixLen

    def processPheno(self, file):
        """
        处理头文件，生成新的头文件
        :param file: str 文件名
        :return: dict/csv 新的头文件
        """
        phenoData, _, _ = self.splitFile(file)
        for item in phenoData:
            if 'age' in item:
                age = re.sub('age: ', '', item).replace('"', '').split('\t')
            if 'sex' in item:
                sex = re.sub('sex: ', '', item).replace('"', '').split('\t')
            if 'sample_id' in item:
                sample_id = item.replace('"', '').replace('!Series_sample_id\t', '').split(' ')
            if 'source_name' in item:
                tissues = item.replace('"', '').split('\t')
        age = [eval(item) for item in age[1:]]
        sex = sex[1:]
        tissues = tissues[1:]
        diease = ['' for i in range(len(age))]
        race = ['' for i in range(len(age))]

        newPhenoData = []
        for i in range(len(age)):
            newPhenoData.append(
                {
                    'ID_REF': sample_id[i],
                    'Sex': sex[i],
                    'Age': age[i],
                    'Tissue': tissues[i],
                    'Diease': diease[i],
                    'Race': race[i]
                }
            )
        # 保存新的头文件
        with open('newPhoneData.csv', 'w', newline='', encoding='utf-8') as f:
            csv_writer = csv.DictWriter(f, fieldnames=list(newPhenoData[0].keys()))
            csv_writer.writeheader()
            csv_writer.writerows(newPhenoData)
        f.close()
        return newPhenoData

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
                print(line)
                if 'ID_REF' in line.replace('"', '').split('\t'):
                    ID_REF = line.replace('"', '').split('\t')[colList[0]:colList[1] + 1]
                if rowLeft <= i <= rowRight:
                    cpg.append(line.replace('"', '').split('\t')[0])
                    data.append(self.fillMissingValues(line.replace('"', '').split('\t'))[colList[0]:colList[1] + 1])
            if rowRight > len(lines):
                rowLeft = 0
                rowRight -= len(lines)
            else:
                break
        print(ID_REF)
        newExpressionMatrix = pd.DataFrame(data, index=cpg, columns=ID_REF)
        # 甲基化数据处理
        if 'ID_REF' in newExpressionMatrix.index.values:
            newExpressionMatrix.drop(index='ID_REF', inplace=True)
        if 'ID_REF' in newExpressionMatrix.columns.tolist():
            newExpressionMatrix.drop(columns='ID_REF', inplace=True)
        newExpressionMatrix.to_csv('result4.csv')
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
        if 'ID_REF' == data[0]:
            return data
        for i in data[1:]:
            if i != '':
                count += 1
        for i in range(1, len(data)):
            if data[i] != '':
                dataSum += eval(data[i])
        newData.append(data[0])
        for i in range(1, len(data)):
            if data[i] == '' or eval(data[i]) <= 0:
                newData.append(dataSum / count)
            else:
                newData.append(eval(data[i]))
        return newData


if __name__ == '__main__':
    txt = TxtIterReader()
    # 1. 拆分头文件和表达矩阵，分别存入两个文件
    # 头文件 GSEXXX_pheno.txt  表达矩阵 GSEXXX_beta.csv
    txt.splitFile('../RawData/GSE20242_series_matrix.txt')
    # 2. 生成新的头文件

    # 3. 分割表达矩阵并填补缺失值
    txt.splitExpressionMatrix('./expressionMatrix.txt', row=(0, 27), col=(0, 25))