#### NO.04 Hannum Clocks ####

Hannum <- function(dat0){
  dat0 <- data.frame(rownames(dat0), dat0)
  names(dat0)[names(dat0) == 'rownames.dat0.'] <- 'ProbeID'

  datClock = read.table("/home/zongxizeng/methyTest/R/04/Hannum_TableS2_71probes.txt",header=T,sep="\t")

  #若缺少整个cpg位点(补0.5值)--起
  #取出缺少的cpg位点
  dispos <- setdiff(datClock$Marker,dat0$ProbeID)
  #建立缺少的cpg矩阵
  dis <- matrix(data=0.5, nrow = length(dispos), ncol = length(colnames(dat0)), byrow = FALSE, dimnames = list(dispos,colnames(dat0)))
  dis <- data.frame(dis)
  dis$ProbeID <- rownames(dis)
  #dis <- dis[-1,]
  #合并两个（按行）
  dat0 <- rbind(dat0,dis)
  #若缺少整个cpg位点--终

  selectCpGsClock = dat0$ProbeID %in% datClock$Marker #logical for x %in% y
  print("calculating score for.. Hannum DNAm age")
  print(paste0("number of probes missing..",print((length(datClock$Marker)-1) - sum(selectCpGsClock)))) #+1 to account for intercept term

  datMethClock0=data.frame(t(dat0[selectCpGsClock ,-1]))
  colnames(datMethClock0) = as.character(dat0$ProbeID[selectCpGsClock])

  datClock2 = datClock[datClock$Marker %in% colnames(datMethClock0),]
  datMethClock= datMethClock0[,match(datClock2$Marker,colnames(datMethClock0))]

  Hannum=as.numeric(as.matrix(datMethClock) %*% as.numeric(datClock2$Coefficient))
  return(Hannum)
}