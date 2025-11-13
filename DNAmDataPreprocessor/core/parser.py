
import subprocess
import pandas as pd
import gzip
import shutil
from pathlib import Path
import logging


class DataParser:
    def __init__(self, input_path, output_dir):
        """
        Initialize the Data Parser
        
        :param config_path: Path to the configuration file
        """
        self.script_dir = Path(__file__).parent.absolute()
        self.output_dir = output_dir
        self.input_path = input_path
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """
        Configure logging system for tracking processing steps and debugging
        
        Returns:
        --------
        logging.Logger
            Configured logger instance for the class
        """
        logger = logging.getLogger('DataParser')
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
        
    def get_r_script_path(self):
        """Get the absolute path to the R script in the same directory as this Python script"""
        r_script_path = self.script_dir / "parse_methylation_data.R"
        if not r_script_path.exists():
            raise FileNotFoundError(f"R script not found at: {r_script_path}")
        return r_script_path
    
    def run_r_parser(self):
        """Execute R parsing function"""
        try:
            # Get the absolute path to the R script
            r_script_path = self.get_r_script_path()
            
            # Build R command
            r_script = f"""
            # Load R parsing functions from the same directory as Python script
            source('{r_script_path}')
            
            # Get parameters from configuration
            input_path <- '{self.input_path}'
            output_dir <- '{self.output_dir}'
            idat_method <- 'minfi'  # Can be read from config if needed
            
            # Call parsing function
            parse_methylation_data(
                input_path = input_path,
                output_dir = output_dir,
                idat_method = idat_method
            )
            """
            
            # Execute R script
            result = subprocess.run(['Rscript', '-e', r_script], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info("R parsing function executed successfully")
                if result.stdout:
                    self.logger.info(result.stdout)
            else:
                self.logger.error("R parsing function execution failed")
                if result.stderr:
                    self.logger.error(result.stderr)
                raise Exception(f"R script execution error: {result.stderr}")
                
        except Exception as e:
            self.logger.error(f"Error while executing R parsing function: {e}")
            raise
    
    def check_and_process_files(self):
        """Check and process generated files"""
        # Create target directories
        express_dir = Path(self.output_dir) / "methyl"
        pheno_dir = Path(self.output_dir) / "pheno"
        express_dir.mkdir(exist_ok=True, parents=True)
        pheno_dir.mkdir(exist_ok=True, parents=True)
        
        # Get all files
        files = list(Path(self.output_dir).glob("*"))
        # Group files by ID
        file_groups = {}
        for file_path in files:
            if file_path.is_file():
                # Extract ID (remove suffix)
                stem = file_path.stem
                if stem.endswith('_beta.csv'):
                    geo_id = stem[:-9]  # Remove '_beta.csv'
                    file_groups.setdefault(geo_id, {})['beta'] = file_path
                elif stem.endswith('_pheno'):
                    geo_id = stem[:-6]  # Remove '_pheno'
                    file_groups.setdefault(geo_id, {})['pheno'] = file_path
        # Check files for each ID
        processed_count = 0
        for geo_id, files_dict in file_groups.items():
            self.logger.info(f"Checking ID: {geo_id}")
            
            # Check file completeness
            if 'beta' not in files_dict:
                self.logger.warning(f"ID {geo_id} is missing beta file")
                continue
            if 'pheno' not in files_dict:
                self.logger.warning(f"ID {geo_id} is missing pheno file")
                continue
            
            beta_path = files_dict['beta']
            pheno_path = files_dict['pheno']
            
            # Check beta file headers
            self.check_beta_headers(beta_path, pheno_path, geo_id)
            
            # Move files to organized directories
            self.move_files(beta_path, pheno_path, express_dir, pheno_dir, geo_id)
            processed_count += 1
        
        self.logger.info(f"Successfully processed {processed_count} datasets")
        return processed_count
    
    def check_beta_headers(self, beta_path, pheno_path, geo_id):
        """Check beta file headers and perform necessary mapping"""
        try:
            # Read beta file headers (only headers, not full data)
            with gzip.open(beta_path, 'rt') as f:
                header_line = f.readline().strip()
            
            headers = header_line.split(',')
            
            # First column should be CpG_Site, check remaining columns
            sample_headers = headers[1:]  # Remove first column
            
            # Check if headers start with GSM (GEO sample IDs typically start with GSM)
            gsm_headers = [h for h in sample_headers if h.startswith('GSM')]
            
            if len(gsm_headers) != len(sample_headers):
                self.logger.warning(f"ID {geo_id} beta file headers are not in GSM format, attempting mapping from pheno file")
                self.remap_beta_headers(beta_path, pheno_path, geo_id)
            else:
                self.logger.info(f"ID {geo_id} beta file headers are in correct format")
                
        except Exception as e:
            self.logger.error(f"Error checking beta file headers (ID: {geo_id}): {e}")
    
    def remap_beta_headers(self, beta_path, pheno_path, geo_id):
        """Remap beta file headers using SampleID from pheno file"""
        try:
            # Read pheno file to get SampleID
            pheno_df = pd.read_excel(pheno_path)
            
            if 'SampleID' not in pheno_df.columns:
                self.logger.warning(f"ID {geo_id} pheno file doesn't have SampleID column")
                # Try to find columns containing GSM IDs
                gsm_columns = [col for col in pheno_df.columns if any(pheno_df[col].astype(str).str.startswith('GSM').any())]
                if gsm_columns:
                    sample_ids = pheno_df[gsm_columns[0]].tolist()
                    self.logger.info(f"Using column '{gsm_columns[0]}' as sample IDs")
                else:
                    self.logger.warning(f"ID {geo_id} pheno file doesn't contain GSM sample IDs")
                    return
            else:
                sample_ids = pheno_df['SampleID'].tolist()
            
            # Read beta file
            beta_df = pd.read_csv(beta_path, compression='gzip')
            
            # Check if column count matches
            if len(beta_df.columns) - 1 != len(sample_ids):
                self.logger.warning(f"ID {geo_id} beta file column count ({len(beta_df.columns)-1}) doesn't match pheno file SampleID count ({len(sample_ids)})")
                # Try to truncate or pad
                if len(beta_df.columns) - 1 > len(sample_ids):
                    sample_ids.extend([f"Sample_{i}" for i in range(len(sample_ids), len(beta_df.columns)-1)])
                    self.logger.info(f"Padded sample IDs to {len(sample_ids)}")
                else:
                    sample_ids = sample_ids[:len(beta_df.columns)-1]
                    self.logger.info(f"Truncated sample IDs to {len(sample_ids)}")
            
            # Rename columns (keep first column as CpG_Site)
            new_columns = ['CpG_Site'] + sample_ids
            beta_df.columns = new_columns
            
            # DIRECTLY OVERWRITE THE ORIGINAL FILE
            with gzip.open(beta_path, 'wt') as f:
                beta_df.to_csv(f, index=False)
            self.logger.info(f"ID {geo_id} beta file headers successfully mapped")
            
        except Exception as e:
            self.logger.error(f"Error remapping beta file headers (ID: {geo_id}): {e}")
            # Clean up temporary file
            temp_path = beta_path.with_suffix('.csv.gz')
            if temp_path.exists():
                temp_path.unlink()
    
    def move_files(self, beta_path, pheno_path, express_dir, pheno_dir, geo_id):
        """Move files to new organized directories"""
        try:
            # Target paths
            beta_dest = express_dir / beta_path.name
            pheno_dest = pheno_dir / pheno_path.name
            
            # Move files
            shutil.move(str(beta_path), str(beta_dest))
            shutil.move(str(pheno_path), str(pheno_dest))
            
            self.logger.info(f"ID {geo_id} files successfully moved:")
            self.logger.info(f"  Beta file: {beta_dest}")
            self.logger.info(f"  Pheno file: {pheno_dest}")
            
        except Exception as e:
            self.logger.error(f"Error moving files (ID: {geo_id}): {e}")
    
    def process(self):
        """Main processing workflow"""
        try:
            self.logger.info("Starting methylation data processing")
            self.logger.info(f"Input path: {self.input_path}")
            self.logger.info(f"Output directory: {self.output_dir}")
            
            # Step 1: Execute R parsing function
            self.run_r_parser()
            
            # Step 2: Check and process files
            processed_count = self.check_and_process_files()
            
            self.logger.info("Methylation data processing completed successfully")
            return processed_count
            
        except Exception as e:
            self.logger.error(f"Error during processing: {e}")
            raise

