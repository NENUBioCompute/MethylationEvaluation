from Utilities.FileDealers.PickleDealer import PickleDealer
import pandas as pd
import numpy as np
import os


class EPM:
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

    def predict(self, methylation_data, fill_value):
        """
        Predict n epigenetic states given an m x n methylation array
        :param data: feature matrix
        :return: predicted results
        """
        try:
            feture_vertors = methylation_data[self.cpgs].values.T

        except KeyError:
            cpgs_data = pd.DataFrame(np.full((len(methylation_data), len(self.cpgs)), fill_value), columns=self.cpgs,
                                     index=methylation_data.index)
            common = set(self.cpgs).intersection(set(list(methylation_data)))
            cpgs_data[list(common)] = methylation_data[list(common)].astype('float64')
            feture_vertors = cpgs_data[self.cpgs].values.T

        return self.model.predict(feture_vertors)


def EPMTest(file_path):
    # X_test = pd.read_csv(file_path, compression='gzip')
    X_test = pd.read_csv(file_path)
    X_test.index = X_test[X_test.columns[0]]
    X_test = X_test[X_test.columns[1:]].T

    # generate predicted ages sing the test data
    epm_cv = EPM('../Python/EpigeneticPacemaker/EPM_model.pkl',
                 '../Python/EpigeneticPacemaker/selected_cpg_sites_NO22.pickle')
    pred_age = epm_cv.predict(X_test)

    return pred_age


