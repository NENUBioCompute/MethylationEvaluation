import csv
import os

import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import time
import json

table = importr('data.table')
robjects.r.source('/home/zongxizeng/MethylationEvaluation/Evaluation/R/05/WeidnerAge.R')


def WeidnerAge(GEOID):
    # beta data path
    beta_path = '/home/data/Standardized/express/' + GEOID + '_beta.csv'
    # pheno data path
    pheno_path = '/home/data/Standardized/pheno/' + GEOID + '_pheno.csv'
    # get  pheno data
    pheno_data = pd.read_csv(pheno_path)

    # run R test function
    start_t = time.time()
    RTestFunction = robjects.r.WeidnerAge(beta_path)
    end_t = time.time()

    trueAge = pheno_data['Age'].tolist()
    FileName = GEOID + "_predicted_by_NO.05.json"
    print(FileName)
    localTime = time.localtime()
    curTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
    ageData = {
        "FileName": FileName,
        "datetime": curTime,
        "Algorithm": "NO.05_WeidnerAge",
        "Dataset": GEOID,
        "Age_unit": pheno_data['Age_unit'].tolist()[0],
        "AgeRange": [min(trueAge), max(trueAge)],
        "SampleNum": len(trueAge),
        "ConsumeTime(Sec)": str(round((end_t - start_t), 3)) + 's',
        "Tissue": pheno_data['Tissue'].tolist(),
        "Condition": pheno_data['Condition'].tolist(),
        "Disease": pheno_data['Disease'].tolist(),
        "Gender": pheno_data['Gender'].tolist(),
        "Race": pheno_data['Race'].tolist(),
        "ID_REF": pheno_data['ID'].tolist(),
        "PredAge": list(RTestFunction),
        "TrueAge": trueAge,
        "Platform": pheno_data['Platform'].tolist()[0]
    }
    print(ageData)
    # file = '/home/zongxizeng/MethylationEvaluation/Evaluation/ResultNew/05/' + FileName
    # with open(file, 'w') as f:
    #     json.dump(ageData, f)
    # f.close()


WeidnerAge('GSE67444')
# if __name__ == '__main__':
#     geo = ['GSE67444','GSE42700','GSE77445','GSE75248']
#     errorGeo = []
#     for i in geo:
#         res_file = '/home/zongxizeng/MethylationEvaluation/Evaluation/ResultNew/05/' + i + '_predicted_by_NO.05.json'
#         if os.path.exists(res_file):
#             print('This result file already exists')
#             continue
#         else:
#             try:
#                 WeidnerAge(i)
#                 errorGeo.append(i)
#             except:
#                 print(i)
#                 continue
#     print(errorGeo)