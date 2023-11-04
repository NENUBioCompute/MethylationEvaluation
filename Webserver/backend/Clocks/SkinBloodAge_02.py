import rpy2.robjects as robjects
from rpy2.robjects.packages import importr




def SkinBloodAge(beta_path):
    table = importr('data.table')
    robjects.r.source('../R/02/DNAmAgeSkinClock.R')
    # run R test function
    RTestFunction = robjects.r.SkinBloodAge(beta_path)
    print(list(RTestFunction))
    return list(RTestFunction)
