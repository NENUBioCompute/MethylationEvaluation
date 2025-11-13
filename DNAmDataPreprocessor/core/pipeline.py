import yaml
from typing import Dict, List, Optional, Any
from core.downloader import DataDownloader
from core.parser import DataParser
from core.processor_pheno import create_phenotype_standardizer, standardize_all_datasets
from core.processor_methyl import DNAMethylationNormalizer
from utils.config import load_config
from utils.logger import setup_logger


class DNAmPreprocessorPipeline:
    """
    DNA methylation Data Preprocessing Pipeline
    Encapsulates a complete workflow for data downloading, parsing, 
    and normalization.
    """
    
    def __init__(self, config_path: str = "./config/default.yaml"):
        """
        Initialize the preprocessing pipeline.
        
        Args:
            config_path: Path to the configuration file.
        """
        self.config_path = config_path
        self.config = load_config(config_path)
        self.logger = setup_logger(__name__, self.config.get('logging', {}))
        
        # Initialize components
        self.downloader = None
        self.parser = None
        self.pheno_standardizer = None
        self.methyl_normalizer = None
        
        self._initialize_components()
        
    def _initialize_components(self):
        """Initialize all processing components."""
        try:
            # Initialize downloader
            downloader_config = self.config.get('downloader', {})
            self.downloader = DataDownloader(
                downloader_config.get('download_dir'),
                downloader_config.get('max_retries'),
                downloader_config.get('timeout'),
                downloader_config.get('use_multiprocessing', False),
                downloader_config.get('preferred_method', 'requests'),
                downloader_config.get('downloaded_files_record')
            )
            self.logger.info("Downloader initialized successfully.")
            
            # Initialize parser
            parsing_config = self.config.get('parsing', {})
            self.parser = DataParser(
                parsing_config.get('input_path'),
                parsing_config.get('output_dir')
            )
            self.logger.info("Data parser initialized successfully.")
            
            # Initialize phenotype data standardizer
            pheno_config = self.config.get('pheno_standardization', {})
            self.pheno_standardizer = create_phenotype_standardizer(
                pheno_config.get('data_mapping_file'),
                pheno_config.get('value_mapping_file'),
                pheno_config.get('output_dir')
            )
            self.logger.info("Phenotype standardizer initialized successfully.")
            
            # Initialize DNA methylation normalizer
            methyl_config = self.config.get('methyl_standardization', {})
            self.methyl_normalizer = DNAMethylationNormalizer(
                expression_path=methyl_config.get('expression_input_dir'),
                pheno_path=methyl_config.get('pheno_input_dir'),
                output_path=methyl_config.get('output_dir')
            )
            self.logger.info("DNA methylation normalizer initialized successfully.")
            
        except Exception as e:
            self.logger.error(f"Component initialization failed: {e}")
            raise
    
    def download_data(self, 
                     download_list_path: Optional[str] = None,
                     ) -> Dict[str, Any]:
        """
        Download data files.
        
        Args:
            download_list_path: Path to the download list file. 
                                If None, uses the path from the config.
            
        Returns:
            A dictionary containing download results.
        """
        self.logger.info("Starting data download process.")
        
        if download_list_path is None:
            download_list_path = "./config/DownloadList.txt"
        
        try:
            # Execute download
            results = self.downloader.download_from_list(download_list_path)
            
            # Get download status
            status = self.downloader.get_download_status()
            
            self.logger.info(
                f"Data download completed. "
                f"Success: {status.get('downloaded_files_count', 0)}, Failed: {status.get('failed', 0)}"
            )
            
            return {
                'results': results,
                'status': status,
                'success': status.get('failed', 0) == 0
            }
            
        except Exception as e:
            self.logger.error(f"Data download failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def parse_data(self) -> Dict[str, Any]:
        """
        Parse downloaded data files.
            
        Returns:
            A dictionary containing parsing results.
        """
        self.logger.info("Starting data parsing process.")
        
        try:
            # Execute parsing
            processed_count = self.parser.process()
            
            self.logger.info("Data parsing completed. "
                             f"Processed {processed_count} datasets."
                             )
            
            return {
                'success': True,
                'message': 'Data parsing completed.'
            }
            
        except Exception as e:
            self.logger.error(f"Data parsing failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def validate_mappings(self) -> Dict[str, Any]:
        """
        Validate data mapping relationships.
        
        Returns:
            A dictionary containing validation results.
        """
        self.logger.info("Starting mapping validation.")
        
        try:
            validation_results = self.pheno_standardizer.validate_mappings()
            
            self.logger.info("Mapping validation completed.")
            
            return {
                'success': True,
                'validation_results': validation_results
            }
            
        except Exception as e:
            self.logger.error(f"Mapping validation failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def standardize_pheno_data(self) -> Dict[str, Any]:
        """
        Standardize phenotype data.
            
        Returns:
            A dictionary containing standardization results.
        """
        self.logger.info("Starting phenotype data standardization.")
        
        try:
            pheno_config = self.config.get('pheno_standardization', {})
            results = standardize_all_datasets(
                self.pheno_standardizer, 
                pheno_config.get('input_dir')
            )
            
            self.logger.info(
                f"Phenotype data standardization completed. "
                f"Processed {len(results)} datasets."
            )
            
            return {
                'success': True,
                'results': results,
                'processed_count': len(results)
            }
            
        except Exception as e:
            self.logger.error(f"Phenotype data standardization failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def standardize_methyl_data(self, overwrite: bool = True) -> Dict[str, Any]:
        """
        Standardize DNA methylation data.
        
        Args:
            overwrite: Whether to overwrite existing files.
            
        Returns:
            A dictionary containing standardization results.
        """
        self.logger.info("Starting DNA methylation data standardization.")
        
        try:
            results = self.methyl_normalizer.run_full_pipeline(
                overwrite=overwrite
            )
            
            self.logger.info("DNA methylation data standardization completed. "
                             f"Processed {len(results)} datasets."
                             )
            
            return {
                'success': True,
                'results': results
            }
            
        except Exception as e:
            self.logger.error(f"DNA methylation data standardization failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def run_full_pipeline(self, 
                         download_list_path: Optional[str] = None, 
                         overwrite: bool = True
                         ) -> Dict[str, Any]:
        """
        Run the complete preprocessing pipeline.
        
        Args:
            download_list_path: Path to the download list file.
            overwrite: Whether to overwrite existing files.
            
        Returns:
            A dictionary containing full pipeline results.
        """
        self.logger.info("Starting full preprocessing pipeline.")
        
        pipeline_results = {}
        
        try:
            # 1. Data download
            download_result = self.download_data(download_list_path=download_list_path)
            pipeline_results['download'] = download_result
            
            if not download_result['success']:
                self.logger.error("Download stage failed. Pipeline stopped.")
                return pipeline_results
            
            # 2. Data parsing
            parse_result = self.parse_data()
            pipeline_results['parse'] = parse_result
            
            if not parse_result['success']:
                self.logger.error("Parsing stage failed. Pipeline stopped.")
                return pipeline_results
            
            # 3. Mapping validation
            validation_result = self.validate_mappings()
            pipeline_results['validation'] = validation_result
            
            if not validation_result['success']:
                self.logger.warning("Mapping validation failed. Continuing with standardization.")
            
            # 4. Phenotype data standardization
            pheno_result = self.standardize_pheno_data()
            pipeline_results['pheno_standardization'] = pheno_result
            
            if not pheno_result['success']:
                self.logger.error("Phenotype standardization failed. Pipeline stopped.")
                return pipeline_results
            
            # 5. DNA methylation data standardization
            methyl_result = self.standardize_methyl_data(overwrite=overwrite)
            pipeline_results['methyl_standardization'] = methyl_result
            
            # Compute overall success
            pipeline_results['overall_success'] = all(
                result.get('success', False)
                for step, result in pipeline_results.items()
                if step != 'validation'  # Validation step is optional
            )
            
            self.logger.info("Full preprocessing pipeline completed successfully.")
            
        except Exception as e:
            self.logger.error(f"Full pipeline execution failed: {e}")
            pipeline_results['overall_success'] = False
            pipeline_results['error'] = str(e)
        
        return pipeline_results
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current pipeline status.
        
        Returns:
            A dictionary containing status information.
        """
        status = {
            'components_initialized': {
                'downloader': self.downloader is not None,
                'parser': self.parser is not None,
                'pheno_standardizer': self.pheno_standardizer is not None,
                'methyl_normalizer': self.methyl_normalizer is not None
            },
            'config_loaded': self.config is not None
        }
        
        # If downloader is initialized, get its status
        if self.downloader:
            status['download_status'] = self.downloader.get_download_status()
        
        return status
    
    def update_config(self, new_config: Dict[str, Any]):
        """
        Update configuration and reinitialize components.
        
        Args:
            new_config: New configuration dictionary.
        """
        # Update in-memory configuration
        self.config.update(new_config)
        
        # Save to file
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f)
        
        # Reinitialize components
        self._initialize_components()
        
        self.logger.info("Configuration updated successfully.")
