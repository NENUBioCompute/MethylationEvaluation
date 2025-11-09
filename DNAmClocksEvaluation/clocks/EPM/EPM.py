
from utils.pickle_dealer import PickleDealer
import pandas as pd
import numpy as np
import os
    
class EPM_calculate:
    """
    The Epigenetic Pacemaker, EPM,
    is an implementation of a fast conditional expectation maximization algorithm
    that models epigenetic states under and evolutionary framework.
    url: https://epigeneticpacemaker.readthedocs.io/en/latest/
    Methods in author package:
    fit(meth_array: numpy.array, states: numpy.array)
    predict(meth_array: numpy.array) -> predicted epigenetic states: numpy.array
    score(meth_array: numpy.array, states: numpy.array) -> Pearson R: Tuple[significance, R value]
   """

    def __init__(self, model_file, cpgs_file):
        self.model = PickleDealer.load_pfile(model_file)
        self.cpgs = PickleDealer.load_pfile(cpgs_file)

    def predict(self, methylation_data):
        """
        Predict n epigenetic states given an m x n methylation array
        :param data: feature matrix
        :return: predicted results
        """
        try:
            feture_vertors = methylation_data[self.cpgs].values.T

        except KeyError:
            cpgs_data = pd.DataFrame(np.full((len(methylation_data), len(self.cpgs)), 0.5), columns=self.cpgs, index=methylation_data.index)
            common = set(self.cpgs).intersection(set(list(methylation_data)))
            cpgs_data[list(common)] = methylation_data[list(common)].astype('float64')
            feture_vertors = cpgs_data[self.cpgs].values.T

        return self.model.predict(feture_vertors)
    
def EPM(file_path, method_dir=None):
    """ 
    Predict epigenetic age using EPM model
    :param file_path: path to the methylation data file (CSV format)
    :param method_dir: directory containing the EPM model files
    :return: predicted epigenetic ages
    """
    # Change working directory if method_dir is provided
    if method_dir:
        original_dir = os.getcwd()
        os.chdir(method_dir)
    try:
        X_test = pd.read_csv(file_path)
        X_test.index = X_test[X_test.columns[0]]
        X_test = X_test[X_test.columns[1:]].T

        # generate predicted ages sing the test data
        epm_cv = EPM_calculate('EPM_model.pkl',
                        'selected_cpg_sites_NO22.pickle')
        pred_age = epm_cv.predict(X_test)
            
        return pred_age
    finally:
        # Restore original working directory
        if method_dir:
            os.chdir(original_dir)
            print(f"Restored working directory to: {original_dir}")


if __name__ == '__main__':
    # Example usage
    import sys
    if len(sys.argv) > 1:
        dataset_path = sys.argv[1]
        method_dir = sys.argv[2] if len(sys.argv) > 2 else None
        result = EPM(dataset_path, method_dir)
        print("Results:", result)
    else:
        print("Usage: python EPM.py <dataset_path> [method_dir]")