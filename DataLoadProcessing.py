
import torch
import numpy as np
import torch.utils.data as Data
from sklearn.model_selection import train_test_split


class DataSplitProcessing():

    def __init__(self):
        pass

    def train_val_test_split(self, matrix, label, split_ratio={'val_size': 0.125, 'test_size': 0.2}, random_state=59):
        x_train, x_test, y_train, y_test = train_test_split(matrix, label, test_size=split_ratio['test_size'],
                                                            random_state=random_state)
        if split_ratio['val_size'] != 0:
            x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=split_ratio['val_size'],
                                                                random_state=random_state)
            return x_train, x_val, x_test, y_train, y_val, y_test

        return x_train, x_test, y_train, y_test

    def dataloader(self, matrix, label, batch_size=32, shuffle=True, drop_last=True):
        Dataset = Data.TensorDataset(matrix, label)
        DataLoader = Data.DataLoader(dataset=Dataset, batch_size=batch_size, shuffle=shuffle, drop_last=drop_last)
        return DataLoader