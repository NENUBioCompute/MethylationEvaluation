# -*- coding: utf-8 -*-
# @Time    : 2022/7/29 20:41, 2023/1/5
# @Author  : ouyangxike, Jing.Qu
# @Email   : 1586658982@qq.com, qujing579@163.com
# @File    : CSVDealer.py
# @Software: PyCharm
import csv
from MethylationEvaluation.Utilities.FileDealers.FileSystem import *

class CSVDealer:
    """
    Process files in CSV format.
    """
    @staticmethod
    def IterRead(file:str, num_read: int = 1,col_delimiter: str = " " ,drop:str = r"", favor:str = r"")->iter:

        count = 0
        lines = []
        csv.field_size_limit(500 * 1024 * 1024)
        csv.register_dialect('mydialect', delimiter=col_delimiter, quoting=csv.QUOTE_ALL)
        with open(file, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile, dialect='mydialect')
            for aline in csv_reader:
                count += 1
                lines.append(aline)
                if count >= num_read:
                    yield lines
                    count = 0
                    lines.clear()
            if count > 0:
                yield lines

    @staticmethod
    def IterReadMatrix(file:str, rows:range, cols:range, col_delimiter: str = '') -> iter:

        csv.register_dialect('mydialect', delimiter=col_delimiter, quoting=csv.QUOTE_ALL)
        dicts = {}
        with open(file, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile, dialect='mydialect')
            result = list(csv_reader)
            for aline in result[rows.start:rows.stop]:
                for j in range(cols.start, cols.stop):
                    new_aline = list(aline.items())
                    dicts[new_aline[j][0]] = new_aline[j][1]
                yield dicts

    @staticmethod
    def CSVWriter(contents, save_path):
        with open(save_path, "w") as csvfile:
            writer = csv.writer(csvfile)
            for content in contents:
                writer.writerow(content)



if __name__ == '__main__':

    iter_reader = CSVDealer.IterRead('../../data/dgidb/categories/categories.tsv', 5, '\t')
    for lines in iter_reader:
        for aline in lines:
            print(aline)
