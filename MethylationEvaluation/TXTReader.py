import re


class TXTReader:
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
        f.close()

    @staticmethod
    def IterReadMatrix(file: str, rows: range, cols: range, col_delimiter: str = r" ") -> iter:
        """
        :param file:str File full path
        :param rows:The range of rows the file needs to be split on
        :param cols:The range of columns the file needs to be split on
        :param col_delimiter: the delimiter/s may be used in the text file, examples: r"[ \n\t;,!]"
        """
        with open(file, 'r') as f:
            for i in range(rows.start):
                next(f)
            for i in range(rows.start, rows.stop):
                aline = f.readline()
                if not aline:
                    break
                elements = re.split(col_delimiter, aline)
                col_len = len(elements)
                if cols.stop < col_len:
                    yield elements[cols.start:cols.stop]
                else:
                    yield elements[cols.start:col_len - 1]


if __name__ == '__main__':
    txt = TXTReader()
    for i in txt.IterReadMatrix('../../RawData/GSE20242_express_matrix.txt', range(0,5), range(0,5), '\t'):
        print(i)