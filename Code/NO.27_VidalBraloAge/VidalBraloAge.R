# 导入所需要的包
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
for (i in 1:nrow(dat0)) {
  dat0[i,][is.na(dat0[i,])] <- sum(dat0[i,], na.rm = T) / length(dat0[i,])
}

# 读取方法使用的cpg位点数据
Weights = read.csv("D:/DNA Methylation/DNAmClock/VidalBraloAge/VidalBralo_weights.csv")
# cpg位点名称
Weights$probeID = as.character(Weights$probeID)
# 位点的权重系数
Weights$Coefficient = as.numeric(as.character(Weights$Coefficient))

# 表达矩阵与权重中的cpg位点进行匹配
selectCpGsClock = dat0$ProbeID %in% Weights$probeID #logical for x %in% y

# 输出是否有cpg位点缺失
print("calculating score for.. Vidal-Bralo DNAm Age")
print(paste0("number of probes missing.. ", print((length(Weights$probeID) - 1) - sum(selectCpGsClock)))) #+1 to account for intercept term

# 提取出表达矩阵中只包含方法所用cpg位点的矩阵
datMethClock0 = data.frame(t(dat0[selectCpGsClock, -1]))
colnames(datMethClock0) = as.character(dat0$ProbeID[selectCpGsClock])

Weights2 = Weights[Weights$probeID %in% c("Intercept", colnames(datMethClock0)),]
datMethClock = datMethClock0[, match(Weights2$probeID[-1], colnames(datMethClock0))]
datMethClock = as.data.frame(lapply(datMethClock, as.numeric))
# 计算预测年龄并输出
VidalBraloAge = as.numeric(Weights2$Coefficient[1] + (as.matrix(datMethClock) %*% as.numeric(Weights2$Coefficient[-1])))
VidalBraloAge
