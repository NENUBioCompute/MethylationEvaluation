from pathlib import Path
import os

# base directory configuration
BASE_DIR = Path(__file__).parent.parent
METHODS_DIR = BASE_DIR / "clocks"  # directory containing clock methods
OUTPUT_DIR = BASE_DIR / "results_clock_pred"  # output directory for prediction results

# data path configuration (adjust according to your environment)
# please used absolute paths to avoid path issues
BETA_DIR = Path('/home/qujing/MethylationEvaluation/DNAmClocksEvaluation/data/express')  # Methylation beta values directory
META_DIR = Path('/home/qujing/MethylationEvaluation/DNAmClocksEvaluation/data/pheno')  # Phenotype directory

# create necessary directories
OUTPUT_DIR.mkdir(exist_ok=True) 

# evaluation datasets configuration
EVALUATION_DATASETS = [
    'GSE151604_beta.csv.gz',
]
