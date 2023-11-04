import rpy2.robjects as robjects
from rpy2.robjects.packages import importr


table = importr('data.table')
robjects.r.source('../R/19/BNNAge.R')


def BNNAge(beta_path):
    # run R test function
    RTestFunction = robjects.r.BNNAge(beta_path)
    return list(RTestFunction)

