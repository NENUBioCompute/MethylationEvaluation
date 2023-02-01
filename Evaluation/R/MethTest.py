import json
import os
import time
from MongoAdd import addData
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

table = importr('data.table')
robjects.r.source('/home/zongxizeng/methyTest/R/Clocks.R')

file_dir = "/home/data/Standardized/express"
geo = []
for root, dirs, files in os.walk(file_dir, topdown=False):
    for i in files:
        if 'beta.csv' in i:
            i = i.replace('_beta.csv', '')
            start_t = time.time()
            r_clock = robjects.r.ClocksTest(i)
            end_t = time.time()

            trueAge = list(r_clock[1])
            AgeRange = []
            AgeRange.append(min(trueAge))
            AgeRange.append(max(trueAge))
            FileName ='/home/zongxizeng/methyTest/result/' + i + "_predicted.json"
            print(FileName)
            localTime = time.localtime()
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
            ageData = {
                "FileName": i + "_predicted.json",
                "datetime": curTime,
                "Dataset": i,
                # "FeaType": r_clock[4][0],
                "AgeRange": AgeRange,
                "SampleNum": len(r_clock[0]),
                "ConsumeTime(Min)": str((end_t - start_t) / 60),
                "ID_REF": list(r_clock[0]),
                "Age_unit": list(r_clock[2]),
                "Tissue": list(r_clock[3]),
                "Condition": list(r_clock[4]),
                "Disease": list(r_clock[5]),
                "Gender": list(r_clock[6]),
                "Race": list(r_clock[7]),
                # platform: list(r_clock[8]),
                "PredAge": {
                    "SkinBloodAge": list(r_clock[8]),
                    "HannumAge": list(r_clock[9]),
                    "WeidnerAge": list(r_clock[10]),
                    "LinAge": list(r_clock[11]),
                    "PedBEAge": list(r_clock[12]),
                    "MEATAge": list(r_clock[13]),
                    "LevineAge": list(r_clock[14]),
                    "CorticalClockAge": list(r_clock[15]),
                    "VidalBraloAge": list(r_clock[16]),
                    "HorvathAge": list(r_clock[17]),
                    "ZhangAge": list(r_clock[18]),
                    "BNNAge": list(r_clock[19])
                },
                "TrueAge": list(r_clock[1])
            }

            with open(FileName, 'w') as f:
                json.dump(ageData, f)
            # return ageData
            addData(ageData)
