import os

import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import time
import json

table = importr('data.table')
robjects.r.source('../R/06/LinAge.R')


def LinAge(beta_path):
    robjects.r.source('../R/06/LinAge.R')
    # run R test function
    RTestFunction = robjects.r.LinAge(beta_path)
    return list(RTestFunction)


