import os
import torch
import torch.nn as nn
import numpy as np
import torch
import pandas as pd
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

class SEAttention(nn.Module):
    """
    Squeeze-and-Excitation (SE) Attention Block.

    This module adaptively recalibrates channel-wise feature responses.
    """
    def __init__(self, channel=512, reduction=16):
        super().__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channel, channel // reduction, bias=False),
            nn.LeakyReLU(inplace=True),
            nn.Linear(channel // reduction, channel, bias=False),
            nn.LeakyReLU(inplace=True)
        )

    def forward(self, x):
        """
        Forward pass of SEAttention.
        Args:
            x: Tensor of shape (batch_size, channels, H, W)
        Returns:
            Re-weighted tensor of same shape.
        """
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y.expand_as(x)

class MLP(torch.nn.Module):
    """
    Multi-layer Perceptron (MLP) model with integrated SE attention.
    Designed for age prediction from methylation features.
    """
    def __init__(self, in_features,num_hidden_1=32,num_hidden_2=32,num_hidden_3=32,num_hidden_4=32):
        super().__init__()
        self.atten = SEAttention(1362)
        self.my_network = torch.nn.Sequential(
            # 1st hidden layer
            torch.nn.Linear(in_features, num_hidden_1, bias=False),
            torch.nn.LeakyReLU(),
            torch.nn.BatchNorm1d(num_hidden_1),
            torch.nn.Dropout(0.1),

            # 2nd hidden layer
            torch.nn.Linear(num_hidden_1, num_hidden_2, bias=False),
            torch.nn.LeakyReLU(),
            torch.nn.BatchNorm1d(num_hidden_2),
            torch.nn.Dropout(0.1),

            # 3nd hidden layer
            torch.nn.Linear(num_hidden_2, num_hidden_3, bias=False),
            torch.nn.LeakyReLU(),
            torch.nn.BatchNorm1d(num_hidden_3),
            torch.nn.Dropout(0.1),

            # 4nd hidden layer
            torch.nn.Linear(num_hidden_3, num_hidden_4, bias=False),
            torch.nn.LeakyReLU(),
            torch.nn.BatchNorm1d(num_hidden_4),
            torch.nn.Dropout(0.1),

            # 5nd hidden layer
            torch.nn.Linear(num_hidden_4, 1, bias=False),

        )

    def forward(self, x):
        """
        Forward pass of MLP.
        - Reshapes input into 4D tensor for SEAttention
        - Applies SE attention
        - Flattens and passes through MLP layers
        """
        try:
            x = np.reshape(x,(x.shape[0], 1362,6,3),order='F')
            x = self.atten(x)
            x = x.detach().numpy()
            x = np.reshape(x,(x.shape[0],-1),order='F')
            x = torch.tensor(x)
            x = self.my_network(x)
            return x.squeeze()
        except Exception:
            raise ValueError("Input shape mismatch: expected (batch_size, 1362*6*3).")

class MethylationDataset(Dataset):
    """
    Custom PyTorch dataset for DNA methylation data.

    Parameters
    ----------
    feature_array : np.ndarray
        Input methylation beta value matrix (samples x CpGs).
    dtype : np.dtype
        Data type for conversion (default: np.float32).
    """
    def __init__(self, feature_array: np.ndarray, dtype=np.float32):
        if not isinstance(feature_array, np.ndarray):
            raise ValueError("`feature_array` must be a numpy.ndarray.")
        self.features = feature_array.astype(dtype)

    def __getitem__(self, idx):
        """Return a single sample by index."""
        return self.features[idx]
    
    def __len__(self):
        """Return total number of samples."""
        return self.features.shape[0]

def predict_age(model, dataloader, device):
    """
    Predicts biological age using a trained model.

    Parameters
    ----------
    model : torch.nn.Module
        Trained MLP model.
    dataloader : torch.utils.data.DataLoader
        Test data loader.
    device : str
        Device to run inference ("cpu" or "cuda").

    Returns
    -------
    list
        Predicted biological ages.
    """
    model.eval()
    preds = []
    with torch.no_grad():
        for features in dataloader:
            features = features.to(device)
            pred = model(features)
            preds.extend(pred.cpu().numpy().tolist())
    return preds

def check_beta_values(df):
    """
    Verify that all methylation values are valid beta values (between 0 and 1).
    """
    if not ((df >= 0).all().all() and (df <= 1).all().all()):
        raise ValueError("Input methylation matrix contains non-beta values (outside [0,1]).")

def check_missing(df):
    """
    Check if there are missing values in the dataframe.
    """
    if df.isnull().values.any():
        raise ValueError("Input matrix contains missing values. Please impute or remove them before analysis.")

def align_cpg_sites(methylation, cpg_path):
    """
    Align CpG sites between input data and model requirements.

    If certain CpG sites are missing, they are filled with 0.5 (neutral methylation value).
    """
    cpg = pd.read_csv(cpg_path)["cpg"].tolist()
    missing_cols = [m for m in cpg if m not in methylation.columns]
    methylation = pd.concat([methylation, pd.DataFrame(0.5, index=methylation.index,
                                                       columns=missing_cols)], axis=1).loc[:, cpg].copy()
    return methylation

def run_perseclock(methylation_path,  model_path, cpg_path='24516cpg.csv', device="cpu"):
    """
    Run the complete PerSEClock age prediction pipeline.

    Parameters
    ----------
    methylation_path : str
        Path to methylation beta-value matrix (.csv).
    model_path : str
        Path to pre-trained PerSEClock model weights (.pt).
    device : str
        Device for inference ('cpu' or 'cuda').
    Returns
    -------
    list
        Predicted biological ages.
    """
    # Step 1: Load data
    methylation = pd.read_csv(methylation_path, index_col=0) # Rows: CpG sites, Columns: Samples
    methylation = methylation.transpose() # Rows: Samples, Columns: CpG sites
    # Data checks and alignment
    check_missing(methylation)
    check_beta_values(methylation)
    # Align CpG sites
    methylation = align_cpg_sites(methylation, cpg_path)

    # Step 2: Prepare DataLoader
    X = methylation.values.astype("float32")

    # Create Dataset and DataLoader
    dataset = MethylationDataset(X)
    loader = DataLoader(dataset, batch_size=len(X), shuffle=False)

    # Step 3: Load model
    model = MLP(in_features=X.shape[1])
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)

    # Step 4: Predict
    pred_age = predict_age(model, loader, device)
    print(f"[INFO] Successfully predicted {len(pred_age)} samples.")

    return pred_age

def PerSEClock(file_path, method_dir=None):
    """
    PerSEClock methylation age prediction
    :param file_path: str, path to the methylation data file (CSV format)
    :param method_dir: str or None, path to the method directory, if None,
    use current directory
    :return: predicted ages as a numpy array
    """
    # change working directory if method_dir is provided
    if method_dir:
        original_dir = os.getcwd()
        os.chdir(method_dir)
    try:
        # get predicted ages
        pred_age = run_perseclock(
        methylation_path=file_path, # Input methylation beta-value matrix
        model_path="PerSE_model.pt",  # Pre-trained model path
        cpg_path='24516cpg.csv', # CpG sites file path
        )
        return pred_age
    
    finally:
        # Restore original working directory
        if method_dir:
            os.chdir(original_dir)


if __name__ == '__main__':
    # If this script is run directly, perform testing
    import sys
    if len(sys.argv) > 1:
        dataset_path = sys.argv[1]
        method_dir = sys.argv[2] if len(sys.argv) > 2 else None
        result = PerSEClock(dataset_path, method_dir)
        print("Results:", result)
    else:
        print("Usage: python PerSEClock.py <dataset_path> [method_dir]")