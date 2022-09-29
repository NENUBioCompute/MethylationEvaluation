
import torch
import numpy as np
import math

class DataFormatProcessing():

    def __init__(self):
        pass

    def sequence_reshape_to_square_matrix(self, sequences):
        """
        reshape the sequence data to square matrix to suit for the ConV2D net,
        if the dimension of sequence is not enough for square, and then fill the zero
        :param sequences: tensor.torch, (sample_num, feature_dim) or (batch_size, 1, feature_dim)
        :return: square matrix
        """
        single_matrix = self.sequence_reshape_to_single_matrix(sequences)
        square_root = math.ceil(pow(single_matrix.shape[2], 1 / 2))
        comp_num = pow(square_root, 2) - single_matrix.shape[2]
        zeros_ = torch.zeros([single_matrix.shape[0], 1, comp_num], dtype=torch.float64)
        square_matrix = torch.cat((single_matrix, zeros_), 2).reshape(single_matrix.shape[0], 1, square_root, square_root)
        return  square_matrix

    def sequence_reshape_to_single_matrix(self, sequences):
        """
        reshape the sequence data to square matrix to suit for the ConV1D net,
        :param sequences: tensor.torch, (sample_num, feature_dim) or (batch_size, 1, feature_dim)
        :return: square matrix
        """
        _shape = list(sequences.shape())
        single_matrix = sequences.unsqueeze(1) if len(_shape) == 2 else sequences
        return single_matrix

    def image_reshape_to_sequence(self, images):
        pass