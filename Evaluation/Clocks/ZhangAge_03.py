import os

import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import time
import json

table = importr('data.table')
robjects.r.source('/home/zongxizeng/methyTest/R/03/ZhangAge.R')


def ZhangAge(GEOID):
    # beta data path
    beta_path = '/home/data/Standardized/express/' + GEOID + '_beta.csv'
    # pheno data path
    pheno_path = '/home/data/Standardized/pheno/' + GEOID + '_pheno.csv'
    # get  pheno data
    pheno_data = pd.read_csv(pheno_path)

    # run R test function
    start_t = time.time()
    RTestFunction = robjects.r.ZhangAge(beta_path)
    end_t = time.time()

    trueAge = pheno_data['Age'].tolist()
    FileName = GEOID + "_predicted_by_NO.03.json"
    localTime = time.localtime()
    curTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
    ageData = {
        "FileName": FileName,
        "datetime": curTime,
        "Algorithm": "NO.03_Zhang",
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
    # file = '/home/zongxizeng/methyTest/ResultNew/03/' + FileName
    # with open(file, 'w') as f:
    #     json.dump(ageData, f)
    # return ageData

ZhangAge('GSE67444')
# if __name__ == '__main__':
#     geo = ['GSE67444', 'GSE42700', 'GSE75248', 'GSE71678', 'GSE63106', 'GSE77445', 'GSE73103', 'GSE90124', 'GSE108213',
#            'GSE76105', 'GSE69176', 'GSE90060', 'GSE50660', 'GSE41826', 'GSE40360', 'GSE53740', 'GSE40279', 'GSE101961',
#            'GSE151601', 'GSE151603', 'GSE151604', 'GSE151600', 'GSE137841', 'GSE151602', 'GSE198904_1', 'GSE198904_2',
#            'GSE142439', 'GSE137904_1', 'GSE137904_2', 'GSE137904_3', 'GSE137904_4', 'GSE55763_1', 'GSE55763_2',
#            'GSE55763_3', 'GSE55763_4', 'GSE55763_5', 'GSE55763_6', 'GSE55763_7', 'GSE55763_8', 'GSE55763_9',
#            'GSE55763_10', 'GSE55763_11', 'GSE55763_12', 'GSE42861_1', 'GSE42861_2', 'GSE42861_3', 'GSE42861_4',
#            'GSE152026_1', 'GSE152026_2', 'GSE152026_3', 'GSE152026_4', 'GSE152026_5', 'GSE179325_1', 'GSE179325_2',
#            'GSE54211', 'GSE25892', 'GSE23638', 'GSE36812', 'GSE26126', 'GSE31979',
#            'GSE34035', 'GSE20242', 'GSE56342', 'GSE36194', 'GSE56606', 'GSE32867', 'GSE44763',
#            'GSE49905', 'GSE15745', 'GSE41037', 'GSE32396', 'GSE38608', 'GSE20236', 'GSE17448', 'GSE58045', 'GSE49904',
#            'GSE30758', 'GSE22595', 'GSE58119', 'GSE49908', 'GSE62867', 'GSE38873', 'GSE38291',
#            'GSE57285', 'GSE27317', 'GSE57484', 'GSE30601', 'GSE27097', 'GSE32393', 'GSE48988', 'GSE37988', 'GSE28746',
#            'GSE63384', 'GSE19711', 'GSE37008', 'GSE34257']
#
#     # max = ['GSE55763', 'GSE152026','GSE42861', 'GSE43414','GSE137904','GSE179325', ]
#     for i in geo:
#         res_file = '/home/zongxizeng/methyTest/ResultNew/03/' + i + '_predicted_by_NO.03.json'
#         if os.path.exists(res_file):
#             print('This result file already exists')
#             continue
#         else:
#             try:
#                 ZhangAge(i)
#             except:
#                 print(i)
#                 continue
