
from clocks.FeSTwo.Lib_FeatureEngineering import NewFeatures
from utils.pickle_dealer import PickleDealer
import re
import pandas as pd
import numpy as np
import copy
import os

class FeSTwo_calculate:

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

    def get_raw_vectors(self, data):
        """
        FeatureEngineering--raw
        :param sqare_data: methylation matrix data
        :return: contain be selected cpgs data that not need to FeatureEngineering
        """
        # filling the NA cpgs use 0.5
        methylation = pd.DataFrame(np.full((len(data), len(self.raw)), 0.5), columns=list(self.raw), index=data.index)
        common = set(self.raw).intersection(set(list(data)))
        methylation[list(common)] = data[list(common)].astype('float32')
        dfRaw = pd.DataFrame(methylation[list(self.raw)], dtype=np.float64)
        return dfRaw

    def get_sqare_raw_vertor(self, data):
        # get feature vectors respectively
        self.fetch_feature_name()
        dfRaw = self.get_raw_vectors(data)
        square_data = copy.deepcopy(dfRaw)
        dfSquare = self.get_square_vectors(square_data)
        # raw+square
        raw_square = pd.concat([dfRaw, dfSquare], axis=1)
        # extract used features
        fea_vector = raw_square[self.processed]
        fea_vector = fea_vector.replace('NaN', 0.5)
        return fea_vector
    
def FeSTwo(file_path, method_dir=None):
    """
    FeSTwo methylation age prediction
    :param file_path: str, path to the methylation data file (CSV format)
    :param method_dir: str or None, path to the method directory, if None, use current directory
    :return: predicted ages as a numpy array
    """
    # change working directory if method_dir is provided
    if method_dir:
        original_dir = os.getcwd()
        os.chdir(method_dir)
    try:
        methylation = pd.read_csv(file_path)
        methylation.index = methylation[methylation.columns[0]]
        methylation = methylation[methylation.columns[1:]].T
        # get feature vector
        FE = FeSTwo_calculate("FeSTwo_lr_Model.pkl", "command_Combination_FesTwo_lr_raw_Square.pickle")
        fea_vector = FE.get_sqare_raw_vertor(methylation)
        # get predicted ages
        pred_age = FE.predict(fea_vector)
        return pred_age
    finally:
        # Restore original working directory
        if method_dir:
            os.chdir(original_dir)

    
if __name__ == '__main__':
    # If this script is run directly, perform testing
    import sys
    if len(sys.argv) > 1:
        dataset_path = sys.argv[1]
        method_dir = sys.argv[2] if len(sys.argv) > 2 else None
        result = FeSTwo(dataset_path, method_dir)
        print("Results:", result)
    else:
        print("Usage: python FeSTwo.py <dataset_path> [method_dir]")