import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

robjects.r.source('/home/zongxizeng/MissCpGTest/R/Combine.R')

r_clock = robjects.r.Combine('GSE101764')
