import rpy2.robjects as robjects
from rpy2.robjects.packages import importr


table = importr('data.table')
robjects.r.source('../R/24/CorticalClock.R')


def CorticalClockAge(beta_path):
    # run R test function
    RTestFunction = robjects.r.CorticalClock(beta_path)
    return list(RTestFunction)
