import json
import os
import time

import pandas as pd

from Python.EpigeneticPacemaker.EPM import EPMTest
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

table = importr('data.table')
robjects.r.source('../R/Clocks_T.R')


def EPMAge(beta_path):
    # pheno data path
    pheno_path = '/home/data/Standardized/pheno/' + GEOID + '_pheno.csv'
    # get  pheno data
    pheno_data = pd.read_csv(pheno_path)

    # EPM
    start_t = time.time()
    print('================NO.22=====================')
    EPMAge = EPMTest(GEOID)
    end_t = time.time()

    trueAge = pheno_data['Age'].tolist()
    FileName = GEOID + "_predicted_by_NO.22.json"
    localTime = time.localtime()
    curTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)

    ageData = {
        "FileName": GEOID + "_predicted_by_NO.22.json",
        "datetime": curTime,
        "Algorithm": "NO.22_EPM",
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
        "PredAge": EPMAge,
        "TrueAge": trueAge,
        "Platform": pheno_data['Platform'].tolist()[0]
    }
    file = '../Result/22/' + GEOID + "_predicted_by_NO.22.json"
    with open(file, 'w') as f:
        json.dump(ageData, f)
    f.close()
