import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

GEOquery = importr("GEOquery")
Biobase = importr("Biobase")

print(GEOquery)
data = GEOquery.getGE0("GSE19711", filename="/home/data/Download/GSE19711_series matrix,txt.gz",destdir = '.',
                       AnnotGPL=False, getGPL=False)

pheno = Biobase.pData(data)
beta = Biobase.exprs(data)


