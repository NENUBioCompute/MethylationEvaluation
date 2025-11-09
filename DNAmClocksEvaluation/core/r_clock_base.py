import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import time
import os
from .base_clock import BaseClock

class RClockBase(BaseClock):
    """
    Base class for R-based methylation clocks.
    """
    
    def __init__(self, method_name: str):
        super().__init__(method_name)
        # Ensure the data.table package is available
        try:
            self.table = importr('data.table')
        except Exception as e:
            print(f"Warning: Could not import data.table: {e}")
    
    def predict(self, dataset_path: str):
        """Execute R method prediction - fix internal file path issues
        Args:
            dataset_path (str): Path to the input methylation data file.
        Returns:
            pd.DataFrame: DataFrame containing prediction results.
            float: Execution time in seconds.
        """
        # Construct R script path
        r_script_path = self.method_path / f"{self.method_name}.R" 
        
        if not r_script_path.exists():
            raise FileNotFoundError(f"R script not found: {r_script_path}")
        
        # Check dataset file existence
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset file not found: {dataset_path}")

        # Convert paths to absolute paths
        dataset_path = os.path.abspath(dataset_path)
        r_script_path = os.path.abspath(r_script_path)
        method_dir = os.path.abspath(self.method_path)
        
        # Loading R script
        try:
            robjects.r.source(str(r_script_path))
        except Exception as e:
            raise RuntimeError(f"Failed to source R script: {e}")
        
        # Call the R function
        r_function_name = self.method_name
        if not hasattr(robjects.r, r_function_name):
            raise AttributeError(f"R function '{r_function_name}' not found in loaded script")
          
        # Execute R function and measure time
        start_time = time.time()
        try:
            # Convert paths to R-compatible format
            dataset_path_r = dataset_path.replace('\\', '/')
            method_dir_r = method_dir.replace('\\', '/')
            # Call the R function
            pred_age = getattr(robjects.r, r_function_name)(dataset_path_r, method_dir_r)
            execution_time = time.time() - start_time
        except Exception as e:
            raise RuntimeError(f"R function execution failed: {e}")
        
        # Convert results to DataFrame
        results = pd.DataFrame({
            'predicted_age': list(pred_age)
        })
        
        return results, execution_time