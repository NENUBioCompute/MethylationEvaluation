import argparse
import sys
from pathlib import Path

from core.clock_manager import clock_manager
from interfaces.api import DNAmClockAPI

def main():
    """
    Command-line interface for DNAm Clock Tool.
    Allows users to predict biological age using specified methylation clock methods
    on given datasets, list available methods, and run batch evaluations.
    """
    parser = argparse.ArgumentParser(
        description='DNAm Clock Tool - Epigenetic Age Prediction',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--method', 
        required=True,
        help='Name of the DNAm clock method (e.g., HorvathAge, DNAmAgeSkinClock)'
    )
    
    parser.add_argument(
        '--dataset', 
        required=True,
        help='Dataset ID (e.g., GSE152026_4)'
    )
    
    parser.add_argument(
        '--list-methods', 
        action='store_true',
        help='List all available methods'
    )
    
    parser.add_argument(
        '--batch-evaluate',
        action='store_true',
        help='Run batch evaluation on configured datasets'
    )
    
    args = parser.parse_args()
    
    api = DNAmClockAPI()
    
    if args.list_methods:
        methods = api.list_available_methods()
        print("Available DNAm Clock Methods:")
        for method in methods:
            print(f"  - {method}")
        return
    
    if args.batch_evaluate:
        # Run batch evaluation
        from config.settings import EVALUATION_DATASETS
        methods = [args.method] if args.method != 'all' else api.list_available_methods()
        
        print(f"Starting batch evaluation with {len(methods)} methods on {len(EVALUATION_DATASETS)} datasets")
        results = api.batch_evaluate(methods, EVALUATION_DATASETS)
        print("Batch evaluation completed !")
        return
    
    try:
        # Run single method prediction
        results, exec_time = api.predict_age(
            method_name=args.method,
            dataset_id=args.dataset
        )
        
        print(f"Prediction completed successfully in {exec_time:.3f}s!")
        print(f"Dataset: {args.dataset}")
        print(f"Method: {args.method}")
        print(f"Number of samples: {len(results)}")
        print(f"Predicted ages: {results['predicted_age'].tolist()}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()