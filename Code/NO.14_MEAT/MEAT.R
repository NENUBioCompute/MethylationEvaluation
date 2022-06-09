library(MEAT)
library(GEOquery)
library(SummarizedExperiment)
library(data.table)
# 读取GEO数据集
GEOID= 'GSE56105'
gseData <- getGEO(GEOID, destdir = '.', AnnotGPL = FALSE, getGPL = F)
# 获取表达矩阵
dat0 = exprs(gseData[[1]])
# 获取临床数据
ph = pData(gseData[[1]])

# 判断表达矩阵是否为空
if (length(dat0) == 0) {
  name <- paste(GEOID, '_beta.csv', sep = "", collapse = NULL)
  dat0 <- fread(name)
  dat0 <- data.frame
}
else {
  dat0 <- data.frame(rownames(dat0), dat0)
}
# 添加年龄列
ph[, 'Age'] <- as.numeric(ph$`age:ch1`)

# 填补缺失值，采用均值填充
for (i in 1:nrow(dat0)) {
    dat0[i,][is.na(dat0[i,])] <- sum(dat0[i,], na.rm = T) / length(dat0[i,])
}
# 数据格式化
# 将表达矩阵，临床数据和注释表应全部捆绑到一个对象中，以协调元数据并在子集时进行测定。
GSE_SE <- SummarizedExperiment(assays = list(beta = dat0), colData = ph)

# 数据清洗
# 将表达矩阵减少到MEAT方法中使用的所有数据集共有的CPG
GSE_SE_clean <- clean_beta(SE = GSE_SE, version = "MEAT2.0")

#数据校准
# 该步骤协调了数据处理、样品制备、实验室间变异性方面的差异，以获得样品中表观遗传年龄的准确测量值。对数据进行探针和样品过滤，I型和II型探针的归一化以及批次效应的校正
GSE_SE_calibrated <- BMIQcalibration(SE = GSE_SE_clean, version = "MEAT2.0")

# 预测年龄
GSE_SE_epiage <- epiage_estimation(SE = GSE_SE_calibrated, version = "MEAT2.0", age_col_name = "Age")

# 输出年龄预测值
GSE_SE_epiage@colData@listData[["DNAmage"]]
