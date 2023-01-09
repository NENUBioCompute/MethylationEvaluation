from collections import defaultdict
import copy


class HeaderMappingDict:

    def __init__(self):
        self.mapping_dict = {}  #self.create_mapping_dict(data_mapping, **kwargs)

    def fetch_mapping_dict_by_dataset_id(self, dataset_id, fetch='ALL'):
        """
        get mapping_dict according to the dataset_id and fetched identifier
        :param dataset_id: a string indicate dataset id
        :param fetch: contain: 'Tissue', 'Disease', ;Condition', 'Age', 'AgeUnit', 'Gender', 'Race', 'ALL' means all items
        :return: a mapping_dict corresponding  with dataset_id and consist with 8 elements, witch GEOID, Tissue,
        Disease, Condition, Age, AgeUnit, Gender, Race.
        """
        if fetch == 'ALL':
            return self.mapping_dict[dataset_id]
        elif fetch not in self.mapping_dict[dataset_id]:
            raise Exception("Sorry, this is not normal item!")
        else:
            return self.mapping_dict[dataset_id][fetch]

    def create_mapping_dict(self, data_mapping, kwargs):
        """
        create mapping dict by combine several sub mapping-vocabulary to one mapping-dictionary
        :param data_mapping: the DataFrame form of DataMapping File,
        :param kwargs: the DataFrames form of other ValueMapping File
        :return: mapping_dict
        """
        sub_dict_data = self.create_sub_dic_data(data_mapping)
        self.mapping_dict = copy.deepcopy(sub_dict_data)
        for key, dataframe in kwargs.items():
            sub_dict_value = self.create_sub_dic_value(dataframe)
            for dataset_id, mapping_value in sub_dict_value.items():
                self.mapping_dict[dataset_id][key] = {col: mapping_value for col in sub_dict_data[dataset_id][key]}
        # return mapping_dict

    def create_sub_dic_data(self, data):
        """
        create mapping-vocabulary for data
        :param data: dataframe
        :return: dict, {DatasetID: value}, value={'': '', '': ''}
        """
        new_dict = {}
        for row_index, row_value in data.iterrows():
            new_dict[row_value[0]] = {data.columns[col_index + 1]: {col_value: {}} for col_index, col_value in
                                      enumerate(row_value[1:])}  # only support one columns mapping
        return new_dict

    def create_sub_dic_value(self, data):
        """
        create mapping-vocabulary for data
        :param data: dataframe
        :return: dict, {DatasetID: value}, value={'': '', '': ''}
        """
        new_dict = defaultdict(dict)
        for row_index, row_value in data.iterrows():
            new_dict[row_value[0]][row_value[1]] = row_value[-1]
        return new_dict





