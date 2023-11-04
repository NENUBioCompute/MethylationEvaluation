import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

table = importr('data.table')
robjects.r.source('../R/01/Horvath.R')


def HorvathAge(beta_path):
    # run R test function
    RTestFunction = robjects.r.Horvath(beta_path)
    return list(RTestFunction)


