import deal_file as df
import pandas as pd
import numpy as np

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
        data = []
        if file[-3:] == 'txt':
            for line in df.TxtFileDealer.yield_read_line(file):
                data.append(line)
            self.FillMissingValues()
            self.FillMissingElements()

        elif file[-3:] == 'csv':
            data = df.TxtFileDealer.yield_read_line(file)
            self.FillMissingValues()
            self.FillMissingElements()
        outputfiles = []
        for item in data:
            outputfiles.append(data)
        if tofile == True:
            pass
        else:
            return


    def __statTXT(self, file):
        return
        pass #iterable

    def SplitFile(self, file: str, rows, columns, output_path: str):
        """
        Description:
        :param file: The full path of the file to be split
        :param rows: The rows for each sub-file, it should allow the inputs as: row number, row labels, or row indexes
        :param columns: The columns for each sub-file, it should allow the inputs as parameter "rows"
        :param output_path: A fold to output the result files
        :return: True-succeed, False-failed
        """
        f = open(output_path, 'w')
        count = 0
        for line in df.TxtFileDealer.yield_read_line(file):
            if count < rows:
                f.write(line + '\n')
                count += 1
        f.close()
        return False

    def FillMissingValues(self, file: str, missing_values, filling_values, outfile: str):
        """
        Description:
        :param file: The original file with missing values
        :param missing_values: An iterable object containing the locations of all missing values
        :param filling_values: An iterable object containing all the values to fill
        :param outfile: Full path of the result file to be created
        :return: True-succeed, False-failed
        """
        ms = df.TxtFileDealer.get_df(file)
        ms.fillna(filling_values)
        return False

    def FillMissingElements(self, file: str, raw, missing_elems, filling_elems, outfile: str):
        """
        Description:
        :param file: The original file with missing elements
        :param filling_elems: An iterable object containing the locations of all missing values
        :param missing_elems: An iterable object containing all the values to fill
        :param outfile: Full path of the result file to be created
        :return: True-succeed, False-failed
        """
        ms = df.TxtFileDealer.get_df(file)
        methylation = pd.DataFrame(np.full((len(ms),len(raw)),0.5),columns=raw,index=ms.index)
        common = set(raw).intersection(set(list(ms)))
        methylation[list(common)] = ms[list(common)].astype('float32')

        return False

