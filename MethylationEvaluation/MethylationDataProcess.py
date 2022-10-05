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

    def SplitFile(self, file: str, rows: range, columns: range, col_delimiter: str, output_path: str):
        """
        Description:
        :param file: The full path of the file to be split
        :param rows: The rows for each sub-file, it should allow the inputs as: row number, row labels, or row indexes
        :param columns: The columns for each sub-file, it should allow the inputs as parameter "rows"
        :param col_delimiter: the delimiter/s may be used in the text file, examples: r"[ \n\t;,!]"
        :param output_path: A fold to output the result files
        :return: True-succeed, False-failed
        """
        reader = TXTReader()
        data = []
        for i in reader.IterReadMatrix(file, rows, columns, col_delimiter):
            data.append(i)
        data = pd.DataFrame(data)
        data.to_csv(output_path)
        return True

    def FillMissingValues(self, file: str, filling_fun: str, outfile: str, fixed_value=0.5, average_fun='row'):
        """
        Description: fill missing value methods: R package, fixedValue, average, mode...
        :param file: The original file with missing values
        :param outfile: Full path of the result file to be created
        :param filling_fun: fill value function
        :param fixed_value: fixed value when selecting fixed value fill method, default value 0.5
        :param average_fun: row average or col average when selecting average value fill method, default row average
        :return: True-succeed, False-failed
        """
        fill = FillNAValue()
        if filling_fun == 'R':
            data = fill.fill(file)
        elif filling_fun == 'fixed':
            data = fill.fixed(file, fixed_value)
        elif filling_fun == 'average':
            data = fill.average(file, average_fun)
        elif filling_fun == 'mode':
            data = fill.mode(file)
        return True

    def NormalizeFile(self, file: str, normalize_fun: str, outfile: str):
        """
        Description:
        :param file: The original file with missing elements
        :param normalize_fun: normalize methods
        :param outfile: Full path of the result file to be created
        :return: True-succeed, False-failed
        """
        nor = Normalize()
        if normalize_fun == 'R':
            data = nor.methylationFormula(file)
        else:
            data = nor.other()
        return False

    def MatchFileElements(self, file: str, meta_file: str, pheno_file: str, outfile: str):
        """
        Description: Match some Elements methods: matchSampleName, deleteSampleName, matchSampleSeq
        :param file: The original file with needing to match some elements such as column names...
        :param meta_file: Full path of the result file to be created
        :param pheno_file: The original file
        :param outfile: Full path of the result file to be created
        :return: True-succeed, False-failed
        """
        match = Match()
        data = match.deleteSampleName(file, meta_file)
        return False
