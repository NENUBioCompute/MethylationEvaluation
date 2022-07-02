from TXTReader import TXTReader


class MethylationDataProcess:
    """
    Description:
    """

    def StaticData(self, file: str, flag="ALL", tofile=False):
        """
        Description:
        :return: Default outputs the st
        :param file:  The Methylation source data file full path
        :param flag: If the caller requires outputting the statistics results, it should be an iterable
                       object containing a group of strings, such as: "MissingValues", "MissingElements", "ErrValues"
        :param tofile: Default as False, set to True when the statical results are required storing in files
        :return: The statical results or the corresponding files
        """
        pass

    def SplitFile(self, file: str, destpath: str, rows: range, cols: range, col_delimiter: str = r" ") -> str:
        """
        :param file: The file to be split
        :param destpath: The folder to keep sub-files
        :param rows:
        :param cols:
        :param col_delimiter:
        :return:
        """
        try:
            matrix = TXTReader.IterReadMatrix(file, rows, cols, col_delimiter)
        except Exception as e:
            raise e
        try:
            self.__write_to_file(destpath, matrix)
        except Exception as e:
            raise e
        return destpath

    def FillMissingValues(self, file: str, missing_values, filling_values, outfile: str):
        """
        Description:
        :param file: The original file with missing values
        :param missing_values: An iterable object containing the locations of all missing values
        :param filling_values: An iterable object containing all the values to fill
        :param outfile: Full path of the result file to be created
        :return: True-succeed, False-failed
        """
        pass

    def FillMissingElements(self, file: str, missing_elems, filling_elems, outfile: str):
        """
        Description:
        :param file: The original file with missing elements
        :param filling_elems: An iterable object containing the locations of all missing values
        :param missing_elems: An iterable object containing all the values to fill
        :param outfile: Full path of the result file to be created
        :return: True-succeed, False-failed
        """
        pass

    def __generate_subfile_name(self, file, index):
        pass

    # This function should be in the package of file utility
    def __write_to_file(self, file: str, content: iter) -> list:
        pass