
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
        dataset_cpgs = []  # cpgs in dataset
        for line in TXTReader.IterReadMatrix(file, (0, 485577), (0,1), '\t'):
            dataset_cpgs.append(line[0].strip('"'))
        miss_cpgs = []  # cpgs missing in the papers
        with open('./NO_cpgs_dict_14num.json') as f:
            cpgs_num = json.load(f)
            for item in cpgs_num:
                # difference set of CpG between papers and dataset
                miss_cpgs_list = list(set(cpgs_num[item]).difference(set(dataset_cpgs)))

                miss_cpgs_dict = {
                            'paper_id': 'N0.' + str(item),  # paper id
                            'miss_cpgs': miss_cpgs_list,  # missing cpgs
                            'miss_nums': len(miss_cpgs_list),  # number of missing cpgs
                            'miss_ratio': '{:.2%}'.format(len(miss_cpgs_list) / len(cpgs_num[item]))  # ratio of missing cpgs
                        }

                miss_cpgs.append(miss_cpgs_dict)
        f.close()

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
