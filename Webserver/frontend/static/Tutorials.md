### DNA Methylation Age Prediction Platform Tutorial

Welcome to the DNA Methylation (DNAm) Clocks tutorial! This platform offers users an online service for DNA methylation age prediction, as well as a feature to view evaluation reports of various models that based on DNAm age prediction. Below is a detailed guide on how to use these two main features:

---

#### 1. Online Prediction Module

This module provides users with 15 published methylation age prediction models, which more information about the models can be found in **Clock** module. You can choose the appropriate model(s) based on your data attribute.

**Steps to Follow**:

1. **User Access**: 
  -This module is not available for guests. Before using, you must first log in to the platform.
  -If you are a new user, you need to register first, then log in. Otherwise, this feature will not be available.

2. **Select Model**: 
  - After logging in, navigate to the "Online Prediction" module.
  - You'll see a list featuring 15 models on right. ‘Clocks Info’ is a description of the data attribute each model suitable for.
  - Based on your data attribute, select one or more models by ticking the checkbox next to each model.

3. **Upload Data**: 
  - After selecting the model(s), select the uploading data.
  - **File Types and Limitations**:
    - Only CSV and ZIP file formats are supported for upload.
    - A maximum of **100 samples** can be predicted at a time.
  - ** Format of Files to Upload**:
    - **DNA Methylation Expression Matrix**: This matrix stores the Beta values of DNA methylation. It's arranged in a matrix format where rows represent CPG sites, and columns represent samples. There is no limitation on the number of CPG sites, but the sample count is capped at 100.
    - **Phenotype Information**: This file should correspond to the expression matrix samples. It's arranged in a matrix format where rows represent samples and columns represent phenotypic information. Column names should include each sample's ID (mandatory), tissue (mandatory), disease, gender, and race. Any unknown information can be left blank.
  - Before submission:
    - **Declare Dataset Category**: Indicate the type of tissue or cell your dataset belongs to.
    - **Specify Age Unit**: Define the unit in which age is represented in your dataset.
    - **Selection for Missing Values in Expression Matrix**: Choose an imputation method for handling missing values or **"NaN"** in the expression matrix.
  - Ensure your data format meets the platform's requirements, then select and upload your file.
  - After completing the above process, click the "Upload Dataset" button.

4. **Initiate Prediction**: 
  - Once your data is uploaded, the prediction begins.
  - Depending on the number of models selected and the size of the data, the prediction might take some time. Please be patient.

5. **View Prediction Results**: 
  - After the prediction is complete, you can view the age prediction results by clicking on the ‘here’ link on the same page.

---

#### 2. View Evaluation Report Module

This module displays our evaluation results of the 15 prediction methods. You can make a selection based on the desired model and dataset for visual comparison.

**Steps to Follow**:

1. **Select Dataset and Model**: 
  - Log in to the platform and navigate to the "View Evaluation Report" module.
  - **Dataset Selection**:
    - You can select data samples based on dataset ID, tissue, disease, or race. 
    - If selecting by **Dataset ID**: 
      - You can choose one or more datasets from the table displayed on the page.
      - The table provides details such as dataset ID, age range, age unit, and the number of samples. Sorting by dataset ID and sample count in ascending or descending order is supported.
      - Pagination through the table is available, and the number of datasets displayed per page can be modified.
    - If selecting by **tissue, disease, or race**:
      - The page displays 24 tissue categories, 54 disease categories, and 8 race categories for users to choose from.
      - These categories are defined based on a mapping file.
    - Based on the above selection, you can further narrow down the choice by gender.
  - First, choose the dataset of interest from the page table.
  - **Model Selection**:
    - After applying the desired filters and making selections, select the model(s) you wish to compare. Similar to the Online Prediction module, multiple models can be chosen for comparison.

2. **View Evaluation Results**:
  - After selecting the dataset and model(s), click the "Result" button in the upper right.
  - You'll be presented with several visual comparison charts showcasing the performance of each model on the selected dataset. 
    - **Viewing via Tables**:
      - Sample Information Table: Provides a comprehensive view of each sample's details.
      - Predicted Age Table: Shows the predicted age for each sample based on the chosen model.
    - **Viewing via Graphs**:
      - Multiple types of visual representations are available for better data interpretation:
      - Bar Chart: Assists in comparing age distributions across diverse datasets and categories.
      - Pie Chart: Provides a percentage distribution of various tissue or disease categories.
      - Scatter Plot: Helps in identifying patterns or relationships between true age and predicted age.

3. ** Detailed Analysis**: 
  - If you need more in-depth data or analysis, click on the " Comprehensive Report" link under this page to view the full assessment report and other related information.

---

We hope this tutorial helps you make the most of our DNAm Clocks platform. Should you have any questions or suggestions, please don't hesitate to contact us!
