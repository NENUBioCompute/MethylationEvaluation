import pandas as pd
import numpy as  np
import torch
import torch.utils.data as Data
from sklearn.model_selection import train_test_split


class LoadData():
    """
    loads the Dataset from ths csv files passed the parser.
    """

    def __init__(self, ID):
        self.ID = ID

    #         self.calculate_stat()

    def load_origin_data(self):
        # load data
        matrix_file = './Datasets/beta/{}_beta.csv'.format(self.ID)
        label_file = './Datasets/meta/{}_meta.csv'.format(self.ID)
        orign_matrix = pd.read_csv(matrix_file)
        label = pd.read_csv(label_file)
        #######后续把表达矩阵处理一下，就不用这两行了##
        orign_matrix.index = orign_matrix['Unnamed: 0']
        matrix = orign_matrix[[col for col in orign_matrix.columns if col != 'Unnamed: 0']]
        ###########################################
        matrix = pd.DataFrame(matrix.values.T, index=matrix.columns, columns=matrix.index)
        label.index = label['ID']
        return matrix, label

    def divide_data(self, matrix, label, label_key='Age', test_size=0.2, random_state=59):
        x_train, x_test, y_train, y_test = train_test_split(matrix, label[label_key], test_size=test_size,
                                                            random_state=random_state)
        # transform to numpy, to tensor
        if torch.cuda.is_available():
            x_train = torch.tensor(np.array(x_train).astype('float64')).cuda()
            x_test = torch.tensor(np.array(x_test).astype('float64')).cuda()
            y_train = torch.tensor(np.array(y_train).astype('float64')).cuda()
            y_test = torch.tensor(np.array(y_test).astype('float64')).cuda()
        else:
            x_train = torch.tensor(np.array(x_train).astype('float64'))
            x_test = torch.tensor(np.array(x_test).astype('float64'))
            y_train = torch.tensor(np.array(y_train).astype('float64'))
            y_test = torch.tensor(np.array(y_test).astype('float64'))
        return x_train, x_test, y_train, y_test

    def calculate_stat(self):
        matrix, label = self.load_origin_data()
        print(matrix.shape, label.shape)
        
    def calculate_mul(self, matrix):
        return torch.tensor([np.array(torch.mul(x, x.T)) for x in matrix])

    def calculate_complement(self, matrix):
        square_root = math.ceil(pow(matrix.shape[2], 1/2))
        comp_num = pow(square_root, 2) - matrix.shape[2]
        zeros_ = torch.zeros([matrix.shape[0], 1, comp_num], dtype=torch.float64)
        X = torch.cat((matrix, zeros_), 2).reshape(matrix.shape[0], 1, square_root, square_root)
        return X

    def load_datasets(self):
        matrix, label = self.load_origin_data()
        x_train, x_test, y_train, y_test = self.divide_data(matrix, label, label_key='Age', test_size=0.3,
                                                            random_state=59)
        return x_train, x_test, y_train, y_test

    def get_sequence_data(self, X, y):
        X = X.unsqueeze(1)
        data_loader = self.get_DataLoader(X, y, batch_size=32, shuffle=True)
        return data_loader

    def get_image_data_in_Matrix_mul(self, X, y):
        X = X.unsqueeze(2)
        X = self.calculate_mul(X)
        data_loader = self.get_DataLoader(X, y, batch_size=32, shuffle=True)
        return data_loader
    
    def get_image_data_in_reshape(self, X, y):
        X = X.unsqueeze(1)
        X = self.calculate_complement(X)
        data_loader = self.get_DataLoader(X, y, batch_size=32, shuffle=True)
        return data_loader
    
    def get_DataLoader(self, X, y, batch_size=32, shuffle=True):
        Dataset = Data.TensorDataset(X, y)
        Loader = Data.DataLoader(dataset=Dataset, batch_size=batch_size, shuffle=shuffle)
        return Loader


if __name__ == '__main__':
    dataset = 'GSE20236'

    data = LoadData(dataset)
    x_train, x_test, y_train, y_test = data.load_datasets()

    # if you load data as images-input
    train_DataLoader = data.get_image_data_in_reshape(x_train, y_train)  # train
    test_DataLoader = data.get_image_data_in_reshape(x_test, y_test)  # test

    # if you load data as sequences-input
    # train_DataLoader = data.get_sequence_data(x_train, y_train)  # train
    # test_DataLoader = data.get_sequence_data(x_test, y_test)  # test
