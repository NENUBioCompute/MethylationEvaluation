# NO.17 PhenoAge
PhenoAge <- function(betaPath, method_dir) {
  # setting working directory to method_dir
  setwd(method_dir)
  # loading data
  # get expression matrix data
  dat0 <- fread(betaPath)
  dat0 <- data.frame(dat0)
  rownames(dat0) <- dat0$V1
  dat0 <- dat0[,-1]

  dat0 <- data.frame(rownames(dat0), dat0)
  names(dat0)[names(dat0) == 'rownames.dat0.'] <- 'ProbeID'

  datClock=read.csv("Horvath_phenoAge_weights.csv")

  # fill missing cpg row 0.5
  dispos <- setdiff(datClock$CpG, dat0$ProbeID)
  dis <- matrix(data=0.5, nrow = length(dispos), ncol = length(colnames(dat0)), byrow = FALSE, dimnames = list(dispos,colnames(dat0)))
  dis <- data.frame(dis)
  dis$ProbeID <- rownames(dis)
  dat0 <- rbind(dat0,dis)

  selectCpGsClock = dat0$ProbeID %in% datClock$CpG[-1] #logical for x %in% y
  print("calculating score for.. Levine Pheno Age")
  print(paste0("number of probes missing..",print((length(datClock$CpG)-1) - sum(selectCpGsClock)))) #-1 to account for intercept term

  datMethClock0=data.frame(t(dat0[selectCpGsClock ,-1]))
  colnames(datMethClock0) = as.character(dat0$ProbeID[selectCpGsClock])

  # datClock2 = datClock[datClock$CpG %in% c("Intercept",colnames(datMethClock0)),]
  datMethClock= datMethClock0[,match(datClock$CpG[-1],colnames(datMethClock0))]

  LevineAge=as.numeric(datClock$Coefficient[1] + (as.matrix(datMethClock) %*% as.numeric(datClock$Coefficient[-1])))
  return(LevineAge)
}