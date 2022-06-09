library(GEOquery)
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
  names(dat0)[names(dat0) == 'V1'] <- 'ProbeID'
  rownames(dat0) <- dat0$ProbeID
}
else {
  dat0 <- data.frame(rownames(dat0), dat0)
  names(dat0)[names(dat0) == 'rownames.dat0.'] <- 'ProbeID'
}

# 填补缺失值，采用均值填充
for (i in 1:ncol(dat0)){
  dat0[,i][is.na(dat0[,i])] <- 0.5
}


# 方法使用的3个cpg位点的权重
Weights = data.frame(CpG = c("Intercept", "cg02228185", "cg25809905", "cg17861230"),
                     Coefficient = c(38.0, -26.4, -23.7, 164.7))

# 表达矩阵与权重中的cpg位点进行匹配
selectCpGsClock = dat0$ProbeID %in% Weights$CpG[-1]

# 输出是否有cpg位点缺失
print("calculating score for.. Weidner DNAm Age")
print(paste0("number of probes missing.. ", (length(Weights$CpG[-1])) - sum(selectCpGsClock)))

datMethClock0 = data.frame(t(dat0[selectCpGsClock, -1]))
colnames(datMethClock0) = as.character(dat0$ProbeID[selectCpGsClock])

# match order of CpGs with datClock
Weights2 = Weights[Weights$CpG %in% c("Intercept", colnames(datMethClock0)),]
datMethClock = datMethClock0[, match(Weights2$CpG[-1], colnames(datMethClock0))]

# 输出年龄预测值
WeidnerAge = as.numeric(Weights2$Coefficient[1] + (as.matrix(datMethClock) %*% as.numeric(Weights2$Coefficient[-1])))
WeidnerAge
