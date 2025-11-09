from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
from typing import Dict, Any
import json
import time

class BaseClock(ABC):
    """
    Base class for methylation clocks - all clock methods should inherit from this class.
    """
    
    def __init__(self, method_name: str):
        self.method_name = method_name
        self.method_path = Path(__file__).parent.parent / "clocks" / method_name
    
    @abstractmethod
    def predict(self, input_file: str) -> pd.DataFrame:
        """
        Predict ages based on the input methylation data file.
        Should be implemented by all subclasses.
        """
        pass
    
    def save_results(self, results: pd.DataFrame, dataset_id: str, 
                    true_ages: list, metadata: Dict[str, Any], 
                    execution_time: float) -> str:
        """
        Save the prediction results to a JSON file.
        Args:
            results (pd.DataFrame): DataFrame containing prediction results.
            dataset_id (str): Identifier for the dataset.
            true_ages (list): List of true ages for the samples.
            metadata (Dict[str, Any]): Metadata associated with the samples.
            execution_time (float): Time taken to execute the prediction.
        Returns:
            str: Path to the saved JSON file.
        """
        from config.settings import OUTPUT_DIR
        
        OUTPUT_DIR.mkdir(exist_ok=True)
        
        # Construct age data dictionary
        age_data = {
            "FileName": f"{dataset_id}_predicted_by_{self.method_name}.json",
            "datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "Algorithm": self.method_name,
            "Dataset": dataset_id,
            "AgeRange": [min(true_ages), max(true_ages)],
            "SampleNum": len(results),
            "ConsumeTime(Min)": f"{execution_time:.3f}s",
            "ID_REF": metadata.get('ID', []),
            "Age_unit": 'Year',
            "Tissue": metadata.get('Tissue', []),
            "Condition": metadata.get('Condition', []),
            "Disease": metadata.get('Disease', []),
            "Gender": metadata.get('Gender', []),
            "Race": metadata.get('Race', []),
            "Platform": metadata.get('Platform', 'Unknown'),
            "PredAge": results['predicted_age'].tolist(),
            "TrueAge": true_ages
        }
        
        # Save to JSON file
        output_file = OUTPUT_DIR / f"{dataset_id}_predicted_by_{self.method_name}.json"
        with open(output_file, 'w') as f:
            json.dump(age_data, f, indent=4)
        
        return str(output_file)