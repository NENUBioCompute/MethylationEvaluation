# 🧬 DNAm Multi-Module Platform

A comprehensive platform for DNA methylation **data preprocessing**, **clock evaluation**, and **cloud-based visualization**.
This repository integrates three main components:

- ✨ (**DNAmDataPreprocessor**)[https://github.com/NENUBioCompute/MethylationEvaluation/tree/main/DNAmDataPreprocessor] – Automated pipeline for downloading, parsing, and standardizing DNA methylation datasets.

- ✨ (**DNAmClocksEvaluation**)[https://github.com/NENUBioCompute/MethylationEvaluation/tree/main/DNAmClocksEvaluation] – Evaluation framework for benchmarking multiple epigenetic clocks across diverse datasets.

- ✨ (**Webserver**)[http://www.dnamclock.com/#/] – An interactive cloud-based web platform for model visualization and biological age prediction.

---

## 🌱 Overview
This project provides an end-to-end solution for DNA methylation-based biological age estimation and comparative analysis.
It bridges raw data processing, multi-clock evaluation, and online deployment in one unified system.
---

## 📦 Components   

### 🗳️ DNAmDataPreprocessor
**Purpose**: Standardizes raw DNA methylation data for downstream analysis. ([Quick Start])[https://github.com/NENUBioCompute/MethylationEvaluation/tree/main/DNAmDataPreprocessor]
**Key Features:**
- Batch download and parsing of public datasets (GEO, TCGA, etc.)
- Automated handling of ".idat", ".txt", ".csv", and mixed-format inputs
- Standardized Mapping and Validation of Phenotypic Data Based on Configurable Mapping Tables
- A comprehensive standardization workflow encompassing beta value detection, missing value imputation, and matching with phenotypic data.

Supported R packages:
stringr, data.table, tools, R.utils, dplyr, methyLImp2, BiocParallel

### 📊 DNAmClocksEvaluation
**Purpose**: Benchmarks and compares multiple epigenetic clocks across datasets. ([Quick Start])[https://github.com/NENUBioCompute/MethylationEvaluation/tree/main/DNAmClocksEvaluation]
**Key Features:**
- Supports 16+ biological clock models (R- and Python-based)
- Unified evaluation API for performance comparison
- Modular design for easy extension

Core Dependencies:
- tensorflow, numpy, pandas, scikit-learn, EpigeneticPacemaker
- BiocManager, data.table, MEAT, methylclock

### 🌐 Webserver

**Purpose**: Provides an online interface for visualization and user interaction. ([Quick Start])[http://www.dnamclock.com/#/]
**Key Features:**
- Web-based biological age prediction
- Interactive dashboards for multi-clock results
- Dataset upload, prediction, and visualization modules
- Scalable back-end supporting both R and Python integration

## ⚙️ System Requirements
- Python 3.8+
- R 4.1+
- 8GB+ RAM (16GB recommended for large datasets)
- 50GB+ free disk space

## 📚 Citation
If you use DNAmClocksEvaluation in your research, please cite this repository appropriately:
- Wang, H. et al. A Comprehensive Assessment of Methylation-Based Age Prediction Methods. bioRxiv, 2024.2012.2023.627443 (2024). https://doi.org/10.1101/2024.12.23.627443