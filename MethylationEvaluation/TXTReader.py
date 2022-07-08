import re

class TXTReader:
    """
    Process files in TXT format.
    """

    def __init__(self):
        pass

    @staticmethod
    def IterRead(file: str, num_read: int = 1, drop: str = r"", favor: str = r"") -> iter:
        """
        :param file: str File full path
        :param num_read:int The number of lines read each time
        :param drop: Drop the line/s including the given value
        :param favor: Keep the line/s including the given value
        :return:generator
        """
        count = 0
        lines = []
        try:
            with open(file, 'r') as f:
                for aline in f:
                    count += 1
                    lines.append(aline.strip())
                    if count >= num_read:
                        yield lines
                    # Free buffer zone
                        count = 0
                        lines.clear()
            # yield the reset lines counted less than num_read
                if count > 0:
                    yield lines
        except IOError:
            ioError = "Sorry, the file " + file + " does not exist."
            print(ioError)

    @staticmethod
    def IterReadMatrix(file: str, rows: range, cols: range, col_delimiter: str = r" ") -> iter:
        """
        :param file:str File full path
        :param rows:The range of rows the file needs to be split on
        :param cols:The range of columns the file needs to be split on
        :param col_delimiter: the delimiter/s may be used in the text file, examples: r"[ \n\t;,!]"

        """
        try:
            with open(file, 'r') as f:
                for i in range(rows.start):
                    next(f)
            try:
                for i in range(rows.start, rows.stop):
                    aline = f.readline()
                    if not aline:
                        break
                    elements = re.split(col_delimiter, aline)
                    yield elements[cols.start:cols.stop]
            except IndexError:
                print("Please input the correct range!")
        except IOError:
            ioError = "Sorry, the file " + file + " does not exist."
            print(ioError)

    # def split_row(self, line_count):
    #     for i in range(int(len(self.context) / line_count)):
    #         self.write_file(i, i, self.context[i:i + line_count])
    #
    #
    # def split_column(self, column_count):
    #     df = pd.DataFrame(self.context)
    #     print(df.shape[1])
    #     for i in range(int(df.shape[1] / column_count)):
    #         temp_list = np.array(df[range(i, i + column_count)]).tolist()
    #         for j in range(len(temp_list)):
    #             temp_list[j] = list(filter(None, temp_list[j]))
    #         self.write_file(i, i, temp_list)

    # def get_part_file_name(self, part_num, temp_count):
    #     """"获取分割后的文件名称：在源文件相同目录下建立临时文件夹temp_part_file，然后将分割后的文件放到该路径下"""
    #     temp_path = os.path.dirname(self.file)  # 获取文件的路径（不含文件名）
    #     temp_name = os.path.splitext(os.path.basename(self.file))[0]
    #     part_file_name = temp_path + os.sep + temp_name
    #     if not os.path.exists(part_file_name):  # 如果临时目录不存在则创建
    #         os.makedirs(part_file_name)
    #     part_file_name += os.sep + temp_name + "_part" + str(part_num) + "_" + str(temp_count) + ".txt"
    #     return part_file_name

    # def write_file(self, part_num, temp_count, *line_content):
    #     """
    #
    #     """
    #     part_file_name = self.get_part_file_name(part_num, temp_count)
    #     try:
    #         with open(part_file_name, "w") as part_file:
    #             for i in line_content[0]:
    #                 part_file.writelines(i)
    #                 part_file.write("\n")
    #
    #     except IOError as err:
    #         print(err)

    # def write_file(self, part_num, temp_count, *line_content):
    #     """将按行分割后的内容写入相应的分割文件中"""
    #     # print(temp_count)
    #     part_file_name = self.get_part_file_name(part_num, temp_count)
    #     try:
    #         with open(part_file_name, "w") as part_file:
    #             for i in line_content[0]:
    #                 part_file.writelines(i)
    #                 part_file.write("\n")
    #
    #     except IOError as err:
    #         print(err)


if __name__ == "__main__":
    # Example for IterRead
    # test = TXTReader()
    # result = test.IterRead("TXT_test.txt", 3)
    # for line in result:
    #     print(line)
    #
    # Example for IterReadMatrix
    # test = TXTReader()
    # result = test.IterReadMatrix("TXT_test.txt", range(0, 3), range(0, 2), r"[ \n]")
    # for line in result:
    #     print(line)