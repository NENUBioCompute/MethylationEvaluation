
import tensorflow as tf
import numpy as np
import pandas as pd
import time

class AltumAge:
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
        methylation_scaled = self.scaler.transform(methylation_data[self.cpgs])
        pred_age = self.model.predict(methylation_scaled).flatten()
        return pred_age


if __name__ =='__main__':

    dataset = 'GSE20236'
    start = time.time()

    # load data
    data_other = pd.read_csv('/home/data/Standardized/mapped_lv3/{}_pheno.csv'.format(dataset))
    methylation = pd.read_csv('/home/data/Standardized/express/{}_beta.csv'.format(dataset))
    methylation.index = methylation['Unnamed: 0']
    methylation = methylation[methylation.columns[1:]].T
    true_age = data_other['Age'].astype('float64')

    AA = AltumAge('AltumAge.h5', 'scaler.pkl', 'multi_platform_cpgs.pkl')
    pred = AA.predict(methylation)
    end = time.time()
    consume_time = (end - start) / 60
