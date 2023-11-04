<template>
  <div class="tutorBox">
    <h3 style="color:rgb(21,132,202);">DNA Methylation Age Prediction Platform Tutorial</h3>

    <p style="color: rgb(82, 83, 84);">Welcome to the <i>DNA Methylation (DNAm) Clocks</i> tutorial!
      This platform offers users an online service for DNA methylation
      age prediction, as well as a feature to view evaluation reports
      of various models that based on DNAm age prediction. Below is a
      detailed guide on how to use these two main features:</p>

    <hr/>

    <h4>1. Online Prediction Module</h4>

    <p>This module provides users with 15 published methylation age prediction models, which
      more information about the models can be found in <strong>Clock</strong> module. You
      can choose the appropriate model(s) based on your data attribute.</p>

    <p><strong>Steps to Follow</strong>:</p>

    <ol><li><p><strong>User Access</strong>:
    -This module is not available for guests. Before using, you mustfirst log in to the platform.
    -If you are a new user, you need to register first, then log in. Otherwise, this feature will
    not be available.</p></li><li><p><strong>Select Model</strong>: </p><ul><li>After logging in,
      navigate to the &quot;Online Prediction&quot; module.</li><li>You&#39;ll seea list featuring 15
        models on right. 'Clocks Info' is a description of the data attribute each model suitable for.
      </li><li><p>Based on your data attribute, select one or more models by ticking the checkbox next
        to each model.</p></li></ul></li><li><p><strong>Upload Data</strong>: </p><ul><li>After selecting
          the model(s), select the uploading data.</li><li><strong>File Types and Limitations</strong>:<ul><li>Only CSV and ZIP file formats are supported for upload.</li><li>A maximum of <strong>100 samples</strong> can be predicted at a time.</li></ul></li><li><strong> Format of Files to Upload</strong>:<ul><li><strong>DNA Methylation Expression Matrix</strong>: This matrix stores the Beta values of DNA methylation. It&#39;s arranged in a matrix format where rows represent CPG sites, and columns represent samples. There is no limitation on the number of CPG sites, but the sample count is capped at 100.</li><li><strong>Phenotype Information</strong>: This file should correspond to the expression matrix samples. It&#39;s arranged in a matrix format where rows represent samples and columns represent phenotypic information. Column names should include each sample&#39;s ID (mandatory), tissue (mandatory), disease, gender, and race. Any unknown information can be left blank.</li></ul></li><li>Before submission:<ul><li><strong>Declare Dataset Category</strong>: Indicate the type of tissue or cell your dataset belongs to.</li><li><strong>Specify Age Unit</strong>: Define the unit in which age is represented in your dataset.</li><li><strong>Selection for Missing Values in Expression Matrix</strong>: Choose an imputation method for handling missing values or <strong>&quot;NaN&quot;</strong> in the expression matrix.</li></ul></li><li>Ensure your data format meets the platform&#39;s requirements, then select and upload your file.</li><li><p>After completing the above process, click the &quot;Upload Dataset&quot; button.</p></li></ul></li><li><p><strong>Initiate Prediction</strong>: </p><ul><li>Once your data is uploaded, the prediction begins.</li><li><p>Depending on the number of models selected and the size of the data, the prediction might take some time. Please be patient.</p></li></ul></li><li><p><strong>View Prediction Results</strong>: </p><ul><li>After the prediction is complete, you can view the age prediction results by clicking on the ‘here’ link on the same page.</li></ul></li></ol>

    <hr/>

    <h4>2. View Evaluation Report Module</h4>

    <p>This module displays our evaluation results of the 15 prediction methods. You can make a selection based on the desired model and dataset for visual comparison.</p>

    <p><strong>Steps to Follow</strong>:</p>

    <ol><li><p><strong>Select Dataset and Model</strong>: </p><ul><li>Log in to the platform and navigate to the &quot;View Evaluation Report&quot; module.</li><li><strong>Dataset Selection</strong>:<ul><li>You can select data samples based on dataset ID, tissue, disease, or race. </li><li>If selecting by <strong>Dataset ID</strong>: </li><li>You can choose one or more datasets from the table displayed on the page.</li><li>The table provides details such as dataset ID, age range, age unit, and the number of samples. Sorting by dataset ID and sample count in ascending or descending order is supported.</li><li>Pagination through the table is available, and the number of datasets displayed per page can be modified.</li><li>If selecting by <strong>tissue, disease, or race</strong>:</li><li>The page displays 24 tissue categories, 54 disease categories, and 8 race categories for users to choose from.</li><li>These categories are defined based on a mapping file.</li><li>Based on the above selection, you can further narrow down the choice by gender.</li></ul></li><li>First, choose the dataset of interest from the page table.</li><li><p><strong>Model Selection</strong>:</p><ul><li><p>After applying the desired filters and making selections, select the model(s) you wish to compare. Similar to the Online Prediction module, multiple models can be chosen for comparison.</p></li></ul></li></ul></li><li><p><strong>View Evaluation Results</strong>:</p><ul><li>After selecting the dataset and model(s), click the &quot;Result&quot; button in the upper right.</li><li><p>You&#39;ll be presented with several visual comparison charts showcasing the performance of each model on the selected dataset. </p><ul><li><strong>Viewing via Tables</strong>:</li><li>Sample Information Table: Provides a comprehensive view of each sample&#39;s details.</li><li>Predicted Age Table: Shows the predicted age for each sample based on the chosen model.</li><li><strong>Viewing via Graphs</strong>:</li><li>Multiple types of visual representations are available for better data interpretation:</li><li>Bar Chart: Assists in comparing age distributions across diverse datasets and categories.</li><li>Pie Chart: Provides a percentage distribution of various tissue or disease categories.</li><li><p>Scatter Plot: Helps in identifying patterns or relationships between true age and predicted age.</p></li></ul></li></ul></li><li><p><strong> Detailed Analysis</strong>: </p><ul><li>If you need more in-depth data or analysis, click on the &quot; Comprehensive Report&quot; link under this page to view the full assessment report and other related information.</li></ul></li></ol>

    <hr/>

    <p>We hope this tutorial helps you make the most of our DNAm Clocks platform. Should you have any questions or suggestions, please don&#39;t hesitate to contact us!</p>
  </div>
</template>

<script>

export default {
}
</script>

<style scoped>
.tutorBox{
  margin: auto;
  margin-top: 20px;
  width: 80%;
}
</style>
