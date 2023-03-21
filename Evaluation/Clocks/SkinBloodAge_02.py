import os

import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import time
import json

table = importr('data.table')
robjects.r.source('/home/zongxizeng/methyTest/R/02/DNAmAgeSkinClock.R')


def SkinBloodAge(GEOID):
    # beta data path
    beta_path = '/home/data/Standardized/express/' + GEOID + '_beta.csv'
    # pheno data path
    pheno_path = '/home/data/Standardized/pheno/' + GEOID + '_pheno.csv'
    # get  pheno data
    pheno_data = pd.read_csv(pheno_path)

    # run R test function
    start_t = time.time()
    RTestFunction = robjects.r.SkinBloodAge(beta_path)
    end_t = time.time()

    trueAge = pheno_data['Age'].tolist()
    FileName = GEOID + "_predicted_by_NO.02.json"
    localTime = time.localtime()
    curTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
    ageData = {
        "FileName": FileName,
        "datetime": curTime,
        "Algorithm": "NO.02_SkinBloodAge",
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
    file = '/home/zongxizeng/methyTest/ResultNew/02/' + FileName
    # with open(file, 'w') as f:
    #     json.dump(ageData, f)
    # f.close()

SkinBloodAge('GSE67444')
# if __name__ == '__main__':
#     geo = ['GSE109042', 'GSE49905', 'GSE25892', 'GSE151601', 'GSE32149', 'GSE148000', 'GSE34035',
#            'GSE38873', 'GSE49908', 'GSE73103', 'GSE22595', 'GSE78874', 'GSE77136', 'GSE20236',
#            'GSE56606', 'GSE27317', 'GSE44763', 'GSE37988', 'GSE90124', 'GSE58119', 'GSE137502', 'GSE57484',
#            'GSE65638', 'GSE61257', 'GSE101961', 'GSE57285', 'GSE41826', 'GSE38608', 'GSE36194', 'GSE80970',
#            'GSE36812', 'GSE60132', 'GSE32396', 'GSE30870', 'GSE67024', 'GSE30601', 'GSE62867', 'GSE37008', 'GSE75248',
#            'GSE54211', 'GSE137898', 'GSE138279', 'GSE51954', 'GSE111223', 'GSE30758',
#            'GSE63384', 'GSE115797', 'GSE142439', 'GSE80261', 'GSE72773', 'GSE59157', 'GSE40005', 'GSE73832',
#            'GSE19711', 'GSE42700', 'GSE53128', 'GSE32393', 'GSE50660', 'GSE58045', 'GSE40360', 'GSE137884', 'GSE20242',
#            'GSE61431', 'GSE23638', 'GSE38291', 'GSE99029', 'GSE76105', 'GSE90060', 'GSE61496', 'GSE50759', 'GSE94734',
#            'GSE32867', 'GSE63106', 'GSE72777', 'GSE36064', 'GSE69176', 'GSE71245', 'GSE17448', 'GSE56342', 'GSE26126',
#            'GSE99624', 'GSE61258', 'GSE92767', 'GSE50498', 'GSE77445', 'GSE94876', 'GSE72338', 'GSE108213', 'GSE137495',
#            'GSE83334', 'GSE49904', 'GSE151604', 'GSE72775', 'GSE151602', 'GSE137903', 'GSE48325', 'GSE28746',
#            'GSE41037', 'GSE36054', 'GSE27097', 'GSE31979', 'GSE48988', 'GSE73377',
#            'GSE151600', 'GSE32148', 'GSE112987', 'GSE67705', 'GSE151603', 'GSE62219', 'GSE41169', 'GSE59457',
#            'GSE72556', 'GSE64495', 'GSE71678', 'GSE15745', 'GSE77241', 'GSE64511', 'GSE101764', 'GSE137688', 'GSE34257',
#            'GSE137894', 'GSE59509', 'GSE32146', 'GSE87571', 'GSE55763', 'GSE152026', 'GSE42861', 'GSE43414',
#            'GSE137904', 'GSE67444', 'GSE74193', 'GSE40279', 'GSE56105', 'GSE137841', 'GSE59685', 'GSE53740', 'GSE64511',
#            'GSE56581', 'GSE152026',
#            'GSE179325', 'GSE198904_1', 'GSE198904_2']
#     errorGeo = []
#     for i in geo:
#         res_file = '/home/zongxizeng/methyTest/result/02_fill/' + i + '_predicted_by_NO.02.json'
#         if os.path.exists(res_file):
#             print('This result file already exists')
#             continue
#         else:
#             try:
#                 SkinBloodAge(i)
#                 # errorGeo.append(i)
#             except:
#                 print(i)
#                 continue
#     print(len(errorGeo))
#     for i in errorGeo:
#         print(i)