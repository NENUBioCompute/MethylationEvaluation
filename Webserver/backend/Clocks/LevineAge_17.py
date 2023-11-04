import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

table = importr('data.table')
robjects.r.source('../R/17/Levine.R')


def LevineAge(beta_path):
    # run R test function
    RTestFunction = robjects.r.Levine(beta_path)
    return list(RTestFunction)
