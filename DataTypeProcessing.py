
import torch
import numpy as np



class DataTypeProcessing():

    def __init__(self):
        pass

    def array_to_matrix(self, _array):
        """
        input the input data's shape is (x,1) or (1, x) and get the output data's shape is (x, x),
        operation: (x, 1) * (1, x) = (x, x)
        :param _array: nparray
        :return: matrix in format of (x, x)
        """
        assert _array.shape[0] == 1 or _array.shape[1] == 1, "input array's shape must be (x, 1) or (1, x) "
        return np.dot(_array.T, _array) if _array.shape[0] == 1 else np.dot(_array, _array.T)

    def to_numpy(self, data, data_type='float64'):
        """
        convert data's type to numpy in assign type
        :param data: nparray or list
        :param data_type: the expected data type
        :return: object data
        """
        assert '' not in data, "data contains '', please fill or replace"
        new_data = np.array(data).astype(data_type)
        return new_data

    def to_tensor(self, data, data_type='float64'):
        """
        convert data's type to tensor in assign type,
        if torch.cuda is available, to cuda format
        :param data: nparray or list
        :param data_type: the expected data type
        :return: object data
        """
        if torch.cuda.is_available():
            new_data = torch.tensor(self.to_numpy(data, data_type)).cuda()
        else:
            new_data = torch.tensor(self.to_numpy(data,data_type))
        return new_data