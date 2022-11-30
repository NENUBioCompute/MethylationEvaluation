from TXTReader import TXTReader
from FillNAValue import FillNAValue
from Normalize import Normalize
from Match import Match
from Stat import Stat
import pandas as pd


class MethylationDataProcess:
    """
    Description:
    """

    def StaticData(self, file: str, statSubjects="ALL", tofile=False):
        """
        Description:
        :return: Default outputs the st
        :param file:  The Methylation source data file full path
        :param statSubjects: If the caller requires outputting the statistics results, it should be an iterable
                       object containing a group of strings, such as: "MissingValues", "MissingElements", "ErrValues"
        :param tofile: Default as False, set to True when the statical results are required storing in files
        :return: The statical results or the corresponding files
        """
        stat = Stat()
        miss = {
            'missValue': {
                'num': 0,
                'position': []
            },
            'missElements': {
                'num': 0,
                'position': []
            },
            'errValue': {
                'num': 0,
                'position': []
            }
        }
        if file == 'txt' or file == 'csv':
            read = TXTReader
            data = read.IterRead(file)
            if statSubjects == 'ALL':
                num, pos = stat.MissingValue(data)
                miss['missValue']['num'] += num
                miss['missValue']['position'] += pos
        elif file == 'json':
            pass
        elif file == '.gz':
            pass
        return miss

    def __statTXT(self, file):
        return False

    def SplitFile(self, file: str, rows: range, columns: range, col_delimiter: str):
        """
        Description:
        :param file: The full path of the file to be split
        :param rows: The rows for each sub-file, it should allow the inputs as: row number, row labels, or row indexes
        :param columns: The columns for each sub-file, it should allow the inputs as parameter "rows"
        :param col_delimiter: the delimiter/s may be used in the text file, examples: r"[ \n\t;,!]"
        :return: data_path-succeed, False-failed
        """
        reader = TXTReader()
        data = []
        for i in reader.IterReadMatrix(file, rows, columns, col_delimiter):
            data.append(i)
        data = pd.DataFrame(data)
        # data.to_csv(output_path)
        return data

    def FillMissingValues(self, file: str, filling_fun: str, fixed_value=0.5, average_fun='row'):
        """
        Description: fill missing value methods: R package, fixedValue, average, mode...
        :param file: The original file with missing values
        :param filling_fun: fill value function
        :param fixed_value: fixed value when selecting fixed value fill method, default value 0.5
        :param average_fun: row average or col average when selecting average value fill method, default row average
        :return: data-succeed, False-failed
        """
        fill = FillNAValue()
        try:
            if filling_fun == 'R':
                data = fill.fill(file)
            elif filling_fun == 'fixed':
                data = fill.fixed(file, fixed_value)
            elif filling_fun == 'average':
                data = fill.average(file, average_fun)
            elif filling_fun == 'mode':
                data = fill.mode(file)
            return data
        except:
            print('fillNAValue error')
            return False

    def NormalizeFile(self, file, normalize_fun: str):
        """
        Description:
        :param file: The original file with missing elements
        :param normalize_fun: normalize methods
        :return: data-succeed, False-failed
        """
        nor = Normalize()
        try:
            if normalize_fun == 'R':
                data = nor.methylationFormula(file)
            else:
                data = nor.other()
            return data
        except:
            print('normalize error')
            return False

    def MatchFileElements(self, file, meta_file: str, pheno_file: str, outfile: str):
        """
        Description: Match some Elements methods: matchSampleName, deleteSampleName, matchSampleSeq
        :param file: The original file with needing to match some elements such as column names...
        :param meta_file: Full path of the result file to be created
        :param pheno_file: The original file
        :param outfile: Full path of the result file to be created
        :return: True-succeed, False-failed
        """
        match = Match()
        try:
            data = match.deleteSampleName(file, meta_file)
            data = pd.DataFrame(data)
            data.to_csv(outfile)
            return True
        except:
            print('match file error')
            return False

    def getPhenoData(self):
        meta_file = ''
        return meta_file


if __name__ == '__main__':
    meth = MethylationDataProcess()
    file = ''  # file  path
    rows, cols = range(), range()   #
    col_delimiter = ''
    output_path = ''
    filling_fun = ''
    normalize_fun = ''
    outfile = ''

    # get pheno file
    meta_file = meth.getPhenoData()
    # get file path
    data_file = meth.SplitFile(file, rows, cols, col_delimiter)
    # get normalized data
    data_nor = meth.NormalizeFile(data_file, normalize_fun)
    # get fillmissingvalue data
    data_fill = meth.FillMissingValues(data_nor, filling_fun)
    # get matched dataS
    meth.MatchFileElements(data_fill, meta_file, outfile)

