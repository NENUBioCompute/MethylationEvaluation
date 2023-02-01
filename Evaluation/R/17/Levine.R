Levine <- function(dat0){
  dat0 <- data.frame(rownames(dat0), dat0)
  names(dat0)[names(dat0) == 'rownames.dat0.'] <- 'ProbeID'

  datClock=read.csv("/home/zongxizeng/methyTest/R/17/Horvath_phenoAge_weights.csv")

  #若缺少整个cpg位点(补0.5值)--起
  #取出缺少的cpg位点
  dispos <- setdiff(datClock$CpG,dat0$ProbeID)
  #建立缺少的cpg矩阵
  dis <- matrix(data=0.5, nrow = length(dispos), ncol = length(colnames(dat0)), byrow = FALSE, dimnames = list(dispos,colnames(dat0)))
  dis <- data.frame(dis)
  dis$ProbeID <- rownames(dis)
  #dis <- dis[-1,]
  #合并两个（按行）
  dat0 <- rbind(dat0,dis)
  #若缺少整个cpg位点--终

  selectCpGsClock = dat0$ProbeID %in% datClock$CpG[-1] #logical for x %in% y
  print("calculating score for.. Levine Pheno Age")
  print(paste0("number of probes missing..",print((length(datClock$CpG)-1) - sum(selectCpGsClock)))) #-1 to account for intercept term

  datMethClock0=data.frame(t(dat0[selectCpGsClock ,-1]))
  colnames(datMethClock0) = as.character(dat0$ProbeID[selectCpGsClock])

  datClock2 = datClock[datClock$CpG %in% c("Intercept",colnames(datMethClock0)),]
  datMethClock= datMethClock0[,match(datClock2$CpG[-1],colnames(datMethClock0))]

  LevineAge=as.numeric(datClock2$Coefficient[1] + (as.matrix(datMethClock) %*% as.numeric(datClock2$Coefficient[-1])))
  return(LevineAge)
}