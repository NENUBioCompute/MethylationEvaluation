webpackJsonp([15],{"/EsY":function(e,t,o){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var i={render:function(){this.$createElement;this._self._c;return this._m(0)},staticRenderFns:[function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"tutorBox"},[o("h3",{staticStyle:{color:"rgb(21,132,202)"}},[e._v("DNA Methylation Age Prediction Platform Tutorial")]),e._v(" "),o("p",{staticStyle:{color:"rgb(82, 83, 84)"}},[e._v("Welcome to the "),o("i",[e._v("DNA Methylation (DNAm) Clocks")]),e._v(" tutorial!\n    This platform offers users an online service for DNA methylation\n    age prediction, as well as a feature to view evaluation reports\n    of various models that based on DNAm age prediction. Below is a\n    detailed guide on how to use these two main features:")]),e._v(" "),o("hr"),e._v(" "),o("h4",[e._v("1. Online Prediction Module")]),e._v(" "),o("p",[e._v("This module provides users with 15 published methylation age prediction models, which\n    more information about the models can be found in "),o("strong",[e._v("Clock")]),e._v(" module. You\n    can choose the appropriate model(s) based on your data attribute.")]),e._v(" "),o("p",[o("strong",[e._v("Steps to Follow")]),e._v(":")]),e._v(" "),o("ol",[o("li",[o("p",[o("strong",[e._v("User Access")]),e._v(":\n  -This module is not available for guests. Before using, you mustfirst log in to the platform.\n  -If you are a new user, you need to register first, then log in. Otherwise, this feature will\n  not be available.")])]),o("li",[o("p",[o("strong",[e._v("Select Model")]),e._v(": ")]),o("ul",[o("li",[e._v('After logging in,\n    navigate to the "Online Prediction" module.')]),o("li",[e._v("You'll seea list featuring 15\n      models on right. 'Clocks Info' is a description of the data attribute each model suitable for.\n    ")]),o("li",[o("p",[e._v("Based on your data attribute, select one or more models by ticking the checkbox next\n      to each model.")])])])]),o("li",[o("p",[o("strong",[e._v("Upload Data")]),e._v(": ")]),o("ul",[o("li",[e._v("After selecting\n        the model(s), select the uploading data.")]),o("li",[o("strong",[e._v("File Types and Limitations")]),e._v(":"),o("ul",[o("li",[e._v("Only CSV and ZIP file formats are supported for upload.")]),o("li",[e._v("A maximum of "),o("strong",[e._v("100 samples")]),e._v(" can be predicted at a time.")])])]),o("li",[o("strong",[e._v(" Format of Files to Upload")]),e._v(":"),o("ul",[o("li",[o("strong",[e._v("DNA Methylation Expression Matrix")]),e._v(": This matrix stores the Beta values of DNA methylation. It's arranged in a matrix format where rows represent CPG sites, and columns represent samples. There is no limitation on the number of CPG sites, but the sample count is capped at 100.")]),o("li",[o("strong",[e._v("Phenotype Information")]),e._v(": This file should correspond to the expression matrix samples. It's arranged in a matrix format where rows represent samples and columns represent phenotypic information. Column names should include each sample's ID (mandatory), tissue (mandatory), disease, gender, and race. Any unknown information can be left blank.")])])]),o("li",[e._v("Before submission:"),o("ul",[o("li",[o("strong",[e._v("Declare Dataset Category")]),e._v(": Indicate the type of tissue or cell your dataset belongs to.")]),o("li",[o("strong",[e._v("Specify Age Unit")]),e._v(": Define the unit in which age is represented in your dataset.")]),o("li",[o("strong",[e._v("Selection for Missing Values in Expression Matrix")]),e._v(": Choose an imputation method for handling missing values or "),o("strong",[e._v('"NaN"')]),e._v(" in the expression matrix.")])])]),o("li",[e._v("Ensure your data format meets the platform's requirements, then select and upload your file.")]),o("li",[o("p",[e._v('After completing the above process, click the "Upload Dataset" button.')])])])]),o("li",[o("p",[o("strong",[e._v("Initiate Prediction")]),e._v(": ")]),o("ul",[o("li",[e._v("Once your data is uploaded, the prediction begins.")]),o("li",[o("p",[e._v("Depending on the number of models selected and the size of the data, the prediction might take some time. Please be patient.")])])])]),o("li",[o("p",[o("strong",[e._v("View Prediction Results")]),e._v(": ")]),o("ul",[o("li",[e._v("After the prediction is complete, you can view the age prediction results by clicking on the ‘here’ link on the same page.")])])])]),e._v(" "),o("hr"),e._v(" "),o("h4",[e._v("2. View Evaluation Report Module")]),e._v(" "),o("p",[e._v("This module displays our evaluation results of the 15 prediction methods. You can make a selection based on the desired model and dataset for visual comparison.")]),e._v(" "),o("p",[o("strong",[e._v("Steps to Follow")]),e._v(":")]),e._v(" "),o("ol",[o("li",[o("p",[o("strong",[e._v("Select Dataset and Model")]),e._v(": ")]),o("ul",[o("li",[e._v('Log in to the platform and navigate to the "View Evaluation Report" module.')]),o("li",[o("strong",[e._v("Dataset Selection")]),e._v(":"),o("ul",[o("li",[e._v("You can select data samples based on dataset ID, tissue, disease, or race. ")]),o("li",[e._v("If selecting by "),o("strong",[e._v("Dataset ID")]),e._v(": ")]),o("li",[e._v("You can choose one or more datasets from the table displayed on the page.")]),o("li",[e._v("The table provides details such as dataset ID, age range, age unit, and the number of samples. Sorting by dataset ID and sample count in ascending or descending order is supported.")]),o("li",[e._v("Pagination through the table is available, and the number of datasets displayed per page can be modified.")]),o("li",[e._v("If selecting by "),o("strong",[e._v("tissue, disease, or race")]),e._v(":")]),o("li",[e._v("The page displays 24 tissue categories, 54 disease categories, and 8 race categories for users to choose from.")]),o("li",[e._v("These categories are defined based on a mapping file.")]),o("li",[e._v("Based on the above selection, you can further narrow down the choice by gender.")])])]),o("li",[e._v("First, choose the dataset of interest from the page table.")]),o("li",[o("p",[o("strong",[e._v("Model Selection")]),e._v(":")]),o("ul",[o("li",[o("p",[e._v("After applying the desired filters and making selections, select the model(s) you wish to compare. Similar to the Online Prediction module, multiple models can be chosen for comparison.")])])])])])]),o("li",[o("p",[o("strong",[e._v("View Evaluation Results")]),e._v(":")]),o("ul",[o("li",[e._v('After selecting the dataset and model(s), click the "Result" button in the upper right.')]),o("li",[o("p",[e._v("You'll be presented with several visual comparison charts showcasing the performance of each model on the selected dataset. ")]),o("ul",[o("li",[o("strong",[e._v("Viewing via Tables")]),e._v(":")]),o("li",[e._v("Sample Information Table: Provides a comprehensive view of each sample's details.")]),o("li",[e._v("Predicted Age Table: Shows the predicted age for each sample based on the chosen model.")]),o("li",[o("strong",[e._v("Viewing via Graphs")]),e._v(":")]),o("li",[e._v("Multiple types of visual representations are available for better data interpretation:")]),o("li",[e._v("Bar Chart: Assists in comparing age distributions across diverse datasets and categories.")]),o("li",[e._v("Pie Chart: Provides a percentage distribution of various tissue or disease categories.")]),o("li",[o("p",[e._v("Scatter Plot: Helps in identifying patterns or relationships between true age and predicted age.")])])])])])]),o("li",[o("p",[o("strong",[e._v(" Detailed Analysis")]),e._v(": ")]),o("ul",[o("li",[e._v('If you need more in-depth data or analysis, click on the " Comprehensive Report" link under this page to view the full assessment report and other related information.')])])])]),e._v(" "),o("hr"),e._v(" "),o("p",[e._v("We hope this tutorial helps you make the most of our DNAm Clocks platform. Should you have any questions or suggestions, please don't hesitate to contact us!")])])}]};var a=o("VU/8")({},i,!1,function(e){o("ZFWG")},"data-v-309453c4",null);t.default=a.exports},ZFWG:function(e,t){}});
//# sourceMappingURL=15.57a2e972b1e89cab877a.js.map