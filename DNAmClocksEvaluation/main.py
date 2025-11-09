#!/usr/bin/env python3
"""
DNAm Clock Tool Main Entry Point
Provides command-line interface for single method prediction, batch evaluation, and listing available methods.
"""

import argparse
from interfaces.api import api
from config.settings import EVALUATION_DATASETS

def main():
    parser = argparse.ArgumentParser(description='DNAm Clock Tool')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Single method prediction command
    predict_parser = subparsers.add_parser('predict', help='Single method prediction')
    predict_parser.add_argument('--method', required=True, help='Method name')
    predict_parser.add_argument('--dataset', required=True, help='Dataset ID')
    
    # Batch evaluation command
    batch_parser = subparsers.add_parser('batch', help='Batch evaluation')
    batch_parser.add_argument('--methods', nargs='+', help='Method names (default: all methods)')
    batch_parser.add_argument('--datasets', nargs='+', help='Dataset IDs (default: configured datasets)')
    
    # List available methods command
    subparsers.add_parser('list-methods', help='List all available methods')
    
    args = parser.parse_args()
    
    if args.command == 'predict':
        results, exec_time = api.predict_age(args.method, args.dataset)
        print(f"Prediction completed in {exec_time:.3f}s: {results}")
        
    elif args.command == 'batch':
        methods = args.methods if args.methods else api.list_available_methods()
        datasets = args.datasets if args.datasets else EVALUATION_DATASETS
        
        print(f"Starting batch evaluation with {len(methods)} methods on {len(datasets)} datasets")
        results = api.batch_evaluate(methods, datasets)
        print("Batch evaluation completed !")
         
    elif args.command == 'list-methods':
        methods = api.list_available_methods()
        print("Available methods:")
        for method in methods:
            print(f"  - {method}")
            
    else:
        parser.print_help()

if __name__ == "__main__":
    main()