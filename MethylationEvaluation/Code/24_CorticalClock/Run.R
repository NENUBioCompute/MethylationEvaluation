library(GEOquery)
# 在线读取GEO数据
dd <- getGEO('GSE20236', destdir = './', AnnotGPL=F, getGPL = F)
# 读取Beta值(当使用GEO下载的基因芯片里有甲基化数据时)
beta <- exprs(dd[[1]])
#读取临床数据
pheno <- pData(dd[[1]])



#读取本地GEO数据
setwd('E:/cecilia/数据集')
dd <- getGEO("GSE53740", filename="GSE53740_series_matrix.txt.gz", destdir = '', AnnotGPL=F, getGPL = F)

# 读取Beta值(当使用GEO下载的基因芯片里有甲基化数据时)
beta <- exprs(dd)
#读取临床数据
pheno <- pData(dd)
#pheno$`age:ch1` = as.numeric(sub(" years", '', pheno$`age:ch1`))
pheno$`age (y):ch1` = as.numeric(pheno$`age (y):ch1`)
path = "C:/Users/DELL/OneDrive/退行性_crr_personal/第24篇源代码/CorticalClock-master/PredCorticalAge/"
setwd(path)
source('CorticalClock.R')
starttime <- proc.time()
CorticalClock(beta,pheno,'C:/Users/DELL/OneDrive/退行性_crr_personal/第24篇源代码/CorticalClock-master/PredCorticalAge/','geo_accession','age (y):ch1')
runningtime <- proc.time()-starttime
print(runningtime)



####临床数据与表达矩阵分开
dd <- getGEO('GSE72775', destdir = './', AnnotGPL=F, getGPL = F)
#读取临床数据
pheno <- pData(dd[[1]])
pheno$`age:ch1` = as.numeric(pheno$`age:ch1`)
###获取表达矩阵####
library(csv)
#本地导入csv文件
data <- "E:/cecilia/数据集/GSE72775_datBetaNormalized.csv"
beta <- read.csv(data,row.names=1)
colnames(beta) <- pheno$geo_accession
path = "C:/Users/DELL/OneDrive/退行性_crr_personal/第24篇源代码/CorticalClock-master/PredCorticalAge/"
setwd(path)
source('CorticalClock.R')
starttime <- proc.time()
CorticalClock(beta,pheno,'C:/Users/DELL/OneDrive/退行性_crr_personal/第24篇源代码/CorticalClock-master/PredCorticalAge/','geo_accession','age:ch1')
runningtime <- proc.time()-starttime
print(runningtime)

