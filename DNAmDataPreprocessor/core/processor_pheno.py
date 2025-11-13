import os
import pandas as pd
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict

class PhenotypeStandardizer:
    """
    A class for standardizing DNA methylation phenotype files.
    Handles column name alignment and value standardization based on mapping files.
    """
    
    # Define the standard columns that need to be extracted and standardized
    STANDARD_COLUMNS = ['GEO_ID', 'SampleID', 'Tissue', 'Disease', 'Condition', 'Age', 'Age_unit', 'Gender', 'Race']
    
    def __init__(self, data_mapping_file: str, value_mapping_file: str, output_dir: str):
        """
        Initialize the PhenotypeStandardizer.
        
        Args:
            data_mapping_file (str): Path to DataMapping.xlsx file that maps column names
            value_mapping_file (str): Path to ValueMapping.xlsx file that standardizes values
            output_dir (str): Directory where standardized files will be saved
        """
        self.data_mapping_file = data_mapping_file
        self.value_mapping_file = value_mapping_file
        self.output_dir = Path(output_dir)
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize mapping dictionaries
        self.column_mapping_df = None
        self.value_mappings = {}
        
        # Setup logger
        self.logger = self._setup_logger()
        
        # Load mapping files
        self._load_mapping_files()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup and return logger instance"""
        logger = logging.getLogger('PhenotypeStandardizer')
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
    
    def _load_mapping_files(self) -> None:
        """
        Load both the column mapping and value mapping files.
        
        Raises:
            FileNotFoundError: If mapping files are not found
            Exception: If there are errors reading the files
        """
        try:
            # Load column mapping file (DataMapping_V3.xlsx)
            self.logger.info(f"Loading column mapping file: {self.data_mapping_file}")
            self.column_mapping_df = pd.read_excel(self.data_mapping_file)
            self.logger.info(f"Successfully loaded column mapping with {len(self.column_mapping_df)} datasets")
            
            # Load value mapping file (ValueMapping_V4.xlsx)
            self.logger.info(f"Loading value mapping file: {self.value_mapping_file}")
            value_mapping_sheets = ['Tissue', 'Disease', 'Condition', 'Age', 'Gender', 'Race']
            
            for sheet_name in value_mapping_sheets:
                try:
                    df = pd.read_excel(self.value_mapping_file, sheet_name=sheet_name)
                    self.value_mappings[sheet_name] = df
                    self.logger.info(f"Loaded {sheet_name} mapping with {len(df)} entries")
                except Exception as e:
                    self.logger.warning(f"Could not load sheet '{sheet_name}': {e}")
                    self.value_mappings[sheet_name] = pd.DataFrame()
            
        except FileNotFoundError as e:
            self.logger.error(f"Mapping file not found: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading mapping files: {e}")
            raise
    
    def get_dataset_mapping(self, geo_id: str) -> Dict[str, str]:
        """
        Get column mapping for a specific GEO dataset.
        
        Args:
            geo_id (str): GEO dataset identifier (e.g., 'GSE12345')
            
        Returns:
            Dict[str, str]: Mapping from standard column names to dataset-specific column names
            
        Raises:
            ValueError: If GEO_ID is not found in the mapping file
        """
        if self.column_mapping_df is None:
            raise ValueError("Column mapping dataframe is not loaded")
        
        # Find the row for this GEO_ID
        dataset_row = self.column_mapping_df[self.column_mapping_df['Original_metafile'].str.split('_').str[0] == geo_id]
        
        if dataset_row.empty:
            raise ValueError(f"GEO_ID '{geo_id}' not found in column mapping file")
        
        # Create mapping dictionary
        mapping = {}
        for standard_col in self.STANDARD_COLUMNS:  
            if standard_col in dataset_row.columns:
                dataset_specific_col = dataset_row[standard_col].iloc[0]
                if pd.notna(dataset_specific_col):
                    mapping[standard_col] = str(dataset_specific_col)
                else:
                    mapping[standard_col] = standard_col  # Use standard name if not specified
            else:
                mapping[standard_col] = standard_col
        
        self.logger.debug(f"Column mapping for {geo_id}: {mapping}")
        return mapping
    
    def get_value_mapping(self, geo_id: str, column: str) -> Dict[str, str]:
        """
        Get value mapping for a specific GEO dataset and column.
        
        Args:
            geo_id (str): GEO dataset identifier
            column (str): Column name to get value mapping for
            
        Returns:
            Dict[str, str]: Mapping from original values to standardized values
        """
        if column not in self.value_mappings:
            self.logger.warning(f"No value mapping available for column: {column}")
            return {}
        
        mapping_df = self.value_mappings[column]
        if mapping_df.empty:
            return {}
        
        # Filter mappings for this specific GEO_ID
        geo_mappings = mapping_df[mapping_df['GEO_ID'] == geo_id]
        
        if geo_mappings.empty:
            # Try to find generic mappings (without specific GEO_ID)
            geo_mappings = mapping_df[pd.isna(mapping_df['GEO_ID'])]
            if geo_mappings.empty:
                self.logger.debug(f"No value mapping found for {geo_id} - {column}")
                return {}
        
        # Create mapping dictionary
        value_map = {}
        for _, row in geo_mappings.iterrows():
            original_value = str(row['Unique Value']) if pd.notna(row['Unique Value']) else ''
            standardized_value = str(row[column]) if pd.notna(row[column]) else ''
            
            if original_value and standardized_value:
                value_map[original_value] = standardized_value
        
        self.logger.debug(f"Value mapping for {geo_id} - {column}: {len(value_map)} entries")
        return value_map
    
    def extract_columns(self, pheno_df: pd.DataFrame, column_mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Extract and align columns based on the column mapping.
        
        Args:
            pheno_df (pd.DataFrame): Original phenotype DataFrame
            column_mapping (Dict[str, str]): Mapping from standard to dataset-specific column names
            
        Returns:
            pd.DataFrame: DataFrame with standardized column names
        """
        standardized_df = pd.DataFrame()
        for standard_col, dataset_col in column_mapping.items():
            if dataset_col in pheno_df.columns:
                # Column exists in the original data
                standardized_df[standard_col] = pheno_df[dataset_col]
                self.logger.debug(f"Extracted column '{dataset_col}' as '{standard_col}'")
            else:
                # Column doesn't exist, use constant or None
                if dataset_col == standard_col:
                    standardized_df[standard_col] = None
                    self.logger.warning(f"Column '{dataset_col}' not found. Setting '{standard_col}' to None")
                else:
                    standardized_df[standard_col] = dataset_col
                    self.logger.warning(f"Column '{dataset_col}' not found. Using '{dataset_col}' as constant value for '{standard_col}'")
        
        return standardized_df
    
    def standardize_values(self, df: pd.DataFrame, geo_id: str) -> pd.DataFrame:
        """
        Standardize values in the DataFrame using value mappings.
        
        Args:
            df (pd.DataFrame): DataFrame with standardized column names but original values
            geo_id (str): GEO dataset identifier
            
        Returns:
            pd.DataFrame: DataFrame with standardized values
        """
        standardized_df = df.copy()
        
        for column in self.STANDARD_COLUMNS:
            if column == 'GEO_ID':
                continue  # Skip GEO_ID column
                
            if column in df.columns:
                value_mapping = self.get_value_mapping(geo_id, column)
                if value_mapping:
                    # Apply value mapping
                    standardized_df[column] = df[column].astype(str).map(
                        lambda x: value_mapping.get(x.strip(), x) if pd.notna(x) else x
                    )
                    self.logger.debug(f"Applied value mapping to {column}")
                else:
                    self.logger.debug(f"No value mapping available for {column}")
        
        return standardized_df
    
    def process_phenotype_file(self, pheno_file_path: str) -> Optional[pd.DataFrame]:
        """
        Process a single phenotype file and return standardized DataFrame.
        
        Args:
            pheno_file_path (str): Path to the phenotype file (_pheno.xlsx)
            
        Returns:
            Optional[pd.DataFrame]: Standardized DataFrame or None if processing fails
        """
        try:
            # Extract GEO_ID from filename (assuming format: GSE12345_pheno.xlsx)
            file_name = Path(pheno_file_path).stem
            geo_id = file_name.split('_')[0]
            
            self.logger.info(f"Processing phenotype file: {pheno_file_path} (GEO_ID: {geo_id})")
            
            # Read the phenotype file
            pheno_df = pd.read_excel(pheno_file_path)
            self.logger.info(f"Loaded phenotype data with shape: {pheno_df.shape}")
            
            # Get column mapping for this dataset
            column_mapping = self.get_dataset_mapping(geo_id)
            
            # Extract and align columns
            extracted_df = self.extract_columns(pheno_df, column_mapping)
            
            # Add GEO_ID column if not present
            if 'GEO_ID' not in extracted_df.columns:
                extracted_df['GEO_ID'] = geo_id
            
            # Standardize values
            standardized_df = self.standardize_values(extracted_df, geo_id)
            standardized_df['GEO_ID'] = geo_id  # Ensure GEO_ID column is correct
            
            # Ensure all standard columns are present
            for col in self.STANDARD_COLUMNS:
                if col not in standardized_df.columns:
                    standardized_df[col] = f"Missing_{col}"
            
            self.logger.info(f"Successfully standardized data. Final shape: {standardized_df.shape}")
            return standardized_df
            
        except Exception as e:
            self.logger.error(f"Error processing file {pheno_file_path}: {e}")
            return None
        
    def del_nan_age_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove rows where 'Age' is NaN.
        
        Args:
            df (pd.DataFrame): DataFrame to process 
        Returns:
            pd.DataFrame: DataFrame with NaN 'Age' rows removed
        """
        initial_count = df.shape[0]
        df_cleaned = df.dropna(subset=['Age'])
        final_count = df_cleaned.shape[0]
        self.logger.info(f"Removed {initial_count - final_count} rows with NaN 'Age'")
        return df_cleaned
    
    def save_standardized_data(self, df: pd.DataFrame, geo_id: str) -> str:
        """
        Save standardized DataFrame to CSV file.
        
        Args:
            df (pd.DataFrame): Standardized DataFrame
            geo_id (str): GEO dataset identifier
            
        Returns:
            str: Path to the saved file
        """
        output_file = self.output_dir / f"{geo_id}_pheno.csv"
        df.to_csv(output_file, index=False)
        self.logger.info(f"Saved standardized data to: {output_file}")
        return str(output_file)
    
    def batch_process(self, pheno_dir: str) -> Dict[str, str]:
        """
        Process all phenotype files in a directory.
        
        Args:
            pheno_dir (str): Directory containing phenotype files (_pheno.xlsx)
            
        Returns:
            Dict[str, str]: Dictionary mapping GEO IDs to output file paths
        """
        pheno_dir = Path(pheno_dir)
        results = {}
        
        # Find all phenotype files
        pheno_files = list(pheno_dir.glob("*_pheno.xlsx"))
        self.logger.info(f"Found {len(pheno_files)} phenotype files in {pheno_dir}")
        
        for pheno_file in pheno_files:
            geo_id = pheno_file.stem.split('_')[0]
            
            # Process the file
            standardized_df = self.process_phenotype_file(str(pheno_file))

            # delete rows with NaN Age
            standardized_df = self.del_nan_age_rows(standardized_df)
            
            if standardized_df is not None:
                # Save the standardized data
                output_path = self.save_standardized_data(standardized_df, geo_id)
                results[geo_id] = output_path
            else:
                self.logger.error(f"Failed to process {pheno_file}")
                results[geo_id] = "FAILED"
        
        # Generate processing summary
        successful = sum(1 for status in results.values() if status != "FAILED")
        self.logger.info(f"Batch processing completed: {successful}/{len(pheno_files)} files successful")
        
        return results
    
    def validate_mappings(self) -> Dict[str, Any]:
        """
        Validate that all necessary mappings are available.
        
        Returns:
            Dict[str, Any]: Validation results
        """
        validation_results = {
            'missing_geo_ids': [],
            'missing_value_mappings': defaultdict(list),
            'summary': {}
        }
        
        if self.column_mapping_df is None:
            return validation_results
        
        # Check for GEO IDs in phenotype files that are not in column mapping
        # This would need to be called after knowing which files exist
        
        # Check value mapping coverage
        for sheet_name in ['Tissue', 'Disease', 'Condition', 'Age', 'Gender', 'Race']:
            if sheet_name in self.value_mappings:
                mapping_df = self.value_mappings[sheet_name]
                validation_results['summary'][f'{sheet_name}_mappings'] = len(mapping_df)
            else:
                validation_results['summary'][f'{sheet_name}_mappings'] = 0
        
        validation_results['summary']['total_datasets'] = len(self.column_mapping_df)
        
        return validation_results


# Example usage and interface functions
def create_phenotype_standardizer(data_mapping_file: str, 
                                value_mapping_file: str, 
                                output_dir: str) -> PhenotypeStandardizer:
    """
    Factory function to create a PhenotypeStandardizer instance.
    
    Args:
        data_mapping_file (str): Path to DataMapping_V2.xlsx
        value_mapping_file (str): Path to ValueMapping_V3.xlsx
        output_dir (str): Output directory for standardized files
        
    Returns:
        PhenotypeStandardizer: Configured standardizer instance
    """
    return PhenotypeStandardizer(data_mapping_file, value_mapping_file, output_dir)


def standardize_single_dataset(standardizer: PhenotypeStandardizer, 
                             pheno_file_path: str) -> Optional[str]:
    """
    Standardize a single phenotype file.
    
    Args:
        standardizer (PhenotypeStandardizer): Configured standardizer instance
        pheno_file_path (str): Path to the phenotype file
        
    Returns:
        Optional[str]: Path to the standardized CSV file, or None if failed
    """
    standardized_df = standardizer.process_phenotype_file(pheno_file_path)
    if standardized_df is not None:
        geo_id = Path(pheno_file_path).stem.split('_')[0]
        standardized_df = standardizer.del_nan_age_rows(standardized_df)
        return standardizer.save_standardized_data(standardized_df, geo_id)
    return None


def standardize_all_datasets(standardizer: PhenotypeStandardizer, 
                           pheno_dir: str) -> Dict[str, str]:
    """
    Standardize all phenotype files in a directory.
    
    Args:
        standardizer (PhenotypeStandardizer): Configured standardizer instance
        pheno_dir (str): Directory containing phenotype files
        
    Returns:
        Dict[str, str]: Mapping from GEO IDs to output file paths
    """
    return standardizer.batch_process(pheno_dir)


# Example usage
if __name__ == "__main__":
    # Configuration
    DATA_MAPPING_FILE = "../config/DataMapping_case.xlsx"
    VALUE_MAPPING_FILE = "../config/ValueMapping.xlsx"
    OUTPUT_DIR = "../data/standardized/pheno" 
    PHENO_DIR = "../data/parsed/pheno"
    
    try:
        # Create standardizer
        standardizer = create_phenotype_standardizer(
            DATA_MAPPING_FILE, 
            VALUE_MAPPING_FILE, 
            OUTPUT_DIR
        )
        
        # Validate mappings
        validation = standardizer.validate_mappings()
        print("Validation results:", validation['summary'])
        
        # Process all files in directory
        results = standardize_all_datasets(standardizer, PHENO_DIR)
        
        # Print results
        print("\nProcessing results:")
        for geo_id, status in results.items():
            print(f"  {geo_id}: {status}")
            
    except Exception as e:
        print(f"Error: {e}")