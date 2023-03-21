import os

import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import time
import json

table = importr('data.table')
MEAT = importr('MEAT')
SummarizedExperiment = importr('SummarizedExperiment')

robjects.r.source('/home/zongxizeng/MethylationEvaluation/Evaluation/R/14/MEAT.R')


def MEATAge(GEOID):
    # beta data path
    beta_path = '/home/data/Standardized/express/' + GEOID + '_beta.csv'
    # pheno data path
    pheno_path = '/home/data/Standardized/pheno/' + GEOID + '_pheno.csv'
    # get  pheno data
    pheno_data = pd.read_csv(pheno_path)

    # run R test function
    start_t = time.time()
    RTestFunction = robjects.r.MEAT(beta_path)
    end_t = time.time()

    trueAge = pheno_data['Age'].tolist()
    FileName = GEOID + "_predicted_by_NO.14.json"
    localTime = time.localtime()
    curTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
    ageData = {
        "FileName": FileName,
        "datetime": curTime,
        "Algorithm": "NO.14_MEAT",
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
    # file = '/home/zongxizeng/MethylationEvaluation/Evaluation/ResultNew/14/' + FileName
    # with open(file, 'w') as f:
    #     json.dump(ageData, f)
    # f.close()

MEATAge('GSE151602')
# if __name__ == '__main__':
#     geo = ['GSE54211', 'GSE67444', 'GSE42700', 'GSE75248', 'GSE71678', 'GSE63106',
#            'GSE77445', 'GSE108213', 'GSE90124', 'GSE73103', 'GSE69176', 'GSE50660',
#            'GSE41826', 'GSE90060', 'GSE40279', 'GSE76105', 'GSE198904_1', 'GSE198904_2','GSE179325_1', 'GSE179325_2',
#            'GSE152026_1','GSE152026_2','GSE152026_3','GSE152026_4','GSE152026_5']
#     nogeo = ['GSE55763_1','GSE55763_2','GSE55763_3','GSE55763_4','GSE55763_5',
#              'GSE55763_6','GSE55763_7','GSE55763_8','GSE55763_9','GSE55763_10',
#              'GSE55763_11','GSE55763_12']
#     for i in nogeo:
#         res_file = '/home/zongxizeng/MethylationEvaluation/Evaluation/ResultNew/14/' + i + '_predicted_by_NO.14.json'
#         if os.path.exists(res_file):
#             print('This result file already exists')
#             continue
#         else:
#             try:
#                 MEATAge(i)
#             except:
#                 print(i)
#                 continue
