from Python.FeSTwo.Lib_FeatureEngineering import NewFeatures
from Utilities.FileDealers.PickleDealer import PickleDealer
import re
import pandas as pd
import numpy as np
import copy


class FeSTwo:

    def __init__(self, model_file, cpgs_file):
        self.model = PickleDealer.load_pfile(model_file)
        self.fea_selected = list(PickleDealer.load_pfile(cpgs_file))
        self.raw, self.processed = set(), []

    def predict(self, methylation_data):
        """
        Predict m epigenetic states given an m x n methylation array
        :param data: feature matrix
        :return: predicted results
        """
        return self.model.predict(methylation_data)

    def fetch_feature_name(self):
        pattern = re.compile('"(.+?)"')
        for fea in self.fea_selected:
            fea = pattern.findall(fea)[0]
            self.raw.add(fea)
            self.processed.append(fea)

    def get_square_vectors(self, square_data):
        """
        FeatureEngineering--Square
        :param sqare_data: raw data
        :return: squared data
        """
        FE = NewFeatures(n_jobs=-1, type_='Square')
        dfSquare = FE.transform(square_data)
        return dfSquare

    def get_raw_vectors(self, data, fill_value):
        """
        FeatureEngineering--raw
        :param sqare_data: methylation matrix data
        :return: contain be selected cpgs data that not need to FeatureEngineering
        """
        # filling the NA cpgs use 0.5
        methylation = pd.DataFrame(np.full((len(data), len(self.raw)), fill_value), columns=self.raw, index=data.index)
        common = set(self.raw).intersection(set(list(data)))
        methylation[list(common)] = data[list(common)].astype('float32')
        dfRaw = pd.DataFrame(methylation[self.raw], dtype=np.float64)
        return dfRaw

    def get_sqare_raw_vertor(self, data, fill_value):
        # get feature vectors respectively
        self.fetch_feature_name()
        dfRaw = self.get_raw_vectors(data, fill_value)
        square_data = copy.deepcopy(dfRaw)
        dfSquare = self.get_square_vectors(square_data)
        # raw+square
        raw_square = pd.concat([dfRaw, dfSquare], axis=1)
        # extract used features
        fea_vector = raw_square[self.processed]
        fea_vector = fea_vector.replace('NaN', 0.5)
        return fea_vector


def FeSTwoTest(file_path):
    # methylation = pd.read_csv(file_path, compression='gzip')
    methylation = pd.read_csv(file_path)
    methylation.index = methylation[methylation.columns[0]]
    methylation = methylation[methylation.columns[1:]].T
    # get feature vector
    FE = FeSTwo("Python/FeSTwo/FeSTwo_lr_Model.pkl",
                "Python/FeSTwo/command_Combination_FesTwo_lr_raw_Square.pickle")
    fea_vector = FE.get_sqare_raw_vertor(methylation)
    # get predicted ages
    pred_age = FE.predict(fea_vector)
    return pred_age



