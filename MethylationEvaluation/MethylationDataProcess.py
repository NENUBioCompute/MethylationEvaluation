
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
        if txt:
            data = __statTXT(file)
        elif csv:
            readcsv
        elif .gz:
            0000

        for item in data:

        return outputfiles

    def __statTXT(self, file):
        return iterable

    def SplitFile(self, file: str, rows, columns, output_path: str):
        """
        Description:
        :param file: The full path of the file to be split
        :param rows: The rows for each sub-file, it should allow the inputs as: row number, row labels, or row indexes
        :param columns: The columns for each sub-file, it should allow the inputs as parameter "rows"
        :param output_path: A fold to output the result files
        :return: True-succeed, False-failed
        """
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
        return False

    def FillMissingElements(self, file: str, missing_elems, filling_elems, outfile: str):
        """
        Description:
        :param file: The original file with missing elements
        :param filling_elems: An iterable object containing the locations of all missing values
        :param missing_elems: An iterable object containing all the values to fill
        :param outfile: Full path of the result file to be created
        :return: True-succeed, False-failed
        """
        return False