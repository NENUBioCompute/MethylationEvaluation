##!/usr/bin/python3
"""
Author: J.QU
Purpose: Conduct the Mapping processing
Created: 11/28/2022
"""

import os
import time
import pandas as pd
from collections import defaultdict
from mapping_argument import get_argparse
from MappedDict import MappedDict
from collections import defaultdict
import logging

args = get_argparse().parse_args()
# set logger, print to console and write to file
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
BASIC_FORMAT = "%(asctime)s:%(levelname)s: %(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
chlr = logging.StreamHandler()  # 输出到控制台的handler
chlr.setFormatter(formatter)
logfile = os.path.join(args.LogDir, 'anomaly_value_file_{}.txt'.format(time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))))
fh = logging.FileHandler(logfile)
fh.setFormatter(formatter)
logger.addHandler(chlr)
logger.addHandler(fh)

class Mapping:
    """
    Mapping the Heading File in dir
    """
    def __init__(self, mapping_dict):
        self.mapping_dict = mapping_dict
        self.anomaly = defaultdict(set)

    def main(self, args):
        """
        mapping and saving file one by one in dir
        :param args: self-defined value
        :return:
        """
        for i, file_name in enumerate(os.listdir(args.dir_path)):
            file_path = os.path.join(args.dir_path, file_name)
            if file_name.split('.')[-1] == 'csv':
                data = pd.read_csv(file_path)
            if file_name.split('.')[-1] == 'xlsx':
                data = pd.read_excel(file_path)
            dataset = file_name.split('_')[0]
            mapping_dict = self.mapping(dataset, fetch=args.Fetch)
            mapped_df = a.get_mapping_df(data, mapping_dict)
            try:
                # save file
                mapped_df.to_csv(os.path.join(args.save_path, file_name.split('.')[0] + '.csv'), index=None)
                logger.info('Dataset {}: save succeed!'.format(dataset))
            except:
                logger.info('Dataset {}: save unsucceed!'.format(dataset))
                continue
        logger.info("anomaly dataset: {}, num: {}".format(self.anomaly, len(self.anomaly)))

    def mapping(self, dataset, fetch='ALL'):
        """
        extract the mapping content according to fetch
        :param dataset: dataset-ID, str
        :param fetch: contain: 'Tissue', 'Disease', ;Condition', 'Age', 'AgeUnit', 'Gender', 'Race', 'ALL' means all items
        :return: object mapping content, dict
        """
        if fetch == 'ALL':
            return self.mapping_dict[dataset]
        elif fetch not in self.mapping_dict[dataset]:
            raise Exception("Sorry, this is not normal item!")
        else:
            return self.mapping_dict[dataset][fetch]

    def get_mapping_df(self, orign_df, mapping_dict):
        """
        compare the original data and the mapping value, replace and create a new dataframe
        :param orign_df: original dataset, dataframe
        :param mapping_dict: mapping dictionary, dict
        :return: new dataframe, dataframe
        """
        mapped_dict = defaultdict(list)
        if 'geo_accession' not in orign_df: return
        mapped_dict['ID'] = orign_df['geo_accession']
        for key, values in mapping_dict.items():
            for value_key, value_mapping in values.items():
                if value_key in orign_df:
                    orign_df[value_key] = orign_df[value_key].astype('str')
                    orign_df[value_key] = orign_df[value_key].replace({'nan': 'NaN', '': 'NaN'})
                    mapped_dict[key] = orign_df[value_key].replace(mapping_dict[key][value_key])
                elif '/' in value_key:
                    self.anomaly[''].add(key)
                else:
                    mapped_dict[key] = [value_key] * orign_df.shape[0]
        mapped_df = pd.DataFrame(mapped_dict)
        for col in list(mapped_df):
            mapped_df = mapped_df.drop(mapped_df[mapped_df[col] == '#remove#'].index)
        mapped_df = mapped_df.drop(mapped_df[mapped_df.Age.isnull].index)
        return mapped_df


if __name__ == '__main__':
    mapped_dict = MappedDict().main(args)
    a = Mapping(mapped_dict)
    a.main(args)