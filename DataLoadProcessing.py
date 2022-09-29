
import torch
import numpy as np
import torch.utils.data as Data
from sklearn.model_selection import train_test_split


class DataSplitProcessing():

    def __init__(self):
        pass

    def train_val_test_split(self, matrix, label, split_ratio={'val_size': 0.125, 'test_size': 0.2}, random_state=59):
        """
        split the dataset(matrix, label) according to ratio to two format that contain
        the first train_dataset(x_train, y_train), test_dataset(x_test, y_test)
        the second train_dataset(x_train, y_train), test_dataset(x_test, y_test), and validation_datasets(x_val, y_val).
        give priority to train-test-split, then split train-validation-data from train dataset, if need to split validation dataset.

        :param matrix: nparray
        :param label: nparray
        :param split_ratio: dict, keys: val_size represent validation ratio, test_size represent test ratio
        :param random_state: random seed
        :return: splited datasets(x_, y_)
        """
        x_train, x_test, y_train, y_test = train_test_split(matrix, label, test_size=split_ratio['test_size'],
                                                            random_state=random_state)
        if split_ratio['val_size'] != 0:
            x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=split_ratio['val_size'],
                                                                random_state=random_state)
            return x_train, x_val, x_test, y_train, y_val, y_test

        return x_train, x_test, y_train, y_test

    def dataloader(self, matrix, label, batch_size=32, shuffle=True, drop_last=True):
        """
        make the dataloader by matrix and label.

        :param matrix: torch.tensor
        :param label: torch.tensor
        :param batch_size: int
        :param shuffle: bool
        :param drop_last: bool
        :return: objected, iterator
        """
        Dataset = Data.TensorDataset(matrix, label)
        DataLoader = Data.DataLoader(dataset=Dataset, batch_size=batch_size, shuffle=shuffle, drop_last=drop_last)
        return DataLoader
