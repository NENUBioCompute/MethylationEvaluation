# 🧬 DNAmClocksEvaluation

A unified and extensible framework for DNA methylation clock evaluation

---

## 📘 Overview

DNAmClocksEvaluation is a modular command-line tool designed for evaluating multiple DNA methylation (DNAm) clocks across diverse datasets.
It provides a unified interface for single-clock prediction, batch evaluation, and method management, supporting both Python-based and R-based clock models.

Each DNAm clock model is encapsulated as an independent module with its own data reading and prediction pipeline, ensuring extensibility and reproducibility.

---

## 🏗️ Project Structure

```bash
DNAmClocksEvaluation/
├── clocks/                # Each DNAm clock implemented as an independent module
│   ├── AltumAge/
│   ├── BNNAge/
│   └── ...
│
├── config/                # Configuration files (paths, dataset info, etc.)
│   └── settings.py
│
├── core/                  # Core execution engines (Python & R method runners)
│   ├── base_clock.py
│   └── clock_manager.py
│   └── python_clock_base.py
│   └── r_clock_base.py
│
├── data/                  # Input datasets (express, pheno, etc.)
│   ├── express/
│   └── pheno/
│
├── interfaces/            # API for invoking model predictions
│   └── api.py
│
├── results_clock_pred/    # Auto-generated prediction results (.json)
│
├── utils/                 # Utility functions for data handling & preprocessing
│   └── data_loader.py
│   └── data_processor.py
│   └── pickle_dealer.py
│
└── main.py                # Command-line entry point
└── requirements.txt       # Package dependencies

```

## ⚙️ Installation

You can clone the repository and install required dependencies:

```bash
git clone https://github.com/NENUBioCompute/MethylationEvaluation.git
cd DNAmClocksEvaluation
pip install -r requirements.txt
```

This project requires both Python and R environments, detail dependencies in **requirements.txt**.
**Please ensure that both are properly installed and accessible in your environment before running the tool.**

## 🚀 Usage
### 🔹 1. List Available Methods
View all available DNAm clock implementations currently registered in the framework:

```bash
python main.py list-methods
```
Output example:

```markdown
Available methods:
  - EPM
  - HannumAge
  - ZhangBlupredAge
  - PedBE
  - PhenoAge
  - VidalBraloAge
  - LinAge
  - CorticalClock
  - MEAT
  - AltumAge
  - FeSTwo
  - WeidnerAge
  - HorvathAge
  - SkinBloodClock
  - BNNAge
  - PerSEClock
```

### 🔹 2. Single Method Prediction

Use the predict command to run a single DNAm clock on a specific dataset.
This command prints prediction results directly to the terminal.

```bash
python main.py predict --method HorvathAge --dataset GSE151604
```

Output example:
```bash
Prediction completed in 7.715s:    predicted_age
0      62.343214
1      67.441997
2      67.867320
3      65.637205
4      65.177566
5      67.179044
6      65.576896
7      64.029010
8      68.270202
9      64.035961
```

### 🔹 3. Batch Evaluation

Run multiple DNAm clocks on multiple datasets simultaneously.
This command automatically saves results as .json files in [results_clock_pred/](https://github.com/NENUBioCompute/MethylationEvaluation/tree/main/DNAmClocksEvaluation/results_clock_pred). 

```bash
python main.py batch --method HorvathAge PerSEClock EPM --dataset GSE151604
```

If no methods or datasets are specified, all available clocks and configured datasets (from [config/settings.py](https://github.com/NENUBioCompute/MethylationEvaluation/blob/main/DNAmClocksEvaluation/config/settings.py)) will be used automatically:

```bash
python main.py batch
```

```bash
Starting batch evaluation with 16 methods on 1 datasets
... 
...
[INFO] Successfully predicted *** samples.
Batch evaluation completed !
```

## 📂 Output Format

Each batch evaluation automatically saves prediction results as JSON files in [results_clock_pred/](https://github.com/NENUBioCompute/MethylationEvaluation/tree/main/DNAmClocksEvaluation/results_clock_pred):

**Example:**
```json
{
    "FileName": "GSE151604_predicted_by_AltumAge.json",
    "datetime": "2025-11-09 15:32:04",
    "Algorithm": "AltumAge",
    "Dataset": "GSE151604",
    "AgeRange": [
        79.0,
        79.0
    ],
    "SampleNum": 10,
    "ConsumeTime(Min)": "23.699s",
    "ID_REF": [...],
    "Age_unit": "Year",
    "Tissue": [...]
    ,
    "Condition": [...],
    "Disease": [...]
    ,
    "Gender": [...],
    "Race": [...],
    "Platform": [...],
    "PredAge": [...],
    "TrueAge": [...]
}
```

## 🧠 Features

✅ Unified interface for 16+ DNAm clocks
✅ Supports both Python & R clock models
✅ Modular design for easy extension
✅ Batch execution & automatic result storage
✅ Dataset-agnostic and reproducible pipeline


## 🧬 Citation

If you use DNAmClocksEvaluation in your research, please cite this repository appropriately:
- Wang, H. et al. A Comprehensive Assessment of Methylation-Based Age Prediction Methods. bioRxiv, 2024.2012.2023.627443 (2024). https://doi.org/10.1101/2024.12.23.627443

