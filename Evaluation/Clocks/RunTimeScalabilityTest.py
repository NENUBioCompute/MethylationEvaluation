
import pdb
import os
import gc
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import time
import json
#  import numpy as np
# frommath import sqrt
import pandas as pd
from collections import defaultdict
import logging


modelPath = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(modelPath+"/log_test_for_scalability.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def time_it(func):
    def wrapper(*args, **kvargs):
        start_time = time.time()
        func(*args, **kvargs)
        end_time = time.time()
        cost_time = end_time - start_time
        return cost_time
    return wrapper

@time_it
def Horvath_01(clock_path, file_path):
    table = importr('data.table')
    robjects.r.source(clock_path)
    pred_age = robjects.r.Horvath(file_path)

@time_it
def DNAmAgeSkinClock_02(clock_path, file_path):
    table = importr('data.table')
    robjects.r.source(clock_path)
    pred_age = robjects.r.SkinBloodAge(file_path)

@time_it
def zhang_03(clock_path, file_path):
    table = importr('data.table')
    robjects.r.source(clock_path)
    pred_age = robjects.r.ZhangAge(file_path)

@time_it
def Hannum_04(clock_path, file_path):
    table = importr('data.table')
    robjects.r.source(clock_path)
    pred_age = robjects.r.Hannum(file_path)

@time_it
def WeidnerAge_05(clock_path, file_path):
    table = importr('data.table')
    robjects.r.source(clock_path)
    pred_age = robjects.r.WeidnerAge(file_path)

@time_it
def LinAge_06(clock_path, file_path):
    table = importr('data.table')
    robjects.r.source(clock_path)
    pred_age = robjects.r.LinAge(file_path)

@time_it
def PedBE_08(clock_path, file_path):
    table = importr('data.table')
    robjects.r.source(clock_path)
    pred_age = robjects.r.PedBE(file_path)

@time_it
def MEAT_14(clock_path, file_path):
    # pdb.set_trace()
    table = importr('data.table')
    MEAT = importr('MEAT')
    SummarizedExperiment = importr('SummarizedExperiment')
    robjects.r.source(clock_path)
    
    pred_age = robjects.r.MEAT(file_path)

@time_it
def Levine_17(clock_path, file_path):
    table = importr('data.table')
    robjects.r.source(clock_path)
    pred_age = robjects.r.Levine(file_path)

@time_it
def BNNAge_19(clock_path, file_path):
    table = importr('data.table')
    robjects.r.source(clock_path)
    pred_age = robjects.r.BNNAge(file_path)

@time_it
def CorticalClock_24(clock_path, file_path):
    table = importr('data.table')
    robjects.r.source(clock_path)
    pred_age = robjects.r.CorticalClock(file_path)

@time_it
def VidalBraloAge_27(clock_path, file_path):
    table = importr('data.table')
    robjects.r.source(clock_path)
    pred_age = robjects.r.VidalBraloAge(file_path)

@time_it
def FeSTwo_09(file_path):
    from Evaluation.Python.FeSTwo.FeSTwo import FeSTwoTest
    pred_age = FeSTwoTest(file_path)
    
@time_it
def AltumAge_15(file_path):
    from Evaluation.Python.AltumAge.AltumAge import AltumAgeTest
    pred_age = AltumAgeTest(file_path)
    
@time_it
def EpigeneticPacemaker_22(file_path):
    from Evaluation.Python.EpigeneticPacemaker.EPM import EPMTest
    pred_age = EPMTest(file_path)

    
if __name__ == '__main__':
    # data path
    path_dict = {
        '100*27K': '/home/data/ScalabilityTestData/100/GSE25892_beta.csv',
        '100*450K': '/home/data/ScalabilityTestData/100/GSE101961_beta.csv',
        '100*850K': '/home/data/ScalabilityTestData/100/GSE137904_beta.csv',
        # '1K*27K': '/home/data/ScalabilityTestData/1K/27K_1K_beta.csv',
        # '1K*450K': '/home/data/ScalabilityTestData/1K/450K_1K_beta.csv',
        # '1K*850K': '/home/data/ScalabilityTestData/1K/850K_1K_beta.csv',
        # '10K*27K': '/home/data/ScalabilityTestData/10K/27K_10K_beta.csv',
                 }

    # clock path
    clocks_path = {
        'MEAT_14': '../R/14/MEAT.R',
        'Horvath_01': '../R/01/Horvath.R',
        'DNAmAgeSkinClock_02': '../R/02/DNAmAgeSkinClock.R',
        'zhang_03': '../R/03/ZhangAge.R',
        'Hannum_04': '../R/04/Hannum.R',
        'WeidnerAge_05': '../R/05/WeidnerAge.R',
        'LinAge_06': '../R/06/LinAge.R',
        'PedBE_08': '../R/08/PedBE.R',
        'Levine_17': '../R/17/Levine.R',
        'BNNAge_19': '../R/19/BNNAge.R',
        'CorticalClock_24': '../R/24/CorticalClock.R',
        'VidalBraloAge_27': '../R/27/VidalBraloAge.R',
        'FeSTwo_09': '',
        'AltumAge_15': '',
        'EpigeneticPacemaker_22': ''
    }

    # record save path
    save_path = 'methods_time_consumed.json'

    methods_time = {} # dict for record
    for method_name, clock_path in clocks_path.items():
        logger.info("method_name:{0},".format(method_name))
        time_consume = defaultdict(list)
        for scalar, file_path in path_dict.items():
            try:
                if '01' in method_name:
                    cost_time = Horvath_01(clock_path, file_path)
                    logger.info("data_type:{0}, cost_time:{1}".format(scalar, cost_time))
                    time_consume['data_type'].append(scalar)
                    time_consume['cost_time'].append(round(cost_time, 3))
                elif '02' in method_name:
                    cost_time = DNAmAgeSkinClock_02(clock_path, file_path)
                    logger.info("data_type:{0}, cost_time:{1}".format(scalar, cost_time))
                    time_consume['data_type'].append(scalar)
                    time_consume['cost_time'].append(round(cost_time, 3))
                elif '03' in method_name:
                    cost_time = zhang_03(clock_path, file_path)
                    logger.info("data_type:{0}, cost_time:{1}".format(scalar, cost_time))
                    time_consume['data_type'].append(scalar)
                    time_consume['cost_time'].append(round(cost_time, 3))
                elif '04' in method_name:
                    cost_time = Hannum_04(clock_path, file_path)
                    logger.info("data_type:{0}, cost_time:{1}".format(scalar, cost_time))
                    time_consume['data_type'].append(scalar)
                    time_consume['cost_time'].append(round(cost_time, 3))
                elif '05' in method_name:
                    cost_time = WeidnerAge_05(clock_path, file_path)
                    logger.info("data_type:{0}, cost_time:{1}".format(scalar, cost_time))
                    time_consume['data_type'].append(scalar)
                    time_consume['cost_time'].append(round(cost_time, 3))
                elif '06' in method_name:
                    cost_time = LinAge_06(clock_path, file_path)
                    logger.info("data_type:{0}, cost_time:{1}".format(scalar, cost_time))
                    time_consume['data_type'].append(scalar)
                    time_consume['cost_time'].append(round(cost_time, 3))
                elif '08' in method_name:
                    cost_time = PedBE_08(clock_path, file_path)
                    logger.info("data_type:{0}, cost_time:{1}".format(scalar, cost_time))
                    time_consume['data_type'].append(scalar)
                    time_consume['cost_time'].append(round(cost_time, 3))
                elif '14' in method_name:
                    cost_time = MEAT_14(clock_path, file_path)
                    logger.info("data_type:{0}, cost_time:{1}".format(scalar, cost_time))
                    time_consume['data_type'].append(scalar)
                    time_consume['cost_time'].append(round(cost_time, 3))
                elif '17' in method_name:
                    cost_time = Levine_17(clock_path, file_path)
                    logger.info("data_type:{0}, cost_time:{1}".format(scalar, cost_time))
                    time_consume['data_type'].append(scalar)
                    time_consume['cost_time'].append(round(cost_time, 3))
                elif '19' in method_name:
                    cost_time = BNNAge_19(clock_path, file_path)
                    logger.info("data_type:{0}, cost_time:{1}".format(scalar, cost_time))
                    time_consume['data_type'].append(scalar)
                    time_consume['cost_time'].append(round(cost_time, 3))
                elif '24' in method_name:
                    cost_time = CorticalClock_24(clock_path, file_path)
                    logger.info("data_type:{0}, cost_time:{1}".format(scalar, cost_time))
                    time_consume['data_type'].append(scalar)
                    time_consume['cost_time'].append(round(cost_time, 3))
                elif '27' in method_name:
                    cost_time = VidalBraloAge_27(clock_path, file_path)
                    logger.info("data_type:{0}, cost_time:{1}".format(scalar, cost_time))
                    time_consume['data_type'].append(scalar)
                    time_consume['cost_time'].append(round(cost_time, 3))
                elif '09' in method_name:
                    cost_time = FeSTwo_09(file_path)
                    logger.info("data_type:{0}, cost_time:{1}".format(scalar, cost_time))
                    time_consume['data_type'].append(scalar)
                    time_consume['cost_time'].append(round(cost_time, 3))
                elif '15' in method_name:
                    cost_time = AltumAge_15(file_path)
                    logger.info("data_type:{0}, cost_time:{1}".format(scalar, cost_time))
                    time_consume['data_type'].append(scalar)
                    time_consume['cost_time'].append(round(cost_time, 3))
                elif '22' in method_name:
                    cost_time = EpigeneticPacemaker_22(file_path)
                    logger.info("data_type:{0}, cost_time:{1}".format(scalar, cost_time))
                    time_consume['data_type'].append(scalar)
                    time_consume['cost_time'].append(round(cost_time, 3))
                del cost_time
                gc.collect()
            except:
                continue
        methods_time[method_name] = time_consume

    # save information of time consumed
    with open(save_path, 'w') as f:
        json.dump(methods_time, f, indent=4)
