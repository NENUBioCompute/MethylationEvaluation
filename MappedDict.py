##!/usr/bin/python3
"""
Author: J.QU
Purpose: Combine the Mapping vocabulary to dictionary
Created: 11/28/2022
"""

import pandas as pd
from mapping_argument import get_argparse
from collections import defaultdict

class MappedDict:
    def __init__(self):
        self.mapping_dict = defaultdict(dict)

    def main(self, args):
        """
        Integrate manual mapping-vocabulary to a comprehensive dictionary
        :param args:  self-defined value
        :return: mapping-dictionary, according to this dictionary mapping in the next step
        """
        # 读取xlsx文件，指定sheet
        data = pd.read_excel(args.DataMappingPath)  # , engine='openpyxl'
        tissue_value = pd.read_excel(args.ValueMappingPath, sheet_name='Tissue')
        disease_value = pd.read_excel(args.ValueMappingPath, sheet_name='Disease')
        age_value = pd.read_excel(args.ValueMappingPath, sheet_name='Age')
        gender_value = pd.read_excel(args.ValueMappingPath, sheet_name='Gender')
        condition_value = pd.read_excel(args.ValueMappingPath, sheet_name='Condition')
        race_value = pd.read_excel(args.ValueMappingPath, sheet_name='Race')

        data_dict = self.get_dict(data, args.data_col)
        tissue_dict = self.get_dict(tissue_value, args.tissue_col)
        disease_dict = self.get_dict(disease_value, args.disease_col)
        age_dict = self.get_dict(age_value, args.agee_col)
        gender_dict = self.get_dict(gender_value, args.gender_col)
        condition_dict = self.get_dict(condition_value, args.condition_col)
        race_dict = self.get_dict(race_value, args.race_col)

        for i, GEO in enumerate(data_dict['GEO ID']):
            for key in list(data_dict.keys())[1:]:
                self.mapping_dict[GEO][key] = {data_dict[key][i]: defaultdict(dict)}

        self.filled_dict('Tissue', tissue_dict, args.tissue_word)
        self.filled_dict('Disease', disease_dict, args.disease_word)
        self.filled_dict('Condition', condition_dict, args.condition_word)
        self.filled_dict('Age', age_dict, args.age_word)
        self.filled_dict('Gender', gender_dict, args.gender_word)
        self.filled_dict('Race', race_dict, args.race_word)

        return self.mapping_dict

    def get_dict(self, data, data_col):
        """
        create mapping-vocabulary for each item (data, tissue, disease, condition, age, gender, race)
        :param data: dataframe
        :param data_col: useful columns
        :return: dict
        """
        data_df = data[data_col]  # extract the relative columns as operated data
        data_dict = defaultdict(list)
        for index in data_df.index:
            if str(data_df.loc[index].values[0]) != 'nan':
                for i, col in enumerate(data_col):
                    data_dict[col].append(data_df.loc[index].values[i])
        return data_dict

    def filled_dict(self, key, obj_dict, item):
        """
        combine several mapping-vocabulary to one mapping-dictionary
        :param key: str, such as 'Tissue', 'Disease', 'Condition', 'Age', 'Gender', 'Race'
        :param obj_dict: dict, a dict corresponding to key
        :param item: str, mapping-level
        :return:
        """
        for i, GEO in enumerate(obj_dict['GEO ID']):
            val = list(self.mapping_dict[GEO][key].keys())[0]
            unique_value = obj_dict['Unique Value'][i]  # if str(obj_dict['Unique Value'][i]) != 'nan' else 0
            self.mapping_dict[GEO][key][val][unique_value] = obj_dict[item][i]


if __name__ == '__main__':

    args = get_argparse().parse_args()
    a = MappedDict()
    mapping_dict = a.main(args)

