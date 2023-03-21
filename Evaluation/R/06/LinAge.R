
LinAge <- function(betaPath) {
  dat0 <- fread(betaPath)
  dat0 <- data.frame(dat0)
  rownames(dat0) <- dat0$V1
  dat0 <- dat0[,-1]
  dat0 <- data.frame(rownames(dat0), dat0)
  names(dat0)[names(dat0) == 'rownames.dat0.'] <- 'ProbeID'

  # 读入权重文件
  Weights=read.csv("/home/zongxizeng/methyTest/R/06/Lin_Weights.csv")

  # fill missing cpg row 0.5
  dispos <- setdiff(Weights$probeID, dat0$ProbeID)
  dis <- matrix(data=0.5, nrow = length(dispos), ncol = length(colnames(dat0)), byrow = FALSE, dimnames = list(dispos,colnames(dat0)))
  dis <- data.frame(dis)
  dis$ProbeID <- rownames(dis)
  dat0 <- rbind(dat0,dis)

  Weights$probeID = as.character(Weights$probeID)
  Weights$Coefficient = as.numeric(as.character(Weights$Coefficient))
  selectCpGsClock = dat0$ProbeID %in% Weights$probeID #logical for x %in% y

  print("calculating score for.. Lin DNAm Age")
  print(paste0("number of probes missing.. ",
                print((length(Weights$probeID)-1) - sum(selectCpGsClock)))) #+1 to account for intercept term

  datMethClock0=data.frame(t(dat0[selectCpGsClock ,-1]))
  colnames(datMethClock0) = as.character(dat0$ProbeID[selectCpGsClock])

  # Weights2 = Weights[Weights$probeID %in% c("Intercept",colnames(datMethClock0)),]
  datMethClock= datMethClock0[,match(Weights$probeID[-1],colnames(datMethClock0))]

  LinAge=as.numeric(Weights$Coefficient[1] + (as.matrix(datMethClock) %*% as.numeric(Weights$Coefficient[-1])))

  return(LinAge)
}
