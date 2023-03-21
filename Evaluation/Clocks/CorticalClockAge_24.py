import os

import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import time
import json

table = importr('data.table')
robjects.r.source('/home/zongxizeng/MethylationEvaluation/Evaluation/R/24/CorticalClock.R')


def CorticalClockAge(GEOID):
    # beta data path
    beta_path = '/home/data/Standardized/express/' + GEOID + '_beta.csv'
    # pheno data path
    pheno_path = '/home/data/Standardized/pheno/' + GEOID + '_pheno.csv'
    # get  pheno data
    pheno_data = pd.read_csv(pheno_path)

    # run R test function
    start_t = time.time()
    RTestFunction = robjects.r.CorticalClock(beta_path)
    end_t = time.time()

    trueAge = pheno_data['Age'].tolist()
    FileName = GEOID + "_predicted_by_NO.24.json"
    localTime = time.localtime()
    curTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
    ageData = {
        "FileName": FileName,
        "datetime": curTime,
        "Algorithm": "NO.24_CorticalClockAge",
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
    # file = '/home/zongxizeng/MethylationEvaluation/Evaluation/ResultNew/24/' + FileName
    # print(FileName)
    # with open(file, 'w') as f:
    #     json.dump(ageData, f)
    # f.close()

CorticalClockAge('GSE20242')
# if __name__ == '__main__':
#     geo = ['GSE67444', 'GSE75248', 'GSE60132', 'GSE69176', 'GSE71678', 'GSE42700', 'GSE63106', 'GSE77445', 'GSE73103',
#            'GSE198904_1', 'GSE198904_2', 'GSE179325', 'GSE90124', 'GSE108213', 'GSE76105', 'GSE90060',
#            'GSE50660', 'GSE40360', 'GSE53740', 'GSE42861', 'GSE40279', 'GSE55763_1', 'GSE55763_2', 'GSE55763_3',
#            'GSE55763_4', 'GSE55763_5', 'GSE55763_6', 'GSE55763_7', 'GSE55763_8', 'GSE55763_9', 'GSE55763_10',
#            'GSE55763_11', 'GSE55763_12',
#            'GSE54211', 'GSE25892', 'GSE23638', 'GSE36812', 'GSE26126', 'GSE31979',
#            'GSE34035', 'GSE20242', 'GSE56342', 'GSE36194', 'GSE56606', 'GSE32867', 'GSE44763',
#            'GSE49905', 'GSE15745', 'GSE41037', 'GSE32396', 'GSE38608', 'GSE20236', 'GSE17448', 'GSE58045', 'GSE49904',
#            'GSE30758', 'GSE22595', 'GSE58119', 'GSE49908', 'GSE62867', 'GSE38873', 'GSE38291',
#            'GSE57285', 'GSE27317', 'GSE57484', 'GSE30601', 'GSE27097', 'GSE32393', 'GSE48988', 'GSE37988', 'GSE28746',
#            'GSE63384', 'GSE19711', 'GSE37008', 'GSE34257']  # 'GSE55763',
#     for i in geo:
#         res_file = '/home/zongxizeng/MethylationEvaluation/Evaluation/ResultNew/24/' + i + '_predicted_by_NO.24.json'
#         if os.path.exists(res_file):
#             print('This result file already exists')
#             continue
#         else:
#             try:
#                 CorticalClockAge(i)
#             except:
#                 print(i)
#                 continue
