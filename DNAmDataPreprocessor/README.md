# 🧬 DNAmDataPreprocessor

A comprehensive and modular pipeline for downloading, parsing, and standardizing DNA methylation data with associated phenotypic information.

---

## 📘 Overview

DNAmDataPreprocessor is a modular and extensible Python framework for DNA methylation data preprocessing.
It provides a reproducible and customizable way to preprocess large-scale methylation datasets (e.g., from GEO), from raw file download to fully standardized datasets ready for downstream analyses such as epigenetic clock modeling, biomarker discovery, and disease classification. The system is designed with modularity and flexibility in mind, allowing users to run the entire workflow or individual components as needed.
---

## 🧠 Features

- ✅ **Automated Data Download**: Multi-threaded downloading with retry mechanisms and progress tracking
- ✅ **Flexible Parsing**: Configurable data parsing with support for multiple file formats
- ✅ **Phenotypic Data Standardization**: Automated mapping and validation using configurable mapping tables
- ✅ **Methylation Data Normalization**: Comprehensive normalization pipeline with quality control
- ✅ **Modular Architecture**: Use individual components or the complete pipeline
- ✅ **Comprehensive Logging**: Detailed logging for debugging and monitoring
- ✅ **Configurable Workflow**: YAML-based configuration for all processing parameters

## 🧩 Pipeline Overview

The pipeline performs five major steps:

|Step	|Function	|Description  |
| - | - | -|
|1️⃣	|Download	|Retrieve raw methylation data files (e.g., IDAT, TXT, CSV) from GEO, TCGA, or local repositories.|
|2️⃣	|Parse	|Parse and organize downloaded files into a unified format for downstream processing.|
|3️⃣	|Validate Mappings	|Verify sample and phenotype field correspondences.|
|4️⃣	|Phenotype Standardization	|Normalize phenotype data using mapping files and consistent value dictionaries.|
|5️⃣	|Methylation Standardization	|Normalize methylation matrices to β-values or M-values and validate completeness.|


## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/NENUBioCompute/MethylationEvaluation.git
cd DNAmDataPreprocessor

# Install dependencies
pip install -r requirements.txt
```
This project requires both Python and R environments, detail dependencies in **requirements.txt**.
**Please ensure that both are properly installed and accessible in your environment before running the tool.**


## 🚀 Quick Start

```python
from core.pipeline import DNAMPreprocessorPipeline

# Initialize the preprocessing pipeline
pipeline = DNAMPreprocessorPipeline("./config/default.yaml")

# Check the current pipeline status
status = pipeline.get_status()
print("Pipeline status:", status)

# Run the full preprocessing pipeline
results = pipeline.run_full_pipeline(
    download_list_path="./config/DownloadList.txt",
    overwrite=True, # Recommendation overwrite=True
)

print("Pipeline execution results:", results)
```

## 🏗️ Project Structure

```bash
dnam_preprocessor/
├── config/
│   ├── default.yaml              # Main configuration file
│   ├── DownloadList.txt          # Files to download
│   ├── DataMapping_case.xlsx     # Data structure mappings - customize
│   └── ValueMapping.xlsx         # Value standardization mappings - predefined
├── core/
│   ├── pipeline.py              # Main Pipeline class
│   ├── downloader.py            # Data download management
│   ├── parser.py                # Data parsing management
│   ├── processor_pheno.py       # Phenotypic data standardization
│   ├── processor_methyl.py      # Methylation data normalization
│   ├── parse_methylation_data.R # Data parsing utilities
│   └── impute_methylation.R     # Methylation normalization utilities
├── utils/ 
│   ├── config.py                # Configuration management
│   └── logger.py                # Logging utilities
├── example_usage.py             # Usage Example
└── requirements.txt             # Package dependencies
```

## ✏️ Configuration Example (config/default.yaml)

The pipeline is configured through YAML files. Key configuration sections:
```yaml
# Download Configuration
downloader:
    download_dir: "./data/raw"
    max_retries: 3
    timeout: 600
    use_multiprocessing: false
    download_method: "requests"
    downloaded_files_record: "./config/downloaded_files.txt"

# Parsing Configuration
parsing:
    input_path: "./config/downloaded_files.txt"
    output_dir: "./data/parsed"

# pheno_standardization Configuration
pheno_standardization:
    data_mapping_file: "./config/DataMapping_case.xlsx"
    value_mapping_file: "./config/ValueMapping.xlsx"
    input_dir: "./data/parsed/pheno"
    output_dir: "./data/standardized/pheno"

# methyl_standardization Configuration
methyl_standardization:
    expression_input_dir: "./data/parsed/methyl"
    pheno_input_dir: "./data/standardized/pheno" 
    output_dir: "./data/standardized/methyl"
```

## 🧠 Usage Examples

### 🏁 1. Run the Full Pipeline

```python
pipeline = DNAMPreprocessorPipeline()
results = pipeline.run_full_pipeline(
    download_list_path="./config/DownloadList.txt",
    overwrite=True,
)
```

### 📍 2. Step-by-Step Execution
```python
# Download only
pipeline.download_data(download_list_path="./config/DownloadList.txt")

# Parse downloaded files
pipeline.parse_data()

# Standardize phenotypic data
pipeline.validate_mappings()
pipeline.standardize_pheno_data()

# Normalize methylation data
pipeline.standardize_methyl_data(overwrite=True)
```

## 📜 Output Structure
The pipeline generates organized output directories:
```bash
raw/                      # Raw downloaded files
parsed/
├── pheno/                # Parsed phenotypic data
└── methyl/               # Parsed methylation data
standardized/
├── pheno/                # Standardized phenotypic data
└── methyl/               # Normalized methylation data
logs/                     # Processing logs
└── pipeline.log          # Log files generated automatically
```

## 🛠️ Mapping Files
### DataMapping.xlsx (manually)
Defines how source data columns map to standardized variable names:
- **Source variable names**: Matching must be performed based on the **column names** in the **parsed phenotype file**.
- **Target standardized names**: We have predefined a mapping template, columns containing: **"GEO_ID", "SampleID", "Tissue", "Disease", "Condition", "Age", "Age_unit", "Gender", "Race"**. 
    * "GEO_ID" denotes the dataset ID;
    * "SampleID" represents the sample ID;
    * "Tissue" indicates the tissue type; 
    * "Disease" refers to the disease status;
    * "Condition" pertains to disease-related information;
    * "Age" is the numerical age value;
    * "Age_unit" specifies the unit of the age value (possible values include: years, months, weeks);
    * "Gender" denotes sex, and ‘Race’ indicates racial information.

### ValueMapping.xlsx (manually)
Specifies how categorical values are standardized:
- **Original values**：Extract unique values from the target column in the parsed phenotype file.
- **Standardized values**: Custom mapping values.
- **Value codes**: "Tissue", "Disease", "Condition", "Age", "Gender", "Race". The six sheets respectively record the corresponding original values and standardized values under each label.
- [ValueMapping.xlsx](https://github.com/NENUBioCompute/MethylationEvaluation/blob/main/DNAmDataPreprocessor/config/ValueMapping.xlsx) is our manually mapped template based on 142 datasets.

## 📚 Citation
If you use DNAmClocksEvaluation in your research, please cite this repository appropriately:
- Wang, H. et al. A Comprehensive Assessment of Methylation-Based Age Prediction Methods. bioRxiv, 2024.2012.2023.627443 (2024). https://doi.org/10.1101/2024.12.23.627443
