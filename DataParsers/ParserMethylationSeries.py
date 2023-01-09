# @Author : Jing.Qu
# @Time :2022/12/29

import os
import collections
import pandas as pd
from MethylationEvaluation.Utilities.FileDealers.CSVDealer import CSVDealer
from MethylationEvaluation.Utilities.FileDealers.ConfigParser import ConfigParser
from MethylationEvaluation.Utilities.FileDealers.MethSeriesParser import MethSeriesParser
from MethylationEvaluation.Utilities.FileDealers.FileSystem import *
from MethylationEvaluation.Utilities.FileDealers.TxtFileDealer import TxtFileDealer


class ParserMethylationSeries:

    def start(self):
        config = ConfigParser.GetConfig('../conf/MethylationData.config')
        uncompress_path = config.get('DataSources', 'uncompress_data_path')
        beta_path = config.get('DataParsers', 'beta_data_path')
        meta_path = config.get('DataParsers', 'meta_data_path')
        meta_named = config.get('DataParsers', 'meta_data_named')
        beta_named = config.get('DataParsers', 'beta_data_named')
        folder_is_exists.__func__(beta_path)
        folder_is_exists.__func__(meta_path)
        com, pData, exprs = self.__classifier(uncompress_path)

        # pheno and exprs in series_matrix file
        for file_name in com:
            dataset = file_name.split('_')[0]
            file_path = os.path.join(uncompress_path, file_name)
            meta_save_path = os.path.join(meta_path, dataset + meta_named)
            beta_save_path = os.path.join(beta_path, dataset + beta_named)

            pData_df = self.parser_pheno(file_path)
            pData_df.to_csv(meta_save_path, index=False)

            lines = TxtFileDealer.IterRead(file_path)
            items = MethSeriesParser.parser_exprs(lines)
            CSVDealer.CSVWriter(items, beta_save_path)
            # exprs_df = self.parser_exprs(file_path)
            # exprs_df.to_csv(beta_save_path, index=False)
            # del pData_df, exprs_df

        # pheno in series_matrix file
        for file_name in pData:
            dataset = file_name.split('_')[0]
            file_path = os.path.join(uncompress_path, file_name)
            meta_save_path = os.path.join(meta_path, dataset + meta_named)

            pData_df = self.parser_pheno(file_path)
            pData_df.to_csv(meta_save_path, index=False)
            del pData_df

        # exprs in excess matrix file
        name_suffix, file_suffix = beta_named.split('.')
        for file_names in exprs:
            dataset = file_name.split('_')[0]
            file_path = os.path.join(uncompress_path, file_name)
            for i, file_name in enumerate(file_path):
                beta_save_path = os.path.join(beta_path, "{}{}_{}.{}".format(dataset, name_suffix, i, file_suffix))
                CSVDealer.CSVWriter(CSVDealer.IterRead(file_names), beta_save_path)

    def __classifier(self, dir_path):
        file_names = os.listdir(dir_path)
        com, pData, exprs = set(), set(), set()
        for file_name in file_names:
            syn_file = set([name for name in file_names if file_name.split('_')[0] in name])
            if len(syn_file) > 1:
                series_file = '{}_series_matrix.txt'.format(dataset)
                pData.add(series_file)
                exprs.union(syn_file.difference(set(series_file)))
            else:
                com.add(file_name)
        return com, pData, exprs

    def parser_pheno(self, file_path):
        lines = TxtFileDealer.IterRead(file_path)
        items = MethSeriesParser.parser_pData(lines)
        pData_df = pd.DataFrame()
        for key, value in items:
            counter = collections.Counter(pData_df.columns.str.contains(key[:-1]))
            if counter[True]:
                num = counter[True] + 1
                key = key[:-1] + str(num)
            pData_df[key] = value
        pData_df = MethSeriesParser.add_new_col(pData_df, identifier=': ', col_term=':ch1')
        return pData_df

    def parser_exprs(self, file_path):
        keys, values = [], []
        lines = TxtFileDealer.IterRead(file_path)
        items = MethSeriesParser.parser_exprs(lines)
        for key, value in items:
            keys.append(key)
            values.append(value)
        exprs_df = pd.DataFrame(data=values, columns=keys)
        return exprs_df


if __name__ == '__main__':
    parser = ParserMethylationSeries()
    parser.start()
