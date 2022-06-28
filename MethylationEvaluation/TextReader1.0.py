import os
import pandas as pd
import numpy as np

import csv


class TxtFileReader:
    """
    文件处理
    """

    def __init__(self, file):
        self.file = file
        self.context = []
        self.line = 0
        with open(self.file, 'r') as f:
            reader = f.read()
            line = reader.split('\n')  # 使用换行
            self.line = len(line)  # 统计有多少行
        for i in range(len(line)):
            self.context.append(line[i].split('\t'))

    def IterReader(self, readcount=200):
        """
        读取文件
        :param file:文件名称
        :param readcount: 需要一次读取的行数,默认两百行
        """

        i = 0
        FileContext = []  # 设置行的缓冲区
        with open(self.file, 'r') as f:
            next(f)
            for line in f:
                i += 1
                FileContext.append(line.strip())
                if i >= readcount:
                    yield FileContext
                    # 释放缓冲区
                    i = 0
                    FileContext.clear()
        # 剩余行
        if i > 0:
            yield FileContext

    def split_row(self, line_count):
        for i in range(int(len(self.context) / line_count)):
            self.write_file(i, i, self.context[i:i + line_count])

    def split_column(self, column_count):
        df = pd.DataFrame(self.context)
        print(df.shape[1])

        for i in range(int(df.shape[1] / column_count)):
            temp_list = np.array(df[range(i, i + column_count)]).tolist()
            for j in range(len(temp_list)):
                temp_list[j] = list(filter(None, temp_list[j]))
            self.write_file(i, i, temp_list)

    def get_part_file_name(self, part_num, temp_count):
        """"获取分割后的文件名称：在源文件相同目录下建立临时文件夹temp_part_file，然后将分割后的文件放到该路径下"""
        temp_path = os.path.dirname(self.file)  # 获取文件的路径（不含文件名）
        temp_name = os.path.splitext(os.path.basename(self.file))[0]
        part_file_name = temp_path + os.sep + temp_name
        if not os.path.exists(part_file_name):  # 如果临时目录不存在则创建
            os.makedirs(part_file_name)
        part_file_name += os.sep + temp_name + "_part" + str(part_num) + "_" + str(temp_count) + ".txt"
        return part_file_name

    def write_file(self, part_num, temp_count, *line_content):
        """将按行分割后的内容写入相应的分割文件中"""
        # print(temp_count)
        part_file_name = self.get_part_file_name(part_num, temp_count)

        try:
            with open(part_file_name, "w") as part_file:
                for i in line_content[0]:
                    part_file.writelines(i)
                    part_file.write("\n")

        except IOError as err:
            print(err)


if __name__ == "__main__":
    test_txt = TxtFileReader("./GSE42510_series_matrix.txt")
    # test_txt.split_row(10)  # 按行分割
    test_txt.split_column(3)  # 按列分割
