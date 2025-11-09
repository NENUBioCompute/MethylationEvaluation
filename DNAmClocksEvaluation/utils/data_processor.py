import pandas as pd
import json
from pathlib import Path
from typing import Tuple, Dict, Any
import numpy as np
import os
from config.settings import BETA_DIR, META_DIR


class DataProcessor:
    """
    Data processor for handling methylation datasets and metadata.
    """
    
    def load_dataset_metadata(self, dataset_id: str) -> Tuple[list, Dict[str, Any]]:
        """
        Load dataset metadata and true ages.

        Args:
            dataset_id (str): The ID of the dataset.

        Returns:
            Tuple[list, Dict[str, Any]]: A tuple containing the true ages and metadata.
        """
        # Construct possible phenotype file paths
        base_dataset_id = dataset_id.split('_')[0].replace('_beta', '')
        pheno_file = META_DIR / f'{base_dataset_id}_pheno.csv'
        
        if not pheno_file.exists():
            # Try other possible file name formats
            possible_pheno_files = [
                META_DIR / f'{dataset_id}_pheno.csv',
                META_DIR / f'{dataset_id.split("_")[0]}_pheno.csv',
                META_DIR / f'{base_dataset_id}_meta.csv',
            ]
            
            for file_path in possible_pheno_files:
                if file_path.exists():
                    pheno_file = file_path
                    break
            else:
                print(f"Warning: Metadata file not found: {base_dataset_id}_pheno.csv")
                return [], {}
        
        try:
            data_other = pd.read_csv(pheno_file)
            
            # determine true ages
            y_true = self._process_true_ages(data_other)
            
            # estimate platform
            platform = self._get_platform_from_dataset(dataset_id)
            
            # pack metadata
            metadata = {
                'ID': data_other['ID'].tolist() if 'ID' in data_other.columns else [],
                'Tissue': data_other['Tissue'].tolist() if 'Tissue' in data_other.columns else ['Unknown'] * len(data_other),
                'Condition': data_other['Condition'].tolist() if 'Condition' in data_other.columns else ['Unknown'] * len(data_other),
                'Disease': data_other['Disease'].tolist() if 'Disease' in data_other.columns else ['Unknown'] * len(data_other),
                'Gender': data_other['Gender'].tolist() if 'Gender' in data_other.columns else ['Unknown'] * len(data_other),
                'Race': data_other['Race'].tolist() if 'Race' in data_other.columns else ['Unknown'] * len(data_other),
                'Platform': platform
            }
            
            return y_true, metadata
            
        except Exception as e:
            print(f"Failed to load metadata: {e}")
            return [], {}
    
    def _process_true_ages(self, data_other: pd.DataFrame) -> list:
        """Process true age data
        Args:
            data_other (pd.DataFrame): Metadata DataFrame.
        Returns:
            list: List of true ages in years.
        """
        if 'Age_unit' not in data_other.columns or 'Age' not in data_other.columns:
            print("Warning: Missing age information")
            return []
        
        age_unit = data_other['Age_unit'].values[0]
        ages = data_other['Age'].astype('float64')
        
        if age_unit == 'Month':
            return (ages / 12).tolist()
        elif age_unit == 'Year':
            return ages.tolist()
        elif age_unit == 'Day':
            return (ages / 365).tolist()
        elif age_unit == 'Week':
            return (ages / 52).tolist()
        else:
            print(f"Warning: Unknown age unit '{age_unit}', assuming years")
            return ages.tolist()
    
    def _get_platform_from_dataset(self, dataset_id: str) -> str:
        """Estimate platform from dataset ID.
        Args:
            dataset_id (str): The ID of the dataset.
        Returns:
            str: Platform name.
        """
        return 'Unknown'  
    
    def get_dataset_path(self, dataset_id: str) -> str:
        """
        Access dataset file path by dataset ID.
        Args:
            dataset_id (str): The ID of the dataset.
        Returns:
            str: Path to the dataset file.
        """
        # construct data file name
        datafile = f"{dataset_id}"
        if not datafile.endswith('.csv'):
            datafile += '.csv'

        # locate file
        beta_file = BETA_DIR / datafile
        if not beta_file.exists():
            # Try other possible file name formats
            possible_beta_files = [
                BETA_DIR / f"{dataset_id}_beta.csv",
                BETA_DIR / f"{dataset_id}.csv.gz",
                BETA_DIR / f"{dataset_id}_beta.csv.gz",
            ]
            
            for file_path in possible_beta_files:
                if file_path.exists():
                    return str(file_path)
            raise FileNotFoundError(f"Failed to locate dataset file: {datafile}")
        return str(beta_file)