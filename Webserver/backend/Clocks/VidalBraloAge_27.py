import os

import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import time
import json

table = importr('data.table')
robjects.r.source('../R/27/VidalBraloAge.R')


def VidalBraloAge(beta_path):


    # run R test function
    RTestFunction = robjects.r.VidalBraloAge(beta_path)
    return list(RTestFunction)
