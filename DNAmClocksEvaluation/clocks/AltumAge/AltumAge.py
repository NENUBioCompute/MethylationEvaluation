
import tensorflow as tf
import numpy as np
import pandas as pd
import os
from pathlib import Path


class AltumAge_calculate:
    """
    Requirements:
        python >= 3.8
        tensorflow == 2.5.0
        numpy == 1.19.5
        pandas == 1.3.0
        sklearn == 0.24.2
    """

    def __init__(self, model_file, scaler_file, cpgs_file):
        self.model = tf.keras.models.load_model(model_file)
        self.scaler = pd.read_pickle(scaler_file)
        self.cpgs = np.array(pd.read_pickle(cpgs_file))

    def predict(self, methylation_data):
        """
        Predict m epigenetic states given an m x n methylation array
        :param data: feature matrix
        :return: predicted results
        """
        try:
            methylation_scaled = self.scaler.transform(methylation_data[self.cpgs].values)
        except KeyError:
            cpgs_data = pd.DataFrame(np.full((len(methylation_data), len(self.cpgs)), 0.5), columns=self.cpgs,
                                     index=methylation_data.index)
            common = set(self.cpgs).intersection(set(list(methylation_data)))
            cpgs_data[list(common)] = methylation_data[list(common)].astype('float64')
            methylation_scaled = self.scaler.transform(cpgs_data[self.cpgs].values)

        pred_age = self.model.predict(methylation_scaled).flatten()
        return pred_age 


def AltumAge(file_path, method_dir=None):
    """
    Predict epigenetic age using AltumAge model
    :param file_path: path to the methylation data file (CSV format)
    :param method_dir: directory containing the AltumAge model files 
    :return: predicted epigenetic ages
    """
    # Change working directory if method_dir is provided
    if method_dir:
        original_dir = os.getcwd()
        os.chdir(method_dir)
    try:
        methylation = pd.read_csv(file_path)
        methylation.index = methylation[methylation.columns[0]]
        methylation = methylation[methylation.columns[1:]].T

        AA = AltumAge_calculate('AltumAge.h5', 'scaler.pkl', 'multi_platform_cpgs.pkl')
        pred = AA.predict(methylation)
    
        return pred
    finally:
        # Restore original working directory
        if method_dir:
            os.chdir(original_dir)

# testing code 
if __name__ == "__main__":
    # Example usage
    import sys
    if len(sys.argv) > 1:
        dataset_path = sys.argv[1]
        method_dir = sys.argv[2] if len(sys.argv) > 2 else None
        result = AltumAge(dataset_path, method_dir)
        print("Results:", result)
    else:
        print("Usage: python AltumAge.py <dataset_path> [method_dir]")