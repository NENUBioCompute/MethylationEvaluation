import rpy2.robjects as robjects
from rpy2.robjects.packages import importr


table = importr('data.table')
robjects.r.source('../R/04/Hannum.R')


def HannumAge(beta_path):
    # run R test function
    RTestFunction = robjects.r.Hannum(beta_path)
    return list(RTestFunction)
