import pandas as pd
from pathlib import Path
from typing import Union, Dict, Any

class DataLoader:
    """
    Utility class for loading methylation data from various file formats.
    """
    
    def __init__(self):
        self.supported_formats = ['.csv', '.tsv', '.txt', '.xlsx', '.xls']
    
    def load(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Load methylation data from a file.
        Args:
            file_path (str or Path): Path to the input data file.
        Returns:
            pd.DataFrame: Loaded methylation data.
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")
        
        suffix = file_path.suffix.lower()
        
        try:
            if suffix == '.csv':
                return pd.read_csv(file_path)
            elif suffix in ['.tsv', '.txt']:
                return pd.read_csv(file_path, sep='\t')
            elif suffix in ['.xlsx', '.xls']:
                return pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {suffix}. Supported formats: {self.supported_formats}")
        except Exception as e:
            raise ValueError(f"Failed to load file {file_path}: {e}")
    
    def validate_dnam_data(self, data: pd.DataFrame) -> bool:
        """
        Validate the structure of the methylation data.
        Args:
            data (pd.DataFrame): Methylation data to validate.
        Returns:
            bool: True if valid, raises ValueError otherwise.
        """
        # Check basic structure
        if data.empty:
            raise ValueError("Input data is empty")

        # Check for CpG probe columns (assuming they start with 'cg')
        cg_columns = [col for col in data.columns if col.startswith('cg')]
        if not cg_columns:
            raise ValueError("No CpG probe columns found (columns should start with 'cg')")
        
        return True