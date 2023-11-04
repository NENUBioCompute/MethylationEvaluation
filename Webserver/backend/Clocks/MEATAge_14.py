import os

import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import time
import json

table = importr('data.table')
MEAT = importr('MEAT')
SummarizedExperiment = importr('SummarizedExperiment')

robjects.r.source('../R/14/MEAT.R')


def MEATAge(beta_path):
    MEAT = importr('MEAT')
    SummarizedExperiment = importr('SummarizedExperiment')

    robjects.r.source('../R/14/MEAT.R')
    # run R test function
    RTestFunction = robjects.r.MEAT(beta_path)
    return list(RTestFunction)
