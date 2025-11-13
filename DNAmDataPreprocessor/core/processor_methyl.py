import os
import pandas as pd
import numpy as np
import glob
import subprocess
from typing import Optional, Tuple, List, Union
import logging

class DNAMethylationNormalizer:
    """
    DNA Methylation Expression Matrix Normalization Class
    
    This class provides a step-by-step normalization pipeline for DNA methylation data.
    The imputation step (Step 2) uses a standalone R script to avoid Python-R data type conversion issues.
    
    Three main steps:
    1. Beta value conversion and validation (Python)
    2. Missing value imputation using methyLImp2 (Standalone R script)
    3. Sample filtering based on phenotype information (Python)
    
    Each step reads from and writes to the output_path, creating a processing pipeline.
    """
    
    def __init__(self, expression_path: str, pheno_path: str, output_path: str):
        """
        Initialize the methylation data normalizer
        
        Parameters:
        -----------
        expression_path : str
            Directory path containing expression matrix files with '_beta.csv.gz' suffix
        pheno_path : str
            Directory path containing phenotype files with '_pheno.csv' suffix  
        output_path : str
            Directory path where processed files will be saved at each step
        """
        self.expression_path = expression_path
        self.pheno_path = pheno_path
        self.output_path = output_path
        self.logger = self._setup_logger()
        self.r_script_path = os.path.join(os.path.dirname(__file__), 'impute_methylation.R')
        
    def _setup_logger(self) -> logging.Logger:
        """
        Configure logging system for tracking processing steps and debugging
        
        Returns:
        --------
        logging.Logger
            Configured logger instance for the class
        """
        logger = logging.getLogger('DNAMethylationNormalizer')
        logger.setLevel(logging.INFO)
        
        # Prevent duplicate log handlers in case of multiple instances
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def validate_data_types(self, matrix: pd.DataFrame) -> pd.DataFrame:
        """
        Ensure all data in the matrix is numeric for proper processing
        
        Parameters:
        -----------
        matrix : pd.DataFrame
            Input methylation data matrix
            
        Returns:
        --------
        pd.DataFrame
            Matrix with all values converted to numeric data types
        """
        self.logger.info("Validating and converting data types to numeric...")
        
        # Convert all data to numeric, coercing errors to NaN
        numeric_matrix = matrix.apply(pd.to_numeric, errors='coerce')
        
        # Check if any non-numeric values were converted to NaN
        conversion_na_count = numeric_matrix.isna().sum().sum() - matrix.isna().sum().sum()
        
        if conversion_na_count > 0:
            self.logger.warning(
                f"Converted {conversion_na_count} non-numeric values to NaN during type conversion"
            )
        
        self.logger.info("Data type validation completed successfully")
        return numeric_matrix
    
    def is_beta_value(self, matrix: pd.DataFrame) -> bool:
        """
        Determine if matrix values represent valid beta values (0 to 1 range)
        
        Parameters:
        -----------
        matrix : pd.DataFrame
            Methylation data matrix to validate
            
        Returns:
        --------
        bool
            True if values are within acceptable beta range, False otherwise
        """
        # Use random sampling for efficiency with large datasets
        values = matrix.values.flatten()
        sample_size = min(10000, len(values))
        sampled_values = np.random.choice(values, size=sample_size, replace=False)
        
        # Remove NaN values from sampling to avoid skewing results
        sampled_values = sampled_values[~np.isnan(sampled_values)]
        
        if len(sampled_values) == 0:
            self.logger.warning("No valid numeric values found for beta validation")
            return False
        
        # Check if values are within beta range with small tolerance for precision errors
        is_beta = np.all((sampled_values >= -0.001) & (sampled_values <= 1.001))
        
        beta_info = f"Beta validation: {is_beta}, Value range: [{sampled_values.min():.3f}, {sampled_values.max():.3f}]"
        self.logger.info(beta_info)
        
        return is_beta
    
    def step1_convert_to_beta(self, overwrite: bool = True) -> dict:
        """
        STEP 1: Convert raw methylation values to beta values and save to output_path
        
        Parameters:
        -----------
        overwrite : bool, default=False
            If True, overwrite existing files in output_path. If False, skip files that already exist.
            
        Returns:
        --------
        dict
            Processing statistics for step 1
        """
        self.logger.info("Starting STEP 1: Beta value conversion")
        
        # Ensure output directory exists
        os.makedirs(self.output_path, exist_ok=True)
        
        # Find all expression matrix files
        expression_pattern = os.path.join(self.expression_path, "*_beta.csv.gz")
        expression_files = glob.glob(expression_pattern)
        
        self.logger.info(f"Found {len(expression_files)} expression files for beta conversion")
        
        if not expression_files:
            self.logger.warning("No expression files found matching pattern")
            return {}
        
        # Initialize results tracking
        processing_results = {
            'total_files': len(expression_files),
            'converted': 0,
            'already_beta': 0,
            'skipped': 0,
            'failed': 0,
            'failed_files': []
        }
        
        # Process each expression file
        for expr_file in expression_files:
            try:
                # Determine output filename
                output_filename = os.path.basename(expr_file)
                output_path = os.path.join(self.output_path, output_filename)
                
                # Skip if file exists and overwrite is False
                if os.path.exists(output_path) and not overwrite:
                    self.logger.info(f"Skipping {expr_file} - output already exists")
                    processing_results['skipped'] += 1
                    continue
                
                self.logger.info(f"Processing {expr_file} for beta conversion")
                
                # Load expression matrix
                expression_matrix = pd.read_csv(expr_file, index_col=0)
                self.logger.info(f"Loaded expression matrix: {expression_matrix.shape}")
                
                # Validate and ensure numeric data types
                expression_matrix = self.validate_data_types(expression_matrix)
                
                # Check if conversion is needed
                if not self.is_beta_value(expression_matrix):
                    self.logger.info("Converting intensity values to beta values")
                    
                    # Create a copy for conversion
                    beta_matrix = expression_matrix.copy()
                    
                    # Apply beta conversion to each sample
                    for sample in expression_matrix.columns:
                        try:
                            # PLACEHOLDER: Replace with your actual conversion logic
                            # Beta = Methylated / (Methylated + Unmethylated + 100)
                            current_values = expression_matrix[sample]
                            beta_values = current_values / (current_values + 100)  # Simplified
                            
                            # Ensure values stay within valid beta range
                            beta_values = np.clip(beta_values, 0.0, 1.0)
                            beta_matrix[sample] = beta_values
                            
                        except Exception as e:
                            self.logger.warning(f"Beta conversion failed for sample {sample}: {e}")
                            continue
                    
                    # Save converted matrix
                    beta_matrix.to_csv(output_path, compression='gzip')
                    processing_results['converted'] += 1
                    self.logger.info(f"Beta conversion completed. Saved to: {output_path}")
                    
                else:
                    # File already contains beta values, just copy to output
                    expression_matrix.to_csv(output_path, compression='gzip')
                    processing_results['already_beta'] += 1
                    self.logger.info(f"File already contains beta values. Copied to: {output_path}")
                
            except Exception as e:
                self.logger.error(f"Beta conversion failed for {expr_file}: {e}")
                processing_results['failed'] += 1
                processing_results['failed_files'].append(expr_file)
        
        # Log step 1 summary
        self.logger.info(
            f"STEP 1 completed. Converted: {processing_results['converted']}, "
            f"Already beta: {processing_results['already_beta']}, "
            f"Skipped: {processing_results['skipped']}, "
            f"Failed: {processing_results['failed']}"
        )
        
        return processing_results
    
    def step2_impute_missing_values(self, overwrite: bool = True) -> dict:
        """
        STEP 2: Impute missing values using standalone R script
        
        This step calls a standalone R script that handles all data reading,
        processing with methyLImp2, and writing within the R environment.
        
        Parameters:
        -----------
        overwrite : bool, default=False
            If True, overwrite existing imputed files. If False, skip files that already have imputed versions.
            
        Returns:
        --------
        dict
            Processing statistics for step 2
        """
        self.logger.info("Starting STEP 2: Missing value imputation using standalone R script")
        
        # Ensure output directory exists
        os.makedirs(self.output_path, exist_ok=True)
        
        # Find all files in output path (from step 1)
        output_pattern = os.path.join(self.output_path, "*_beta.csv.gz")
        output_files = glob.glob(output_pattern)
        
        self.logger.info(f"Found {len(output_files)} files for imputation")
        
        if not output_files:
            self.logger.warning("No files found in output path for imputation")
            return {}
        
        # Initialize results tracking
        processing_results = {
            'total_files': len(output_files),
            'imputed': 0,
            'skipped': 0,
            'failed': 0,
            'failed_files': []
        }
        
        # Process each file
        for file_path in output_files:
            try:
                # For imputation, we'll overwrite the same file
                output_path = file_path  # Overwrite the input file
                
                # Skip if we're not overwriting and we want to check for already processed files
                if not overwrite:
                    # Simple check - in practice you might want a more robust approach
                    self.logger.info(f"Processing {file_path} for imputation")
                
                # Check if file has missing values before calling R script
                matrix = pd.read_csv(file_path, index_col=0)
                missing_count = matrix.isnull().sum().sum()
                
                if missing_count == 0:
                    self.logger.info(f"No missing values in {file_path} - skipping imputation")
                    processing_results['skipped'] += 1
                    continue
                
                self.logger.info(f"Found {missing_count} missing values in {file_path}, starting R imputation")
                
                # Call standalone R script for imputation
                success = self._call_r_imputation_script(file_path, output_path)
                
                if success:
                    processing_results['imputed'] += 1
                    self.logger.info(f"R imputation completed successfully for {file_path}")
                else:
                    processing_results['failed'] += 1
                    processing_results['failed_files'].append(file_path)
                    self.logger.error(f"R imputation failed for {file_path}")
                
            except Exception as e:
                self.logger.error(f"Imputation failed for {file_path}: {e}")
                processing_results['failed'] += 1
                processing_results['failed_files'].append(file_path)
        
        # Log step 2 summary
        self.logger.info(
            f"STEP 2 completed. Imputed: {processing_results['imputed']}, "
            f"Skipped: {processing_results['skipped']}, "
            f"Failed: {processing_results['failed']}"
        )
        
        return processing_results
    
    def _call_r_imputation_script(self, input_file: str, output_file: str) -> bool:
        """
        Call the standalone R script for methylation data imputation
        
        Parameters:
        -----------
        input_file : str
            Path to input file with missing values
        output_file : str
            Path where imputed file should be saved
            
        Returns:
        --------
        bool
            True if imputation successful, False otherwise
        """
        try:
            # Build command to call R script
            cmd = [
                'Rscript',
                '--verbose',  # Add verbose flag for better debugging
                self.r_script_path,
                input_file,
                output_file
            ]
            
            self.logger.info(f"Executing optimized R command: {' '.join(cmd)}")
            
            # Execute R script with timeout (2 hours)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,  # Don't raise exception on non-zero return code
                timeout=7200  # 2 hour timeout
            )
            
            # Log R script output
            if result.stdout:
                # Parse and log important information from R output
                for line in result.stdout.split('\n'):
                    if any(keyword in line for keyword in ['===', 'Error', 'Warning', 'Completed', 'probes', 'missing values']):
                        self.logger.info(f"R output: {line}")
            
            if result.stderr:
                self.logger.warning(f"R script stderr: {result.stderr}")
            
            if result.returncode == 0:
                self.logger.info(f"R script completed successfully with return code: {result.returncode}")
                
                # Verify the output file was created and has reasonable size
                if os.path.exists(output_file) and os.path.getsize(output_file) > 1000:
                    return True
                else:
                    self.logger.error(f"Output file verification failed: {output_file}")
                    return False
            else:
                self.logger.error(f"R script failed with return code: {result.returncode}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"R script timed out after 2 hours for file: {input_file}")
            return False
        except Exception as e:
            self.logger.error(f"Error calling R script: {e}")
            return False
    
    def step3_filter_samples(self, overwrite: bool = True) -> dict:
        """
        STEP 3: Filter samples based on phenotype data and save to output_path
        
        This step reads all files from output_path (created in step 2), filters
        samples based on phenotype information (using 'Age' column), and overwrites
        the files in output_path with the filtered results.
        
        Parameters:
        -----------
        overwrite : bool, default=False
            If True, overwrite existing filtered files. If False, skip files that already have filtered versions.
            
        Returns:
        --------
        dict
            Processing statistics for step 3
        """
        self.logger.info("Starting STEP 3: Sample filtering based on phenotype data")
        
        # Ensure output directory exists
        os.makedirs(self.output_path, exist_ok=True)
        
        # Find all files in output path (from step 2)
        output_pattern = os.path.join(self.output_path, "*_beta.csv.gz")
        output_files = glob.glob(output_pattern)
        
        self.logger.info(f"Found {len(output_files)} files for sample filtering")
        
        if not output_files:
            self.logger.warning("No files found in output path for filtering")
            return {}
        
        # Initialize results tracking
        processing_results = {
            'total_files': len(output_files),
            'filtered': 0,
            'skipped': 0,
            'failed': 0,
            'failed_files': []
        }
        
        # Process each file
        for file_path in output_files:
            try:
                # Determine corresponding phenotype file
                base_name = os.path.basename(file_path).replace('_beta.csv.gz', '')
                pheno_file = os.path.join(self.pheno_path, f"{base_name}_pheno.csv")
                
                # Check if phenotype file exists
                if not os.path.exists(pheno_file):
                    self.logger.warning(f"Phenotype file not found: {pheno_file}")
                    processing_results['failed'] += 1
                    processing_results['failed_files'].append(file_path)
                    continue
                
                # For filtering, we'll overwrite the same file
                output_path = file_path  # Overwrite the input file
                
                # Skip if we're not overwriting and the file already has "_filtered" in name
                if not overwrite and "_filtered" in file_path:
                    self.logger.info(f"Skipping {file_path} - already filtered")
                    processing_results['skipped'] += 1
                    continue
                
                self.logger.info(f"Processing {file_path} for sample filtering")
                
                # Load expression matrix
                expression_matrix = pd.read_csv(file_path, index_col=0)
                self.logger.info(f"Loaded expression matrix: {expression_matrix.shape}")
                
                # Load phenotype data
                pheno_data = pd.read_csv(pheno_file)
                self.logger.info(f"Loaded phenotype data: {pheno_data.shape}")
                
                # Validate required columns exist - NOTE: Using 'Age' (capital A)
                required_cols = ['SampleID', 'Age']
                missing_cols = [col for col in required_cols if col not in pheno_data.columns]
                
                if missing_cols:
                    error_msg = f"Phenotype file missing required columns: {missing_cols}"
                    self.logger.error(error_msg)
                    # Provide helpful suggestion if lowercase 'age' exists
                    if 'age' in pheno_data.columns and 'Age' in missing_cols:
                        self.logger.info("Found 'age' column (lowercase) but expected 'Age' (capital A)")
                    processing_results['failed'] += 1
                    processing_results['failed_files'].append(file_path)
                    continue
                
                # Identify samples with valid (non-null) Age values
                valid_samples = pheno_data[pheno_data['Age'].notna()]['SampleID'].tolist()
                self.logger.info(f"Found {len(valid_samples)} samples with valid Age values")
                
                if not valid_samples:
                    self.logger.warning("No samples with valid Age values found")
                    processing_results['failed'] += 1
                    processing_results['failed_files'].append(file_path)
                    continue
                
                # Find intersection between expression matrix and valid phenotype samples
                expression_samples = set(expression_matrix.columns)
                valid_sample_set = set(valid_samples)
                common_samples = expression_samples & valid_sample_set
                
                self.logger.info(
                    f"Sample overlap - Expression: {len(expression_samples)}, "
                    f"Phenotype: {len(valid_sample_set)}, Common: {len(common_samples)}"
                )
                
                if not common_samples:
                    self.logger.error("No overlapping samples found between datasets")
                    processing_results['failed'] += 1
                    processing_results['failed_files'].append(file_path)
                    continue
                
                # Filter matrix to include only common samples
                filtered_matrix = expression_matrix[list(common_samples)]
                
                self.logger.info(
                    f"Sample filtering completed. Original: {expression_matrix.shape}, "
                    f"Filtered: {filtered_matrix.shape}"
                )
                
                # Save filtered matrix (overwriting original)
                filtered_matrix.to_csv(output_path, compression='gzip')
                processing_results['filtered'] += 1
                self.logger.info(f"Sample filtering completed. Saved to: {output_path}")
                
            except Exception as e:
                self.logger.error(f"Sample filtering failed for {file_path}: {e}")
                processing_results['failed'] += 1
                processing_results['failed_files'].append(file_path)
        
        # Log step 3 summary
        self.logger.info(
            f"STEP 3 completed. Filtered: {processing_results['filtered']}, "
            f"Skipped: {processing_results['skipped']}, "
            f"Failed: {processing_results['failed']}"
        )
        
        return processing_results
    
    def run_full_pipeline(self, overwrite: bool = False) -> dict:
        """
        Execute the complete three-step normalization pipeline
        
        This method runs all three steps sequentially, with each step reading from
        and writing to the output_path. Step 2 uses a standalone R script to avoid
        Python-R data conversion issues.
        
        Parameters:
        -----------
        overwrite : bool, default=False
            If True, overwrite existing files at each step. If False, skip steps for files that already exist.
            
        Returns:
        --------
        dict
            Comprehensive processing statistics for all three steps
        """
        self.logger.info("Starting complete three-step normalization pipeline")
        
        # Run each step sequentially
        step1_results = self.step1_convert_to_beta(overwrite=overwrite)
        step2_results = self.step2_impute_missing_values(overwrite=overwrite)
        step3_results = self.step3_filter_samples(overwrite=overwrite)
        
        # Combine results
        pipeline_results = {
            'step1_beta_conversion': step1_results,
            'step2_imputation': step2_results,
            'step3_sample_filtering': step3_results
        }
        
        # Calculate overall success rate
        total_files = step1_results.get('total_files', 0)
        successful_files = total_files - (
            step1_results.get('failed', 0) + 
            step2_results.get('failed', 0) + 
            step3_results.get('failed', 0)
        )
        
        if total_files > 0:
            success_rate = (successful_files / total_files) * 100
        else:
            success_rate = 0
        
        self.logger.info(
            f"Complete pipeline finished. Overall success rate: {success_rate:.1f}% "
            f"({successful_files}/{total_files} files processed successfully)"
        )
        
        return pipeline_results


if __name__ == "__main__":
    """
    Demonstration of the step-by-step DNA methylation normalization pipeline
    with standalone R script for imputation
    """
    # Initialize the normalizer
    normalizer = DNAMethylationNormalizer(
        expression_path="../data/parsed/methyl",       # Input DNA methylation matrix files
        pheno_path="../data/standardized/pheno",       # Input phenotype files
        output_path="../data/standardized/methyl"      # Output directory
    )
    
    # Option 1: Run individual steps
    # step1_results = normalizer.step1_convert_to_beta(overwrite=True)
    # step2_results = normalizer.step2_impute_missing_values(overwrite=True)
    # step3_results = normalizer.step3_filter_samples(overwrite=True)
    
    # Option 2: Run complete pipeline (recommended)
    pipeline_results = normalizer.run_full_pipeline(overwrite=True)
    
    # Display processing summary
    print("\n" + "="*60)
    print("DNA METHYLATION NORMALIZATION PIPELINE - COMPLETE SUMMARY")
    print("="*60)
    
    for step_name, results in pipeline_results.items():
        print(f"\n{step_name.upper().replace('_', ' ')}:")
        print(f"  Total files: {results.get('total_files', 0)}")
        
        if 'converted' in results:
            print(f"  Converted to beta: {results.get('converted', 0)}")
        if 'already_beta' in results:
            print(f"  Already beta: {results.get('already_beta', 0)}")
        if 'imputed' in results:
            print(f"  Imputed: {results.get('imputed', 0)}")
        if 'filtered' in results:
            print(f"  Filtered: {results.get('filtered', 0)}")
        
        print(f"  Skipped: {results.get('skipped', 0)}")
        print(f"  Failed: {results.get('failed', 0)}")
        
        if results.get('failed_files'):
            print(f"  Failed files: {len(results['failed_files'])}")
