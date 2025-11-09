import pandas as pd
from typing import List, Dict, Any, Tuple

from core.clock_manager import clock_manager
from utils.data_processor import DataProcessor

class DNAmClockAPI:
    """
    API class for DNA methylation clock evaluation and prediction.
    """
    
    def __init__(self):
        self.manager = clock_manager
        self.data_processor = DataProcessor()
    
    def list_available_methods(self) -> List[str]:
        """List all available clock methods.
        """
        return self.manager.list_methods()
    
    def predict_age(self, method_name: str, dataset_id: str) -> Tuple[pd.DataFrame, float]:
        """
        Predict biological age using the specified method.
        
        Parameters:
        -----------
        method_name : str
            Clock method name (e.g., 'HorvathAge')
        dataset_id : str
            Dataset identifier
        Returns:
        --------
        tuple
            (Prediction results DataFrame, Execution time)
        """
        # get dataset path
        dataset_path = self.data_processor.get_dataset_path(dataset_id)

        # get clock instance 
        clock = self.manager.get_clock(method_name)
        results, exec_time = clock.predict(dataset_path)
        
        return results, exec_time
    
    def evaluate_method_on_dataset(self, method_name: str, dataset_id: str) -> Dict[str, Any]:
        """
        Evaluate method on a specific dataset.
        
        Parameters:
        -----------
        method_name : str
            Method name
        dataset_id : str
            Dataset identifier
        Returns:
        --------
        dict
            Evaluation results
        """
        try:
            # Get dataset path
            dataset_path = self.data_processor.get_dataset_path(dataset_id)
            print(f"Evaluating method: {method_name} on dataset: {dataset_path}")
            # Load true ages and metadata
            y_true, metadata = self.data_processor.load_dataset_metadata(dataset_id)
            # Get clock instance
            clock = self.manager.get_clock(method_name)
            pred_results, exec_time = clock.predict(dataset_path)
            # Save results
            output_file = clock.save_results(
                pred_results, dataset_id, y_true, metadata, exec_time
            )            
            return {
                'success': True,
                'output_file': output_file,
                'execution_time': exec_time,
                'dataset_id': dataset_id,
                'method_name': method_name,
                'num_samples': len(pred_results)
            }                
        except Exception as e:
            print(f"Evaluation failed: {method_name} on {dataset_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'dataset_id': dataset_id,
                'method_name': method_name
            }
    
    def batch_evaluate(self, method_list: List[str], dataset_list: List[str] = None) -> Dict[str, Any]:
        """
        Batch evaluate multiple methods and datasets.
        
        Parameters:
        -----------
        method_list : list
            List of method names
        dataset_list : list, optional
            List of dataset identifiers (default uses all evaluation datasets)
        Returns:
        --------
        dict
            Evaluation results summary
        """
        from config.settings import EVALUATION_DATASETS
        
        if dataset_list is None:
            dataset_list = EVALUATION_DATASETS
        
        results = {}
        for method_name in method_list:
            results[method_name] = {}
            for dataset in dataset_list:
                dataset_id = dataset.split('.')[0].replace('_beta', '')
                result = self.evaluate_method_on_dataset(method_name, dataset_id)
                results[method_name][dataset_id] = result
        
        return results

# Create global API instance
api = DNAmClockAPI()