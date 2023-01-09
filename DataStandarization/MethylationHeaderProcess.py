
import os
import pandas as pd
import json
from MethylationEvaluation.Utilities.FileDealers.ConfigParser import ConfigParser
from MethylationEvaluation.Utilities.FileDealers.ExcelDealer import ExcelDealer
from HeaderMappingDict import HeaderMappingDict
from collections import defaultdict

class MethylationHeaderMapping:

    def __init__(self):
        self.anomaly = set()

    def get_mapping_infor(self, dataset_id, fetch):
        """
        get mapping_dict correlate with dataset and the columns need to extract from raw
        :param dataset_id: dataset id
        :param fetch: contain: 'Tissue', 'Disease', 'Condition', 'Age', 'AgeUnit', 'Gender', 'Race', 'ALL' means all items
        :return:
        """
        mapping_infor = HMDict.fetch_mapping_dict_by_dataset_id(dataset_id, fetch)
        extract_cols_from_raws = {key: col for key, item in mapping_infor.items() for col in item}
        return mapping_infor, extract_cols_from_raws

    def get_raw_data(self, original_df, extract_cols_from_raw):
        """
        extract the data from raw data according to the columns
        :param original_df: raw data
        :param extract_cols_from_raw: object columns
        :return: needed columns for mapping
        """
        extracted_raw_data = pd.DataFrame()
        for key, col in extract_cols_from_raw.items():
            if col in original_df:
                extracted_raw_data[col] = original_df[col]
            elif '/' in str(col):
                self.anomaly[''].add(key)
            else:
                extracted_raw_data[col] = [col] * original_df.shape[0]
        return extracted_raw_data

    def replace_values(self, mapping_infor, extracted_raw_data):
        """
        compare the original data and the mapping value, replace and create a new dataframe
        :param mapping_infor: a dict contain the mapping value
        :param extracted_raw_data: be extracted raw data
        :return: mapped data
        """
        mapped_data = pd.DataFrame()
        for key, values in mapping_infor.items():
            for orignal_col, mapping_value in values.items():
                mapped_data[key] = extracted_raw_data[orignal_col].replace(mapping_value)
        for col in mapped_data.columns:
            mapped_data = mapped_data.drop(mapped_data[mapped_data[col] == '#remove#'].index)
        return mapped_data

    def compare_raw_with_mapped(self, raw_data, mapped_data):
        """
        compare two version data and get difference
        :param raw_data: original data
        :param mapped_data: new data
        :return: dict indicate difference
        """
        common_col = set(raw_data.columns).intersection(set(mapped_data.columns))
        record_diff = defaultdict(dict)
        complement_dict = {key: [] for key in common_col}
        for col in common_col:
            raw_version = set([str(item) for item in raw_data[col] if str(item) != 'nan'])
            mapped_version = set([str(item) for item in mapped_data[col] if str(item) != 'nan'])
            raw_diff = raw_version.difference(mapped_version)
            mapped_diff = mapped_version.difference(raw_version)
            if not raw_diff and not mapped_diff:
                complement_dict[col].append(' ')
                continue
            complement_dict[col].append('*')  # the difference value
            record_diff[col] = {'raw_version': sorted(list(raw_diff)),
                                'mapped_version': sorted(list(mapped_diff))
                                }
        complement_df = pd.DataFrame(complement_dict)
        return complement_df, record_diff

    def statistic_value_num(self, mapped_data):
        """
        statistic the mapping value amount in the mapped_data
        :param mapped_data: mapped_data: mapped data
        :return: a dict record the mapping value and its amount
        """
        counter_dict = {}
        for col in mapped_data.columns:
            counter_dict[col] = defaultdict(int)
            for index, row in mapped_data.iterrows():
                counter_dict[col][str(row[col])] += 1
        return counter_dict

    def merge_dict_counter(self, single_dict, gatherer_dict):
        """

        :param single_dict:
        :param gatherer_dict:
        :return:
        """
        for key, values in single_dict.items():
            if key not in gatherer_dict:
                gatherer_dict[key] = {}
            for name, number in values.items():
                if name in gatherer_dict[key]:
                    gatherer_dict[key][name] += number
                else:
                    gatherer_dict[key][name] = number
        return gatherer_dict


if __name__ == '__main__':
    config = ConfigParser.GetConfig('../conf/MethylationData.config')

    # this define the basic content contain the path, assigned value, setting, etc.
    mapping_path_params = {
        'Data': {
            'path': config.get('DataMapping', 'path'),
            'sheet': config.get('DataMapping', 'sheet'),
            'columns': config.get('DataMapping', 'columns')
        },
        'Tissue': {
            'path': config.get('TissueMapping', 'path'),
            'sheet': config.get('TissueMapping', 'sheet'),
            'columns': config.get('TissueMapping', 'columns')
        },
        'Disease': {
            'path': config.get('DiseaseMapping', 'path'),
            'sheet': config.get('DiseaseMapping', 'sheet'),
            'columns': config.get('DiseaseMapping', 'columns')
        },
        'Condition': {
            'path': config.get('ConditionMapping', 'path'),
            'sheet': config.get('ConditionMapping', 'sheet'),
            'columns': config.get('ConditionMapping', 'columns')
        },
        'Age': {
            'path': config.get('AgeMapping', 'path'),
            'sheet': config.get('AgeMapping', 'sheet'),
            'columns': config.get('AgeMapping', 'columns')
        },
        'Gender': {
            'path': config.get('GenderMapping', 'path'),
            'sheet': config.get('GenderMapping', 'sheet'),
            'columns': config.get('GenderMapping', 'columns')
        },
        'Race': {
            'path': config.get('RaceMapping', 'path'),
            'sheet': config.get('RaceMapping', 'sheet'),
            'columns': config.get('RaceMapping', 'columns')
        }
    }
    fetch = config.get('DataStandarization', 'fetch')
    raw_data_path = config.get('DataParsers', 'meta_data_path')
    sample_identifier = config.get('DataStandarization', 'sample_identifier')
    mapped_data_save_dir = config.get('DataStandarization', 'mapped_data_dir')
    mapped_header_named = config.get('DataStandarization', 'mapped_header_named')

    header = MethylationHeaderMapping()

    # read xlsx file，according to the assigned sheet
    data_df, tissue_df, disease_df, condition_df, age_df, gender_df, race_df = ExcelDealer.MultiExcelReader(
        mapping_path_params)

    # create mapping_dict
    data_for_mapping = {
        'Tissue': tissue_df, "Disease": disease_df, "Age": age_df,
        "Gender": gender_df, "Condition": condition_df, "Race": race_df
    }
    HMDict = HeaderMappingDict()
    mapping_dict = HMDict.create_mapping_dict(data_df, data_for_mapping)


    raw_file_names = os.listdir(raw_data_path)
    for raw_file_name in raw_file_names:
        dataset_id = raw_file_name.split('_')[0]
        raw_data_file = os.path.join(raw_data_path, raw_file_name)
        try:
            original_df = pd.read_csv(raw_data_file)
            # get mapping_dict correlate with dataset
            mapping_dict, extract_cols_from_raw = header.get_mapping_infor(dataset_id, fetch)

            # extract raw data according to mapping_dict
            extract_cols_from_raw[sample_identifier] = sample_identifier
            extracted_raw_data = header.get_raw_data(original_df, extract_cols_from_raw)

            # replace mapping value
            mapped_data = header.replace_values(mapping_dict, extracted_raw_data)

            # save data
            mapped_file_path = os.path.join(mapped_data_save_dir, dataset_id + mapped_header_named)
            mapped_data.to_csv(mapped_file_path, index=False)
        except:
            print(dataset_id, 'Field!')
            continue

    # compare and statistic
    compare_differ_dict, counter_dict = {}, {}
    compare_complement_table = pd.DataFrame()
    old_mapped_dir = config.get('CompareAndStatistic', 'old_mapped_dir')
    for file_name in os.listdir(mapped_data_save_dir):
        dataset_id = file_name.split('_')[0]
        # read csv file
        new_mapped_path = os.path.join(mapped_data_save_dir, file_name)
        old_mapped_path = os.path.join(old_mapped_dir, file_name)
        new_mapped_file = pd.read_csv(new_mapped_path)
        old_mapped_file = pd.read_csv(old_mapped_path)

        # compare new mapped version with old version
        complement_df, record_diff = header.compare_raw_with_mapped(old_mapped_file, new_mapped_file)
        complement_df['dataset'] = dataset_id
        compare_complement_table = pd.concat([compare_complement_table, complement_df], axis=0)
        compare_differ_dict[dataset_id] = record_diff

        # count the value number in mapped file
        counter_dict_single = header.statistic_value_num(new_mapped_file)
        counter_dict = header.merge_dict_counter(counter_dict_single, counter_dict)

    compare_differ_path = config.get('CompareAndStatistic', 'compare_differ_path')
    compare_complement_path = config.get('CompareAndStatistic', 'compare_complement_path')
    counter_dict_path = config.get('CompareAndStatistic', 'counter_dict_path')

    compare_complement_table.to_csv(compare_complement_path, index=False)
    ExcelDealer.MultiSheetWriterFromDict(counter_dict_path, counter_dict)
    with open(compare_differ_path, 'w') as jf:
        json.dump(compare_differ_dict, jf, indent=4, ensure_ascii=False)





