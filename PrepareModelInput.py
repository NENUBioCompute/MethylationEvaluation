
import torch
from FileReaderFactory import FileReaderFactory
from DataTypeProcessing import DataTypeProcessing
from DataFormatProcessing import DataFormatProcessing
from DataLoadProcesing import DataLoadProcessing

if __name__ == '__main__':
    # load data
    methylation_path = ''
    label_path = ''
    methylation = FileReaderFactory(methylation_path)
    label = FileReaderFactory(label_path)
    age = label['age']

    # convert to tensor type
    type = DataTypeProcessing()
    methylation_tensor  = type.to_tensor(methylation)
    age_tensor = type.to_tensor(age)

    # revise shape
    format = DataFormatProcessing()
    methylation_tensor = format.sequence_reshape_to_single_matrix(methylation_tensor)
    age_tensor = format.sequence_reshape_to_single_matrix(age_tensor)

    # split dataset
    load = DataLoadProcessing()
    x_train, x_test, y_train, y_test = load.train_val_test_split(methylation_tensor, age_tensor, split_ratio={'val_size': 0, 'test_size': 0.2})
    trainloader = load.dataloader(x_train, y_train)
    testloader = load.dataloader(x_test, y_test)