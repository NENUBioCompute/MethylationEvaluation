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

    def predict(self, methylation_data, fill_value):
        """
        Predict m epigenetic states given an m x n methylation array
        :param methylation_data:
        :param fill_value:
        :return: predicted results
        """
        # no fill
        # methylation_scaled = self.scaler.transform(methylation_data[self.cpgs])
        # fill 0.5
        try:
            methylation_scaled = self.scaler.transform(methylation_data[self.cpgs].values)

        except KeyError:
            cpgs_data = pd.DataFrame(np.full((len(methylation_data), len(self.cpgs)), fill_value), columns=self.cpgs,
                                     index=methylation_data.index)
            common = set(self.cpgs).intersection(set(list(methylation_data)))
            cpgs_data[list(common)] = methylation_data[list(common)].astype('float64')
            methylation_scaled = self.scaler.transform(cpgs_data[self.cpgs].values)
        pred_age = self.model.predict(methylation_scaled).flatten()
        return pred_age
