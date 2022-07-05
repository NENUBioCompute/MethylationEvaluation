import re


class TXTReader:
    def __init__(self):
        pass

    @staticmethod
    def IterRead(file: str, count: int = 1, drop: str = r"", favor: str = r"") -> iter:
        """
        :param file: str Filename to be split
        :param count: int Number of rows read at a time
        :param drop: Drop the line/s including the given value
        :param favor: Keep the line/s including the given value
        :return: 
        """
        fileContext = []
        with open(file, 'r') as f:
            for line in f:
                fileContext.append(line.strip())
                if len(fileContext) < count:
                    continue
                yield fileContext
                fileContext.clear()
                break
        if fileContext:
            yield fileContext
        f.close()

    @staticmethod
    def IterReadMatrix(file: str, rows: tuple, cols: tuple, col_delimiter: str = r" ") -> iter:
        """
        :param file: str Filename to be split
        :param rows: tuple Range of rows to be split
        :param cols: tuple Range of columns to be split
        :param col_delimiter: the delimiter/s may be used in the text file, examples: r"[ \n\t]"
        :return: Data of split
        """
        rowLeft = rows[0]
        rowRight = rows[1]

        with open(file, 'r') as f:
            for i, line in enumerate(f):
                if not line:
                    break
                if rowLeft <= i <= rowRight:
                    yield re.split(col_delimiter, line)[cols[0]:cols[1]]
                    # try:
                    #     data = re.split(col_delimiter, line)[cols[0]:cols[1]]
                    # except IndexError:
                    #     data = re.split(col_delimiter, line)[cols[0]:]
                    # finally:
                    #     yield data


if __name__ == '__main__':
    txt = TXTReader()
    for i in txt.IterReadMatrix('../../RawData/GSE20242_express_matrix.txt', (0,5), (0,5), '\t'):
        print(i)
