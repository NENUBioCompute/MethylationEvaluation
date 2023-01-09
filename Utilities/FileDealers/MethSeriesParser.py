"""
@Author  ：Jing.Qu
@File    ：Uncompress.py
@Purpose ：Parser Methylation Series Matrix File
@Created ：2022.12.28
"""

from MethylationEvaluation.Utilities.FileDealers.TxtFileDealer import TxtFileDealer
from MethylationEvaluation.Utilities.FileDealers.Uncompress import Uncompress
from MethylationEvaluation.Utilities.FileDealers.CSVDealer import CSVDealer
import pandas as pd
import multiprocessing as mp
from joblib import Parallel, delayed

class MethSeriesParser:

    @staticmethod
    def parser_pData(batch_size):
        for lines in batch_size:
            for line in lines:
                items = [item.strip('"').strip() for item in line.split('\t')]
                if '!series_matrix_table_begin' in line: break
                if items and '!Sample' in items[0]:
                    yield items[0][8:], items[1:]

    @staticmethod
    def parser_exprs(batch_size):
        flag = False
        for lines in batch_size:
            for line in lines:
                if '!series_matrix_table_begin' in line:
                    flag = True
                    continue
                if '!series_matrix_table_end' in line:
                    flag = False
                if flag:
                    items = [item.strip('"').strip() for item in line.split('\t')]
                    yield items  #items[0], items[1:]

    def parser_pData_and_exprs_com(self, file_path):
        pData, exprs = {}, {}
        flag = False
        for line in TxtFileDealer.IterRead(file_path, num_read=1):
            line = line[0]
            if '!series_matrix_table_begin' in line:
                flag = True
                continue
            if '!series_matrix_table_end' in line:
                flag = False
            items = [item.strip('"').strip() for item in line.split('\t')]
            if items and '!Sample' in items[0]:
                if items[0][8:] in pData:
                    num = len([key for key in pData if items[0][8:-1] in key]) + 1
                    pData[items[0][8:-1]+str(num)] = items[1:]
                    # print(items[1:])
                else:
                    pData[items[0][8:]] = items[1:]
            if flag:
                exprs[items[0]] = items[1:]
        return pData, exprs

    @staticmethod
    def add_new_col(data, identifier=': ', col_term=':ch1'):
        data = data.astype('str')
        new_col_names = {item.split(identifier)[0] for col in data.columns for item in data[col] if identifier in item}
        for new_col in new_col_names:
            data[new_col+col_term] = pd.DataFrame(data=None, columns=[new_col])
        for col in data.columns:
            if True in list(data[col].str.contains(identifier)):
                for index in data.index:
                    split_elems = data[col][index].split(identifier)
                    if len(split_elems) > 2:
                        new_col, value = split_elems[0], " ".join(split_elems[1:])
                    elif len(split_elems) > 1:
                        new_col, value = split_elems
                    else:
                        new_col, value = None, None
                    if new_col:
                        data[new_col+col_term][index] = value
                        data[new_col+col_term].str.strip()
        return data

if __name__ == '__main__':

    dataset = 'GSE40279'
    # download_file_path = '/home/data/Download/{}_series_matrix.txt.gz'.format(dataset)
    # Uncompress().start(download_file_path)
    file_path = '/home/data/Download/{}_series_matrix.txt'.format(dataset)
    beta_save_path = '{}_matrix.csv'.format(dataset)
    meta_save_path = '{}_pheno.csv'.format(dataset)

    lines = TxtFileDealer.IterRead(file_path, num_read=1)
    pData_items, exprs_items = MethSeriesParser.parser_pData(lines), MethSeriesParser.parser_exprs(lines)

    # pData
    pData_df = pd.DataFrame()
    for key, value in pData_items:
        pData_df[key] = value
    pData_df = MethSeriesParser.add_new_col(pData_df, identifier=': ', col_term=':ch1')
    pData_df.to_csv(meta_save_path, index=False)

    # exprs
    items = MethSeriesParser.parser_exprs(lines)
    CSVDealer.CSVWriter(exprs_items, beta_save_path)