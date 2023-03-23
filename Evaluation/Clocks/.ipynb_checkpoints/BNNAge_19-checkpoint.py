import os

import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import time
import json

table = importr('data.table')
robjects.r.source('/home/zongxizeng/MethylationEvaluation/Evaluation/R/19/BNNAge.R')


def BNNAge(GEOID):
    # beta data path
    beta_path = '/home/data/Standardized/express/' + GEOID + '_beta.csv'
    # pheno data path
    pheno_path = '/home/data/Standardized/pheno/' + GEOID + '_pheno.csv'
    # get  pheno data
    pheno_data = pd.read_csv(pheno_path)

    # run R test function
    start_t = time.time()
    RTestFunction = robjects.r.BNNAge(beta_path)
    end_t = time.time()

    trueAge = pheno_data['Age'].tolist()
    FileName = GEOID + "_predicted_by_NO.19.json"
    localTime = time.localtime()
    curTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
    ageData = {
        "FileName": FileName,
        "datetime": curTime,
        "Algorithm": "NO.19_BNNAge",
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
    file = '/home/zongxizeng/MethylationEvaluation/Evaluation/ResultNew/19/' + FileName
    # with open(file, 'w') as f:
    #     json.dump(ageData, f)
    print(ageData)
    # f.close()

BNNAge('GSE20242')
# if __name__ == '__main__':
#     geo = ['GSE54211', 'GSE67444', 'GSE42700', 'GSE75248', 'GSE71678', 'GSE63106', 'GSE73103', 'GSE77445', 'GSE108213',
#            'GSE50660', 'GSE76105', 'GSE90124', 'GSE55763_1', 'GSE55763_2', 'GSE55763_3', 'GSE55763_4', 'GSE55763_5',
#            'GSE55763_6', 'GSE55763_7', 'GSE55763_8', 'GSE55763_9', 'GSE55763_10', 'GSE55763_11', 'GSE55763_12',
#            'GSE151601', 'GSE151603', 'GSE151604', 'GSE151600', 'GSE137904', 'GSE137841', 'GSE151602',
#            'GSE198904_1', 'GSE198904_2', 'GSE179325', 'GSE142439','GSE152026_1','GSE152026_2','GSE152026_3','GSE152026_4','GSE152026_5',
#            'GSE51954']
#     for i in geo:
#         res_file = '/home/zongxizeng/MethylationEvaluation/Evaluation/ResultNew/19/' + i + '_predicted_by_NO.19.json'
#         if os.path.exists(res_file):
#             print('This result file already exists')
#             continue
#         else:
#             try:
#                 BNNAge(i)
#             except:
#                 print(i)
#                 continue
