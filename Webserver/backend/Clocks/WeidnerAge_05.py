import rpy2.robjects as robjects
from rpy2.robjects.packages import importr


table = importr('data.table')
robjects.r.source('../R/05/WeidnerAge.R')

def WeidnerAge(beta_path):
    # run R test function
    RTestFunction = robjects.r.WeidnerAge(beta_path)
    print(list(RTestFunction))
    return list(RTestFunction)
