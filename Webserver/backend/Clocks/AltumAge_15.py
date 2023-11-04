import json
import os
import time

import pandas as pd

from Python.AltumAge.AltumAge import AltumAgeTest



def AltumAge(beta_path):
    # beta data path
    beta_path = '/home/data/Standardized/express/' + beta_path + '_beta.csv'
    # pheno data path
    pheno_path = '/home/data/Standardized/pheno/' + beta_path + '_pheno.csv'
    # get  pheno data
    pheno_data = pd.read_csv(pheno_path)

    # AltumAge
    start_t = time.time()
    print('================NO.15=====================')
    AltumAge = AltumAgeTest(beta_path)
    end_t = time.time()

    trueAge = pheno_data['Age'].tolist()
    localTime = time.localtime()
    curTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
    ageData = {
        "FileName": beta_path + "_predicted_by_NO.15.json",
        "datetime": curTime,
        "Algorithm": "NO.15_AltumAge",
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
        "PredAge": AltumAge,
        "TrueAge": trueAge,
        "Platform": pheno_data['Platform'].tolist()[0]
    }
    file = '../Result/15/' + beta_path + "_predicted_by_NO.15.json"
    with open(file, 'w') as f:
        json.dump(ageData, f)
    f.close()
