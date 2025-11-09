import pandas as pd
import time
import importlib
from pathlib import Path
import sys
import os
from .base_clock import BaseClock

class PythonClockBase(BaseClock):
    """
    Base class for Python-based methylation clocks.
    """
    
    def predict(self, dataset_path: str) -> pd.DataFrame:
        """
        Predict ages using the specified Python methylation clock method.
        Args:
            dataset_path (str): Path to the input methylation data file.
        Returns:
            pd.DataFrame: DataFrame containing predicted ages.
        """
        # Check dataset file existence
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset file not found: {dataset_path}")

        # Convert paths to absolute paths
        dataset_path = os.path.abspath(dataset_path)
        method_dir = os.path.abspath(self.method_path)

        try:
            # Dynamically import the method module
            module_name = f"clocks.{self.method_name}.{self.method_name}"
            
            # Ensure the clocks directory is in sys.path
            clocks_path = Path(__file__).parent.parent / "clocks"
            if str(clocks_path) not in sys.path:
                sys.path.insert(0, str(clocks_path))
            
            module = importlib.import_module(module_name)

            # Python function name is the same as the method name
            function_name = self.method_name
            
            if not hasattr(module, function_name):
                raise AttributeError(f"Python function '{function_name}' not found in module")
     
            start_time = time.time()
            # Try calling the function with different parameter options
            try:
                # Option 1: Pass two arguments (dataset path + method directory)
                pred_age = getattr(module, function_name)(dataset_path, method_dir)
            except TypeError as e:
                # If the function does not accept two arguments, try passing only the dataset path
                if "takes 1 positional argument but 2 were given" in str(e):
                    pred_age = getattr(module, function_name)(dataset_path)
                else:
                    raise e
            execution_time = time.time() - start_time

            # Convert results to DataFrame
            results = pd.DataFrame({
                'predicted_age': list(pred_age)
            })
            
            return results, execution_time
            
        except ImportError as e:
            raise ImportError(f"Failed to import module for {self.method_name}: {e}")
        except Exception as e:
            raise RuntimeError(f"Error during prediction with {self.method_name}: {e}")