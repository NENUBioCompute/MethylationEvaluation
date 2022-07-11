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

    @staticmethod
    def IterReadMatrix(file: str, rows: range, cols: range, col_delimiter: str = r" ") -> iter:
        """
        :param file:str File full path
        :param rows:The range of rows the file needs to be split on
        :param cols:The range of columns the file needs to be split on
        :param col_delimiter: the delimiter/s may be used in the text file, examples: r"[ \n\t;,!]"

        """
        with open(file, 'r') as f:
            # If rows is out of range
            file_len = TXTReader.FileLen(file)
            if rows.start < rows.stop <= file_len:
                for i in range(rows.start):
                    next(f)
                for i in range(rows.start, rows.stop):
                    aline = f.readline()
                    if not aline:
                        break
                    elements = re.split(col_delimiter, aline)
                    col_len = len(elements)
                    #If cols is out of range
                    if cols.start < cols.stop <=col_len:
                        yield elements[cols.start:cols.stop]
                        col_len_temp = len(elements[cols.start:cols.stop])
                        # If it is a matrix
                        if col_len != col_len_temp:
                            raise Exception("Not a Matrix!")
                    else:
                        raise Exception("Please input the correct columns range!")
            else:
                raise Exception("Please input the correct row range!")

    @staticmethod
    def FileLen(file:str):
        File = TXTReader.IterRead(file, 1)
        File_len = 0
        for aline in File:
            File_len +=1
        return File_len


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
    #
    file_len = TXTReader.FileLen("E:/net download/GSE62867_series_matrix.txt")
    print(file_len)
    # file = TXTReader.IterReadMatrix("E:/net download/GSE62867_series_matrix.txt", range(46, 65), range(0, 5), r"[ \n\t]")
    # for line in file:
    #     print(line)



