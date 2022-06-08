import os
import pandas as pd
from functools import wraps
from collections import defaultdict


class TxtFileDealer:
    """
    """
    @staticmethod
    def readline(func):
        @wraps(func)
        def read_file_wraper(file, *args, **kwargs):
            for line in TxtFileDealer.yield_read_line(file):
                func(*args, **kwargs)
            return read_file_wraper

    @staticmethod
    def yield_read_line(file):
        with open(file) as f:
            for line in f:
                yield line
        f.close()

    @staticmethod
    def get_df(file):
        """
        Description:
        :param file: The full path of the txt file to be split
        :return: Dataframe form of expression matrix
        """
        with open(file, 'r') as tf:
            lines = tf.readlines()

        sampleID = []
        cpg_sites = []
        methylation_values = []
        data_other = defaultdict(list)

        for i, line in enumerate(lines):
            if '!series_matrix_table_begin' in line:
                # get sample ID
                sampleID = [item.strip('"') for item in lines[i + 1].split()[1:]]
            if '!Sample_characteristics_ch1' in line:
                # get other information
                for item in line.split('"')[1:]:
                    item = item.strip().split(':')
                    if item[0]:
                        # key = 'age' if 'age' in item[0] else item[0]
                        # temp = item[1].strip() if item[1] != ' NA' else Null
                        data_other[item[0]].append(item[1].strip())
            if line[: 3] == '"cg':
                cpg_sites.append(line.split()[0].strip('"'))
                temp = []
                for item in line.split()[1:]:
                    item = None if item.strip() == 'null' or item.strip() == 'NULL' else float(item)
                    temp.append(item)
                methylation_values.append(temp)

        # define table
        df = pd.DataFrame(methylation_values, columns=sampleID, index=cpg_sites)
        return df