# VidalBraloAge <- function(dat0) {
VidalBraloAge <- function(betaPath) {

  # get expression matrix data
  dat0 <- fread(betaPath)
  dat0 <- data.frame(dat0)
  rownames(dat0) <- dat0$V1
  dat0 <- dat0[,-1]

  # dat0: is a dataframe of beta values with colnames; ProbeID, Sample1, Sample2, etc
  dat0 <- data.frame(rownames(dat0), dat0)
  names(dat0)[names(dat0) == 'rownames.dat0.'] <- 'ProbeID'

  # directory is path where Zhang_elastic_weights.csv file is stored
  Weights = read.csv("/home/zongxizeng/methyTest/R/VidalBralo_weights.csv")
  Weights$probeID = as.character(Weights$probeID)
  Weights$Coefficient = as.numeric(as.character(Weights$Coefficient))

  # fill missing cpg row 0.5
  dispos <- setdiff(Weights$probeID[-1], dat0$ProbeID)
  dis <- matrix(data=0.5, nrow = length(dispos), ncol = length(colnames(dat0)), byrow = FALSE, dimnames = list(dispos,colnames(dat0)))
  dis <- data.frame(dis)
  dis$ProbeID <- rownames(dis)
  dat0 <- rbind(dat0,dis)

  selectCpGsClock = dat0$ProbeID %in% Weights$probeID #logical for x %in% y

  #print how many probes are missing
  print("calculating score for.. Vidal-Bralo DNAm Age")
  print(paste0("number of probes missing.. ", print((length(Weights$probeID) - 1) - sum(selectCpGsClock)))) #+1 to account for intercept term

  datMethClock0 = data.frame(t(dat0[selectCpGsClock, -1]))
  colnames(datMethClock0) = as.character(dat0$ProbeID[selectCpGsClock])

  #match order of CpGs with Weights
  Weights2 = Weights[Weights$probeID %in% c("Intercept", colnames(datMethClock0)),]
  datMethClock = datMethClock0[, match(Weights2$probeID[-1], colnames(datMethClock0))]
  # datMethClock = as.data.frame(lapply(datMethClock, as.numeric))
  #Output DNAm age estimator for the VidalBraloAge clock
  VidalBraloAge = as.numeric(Weights$Coefficient[1] + (as.matrix(datMethClock) %*% as.numeric(Weights2$Coefficient[-1])))

  return(VidalBraloAge)

}