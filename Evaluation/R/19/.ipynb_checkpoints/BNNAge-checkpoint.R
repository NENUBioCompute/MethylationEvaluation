BNNAge <- function(betaPath) {
  library(methylclock)

  # get expression matrix data
  dat0 <- fread(betaPath)
  dat0 <- data.frame(dat0)
  rownames(dat0) <- dat0$V1
  dat0 <- dat0[,-1]


  dat0 <- data.frame(rownames(dat0), dat0)
  names(dat0)[names(dat0) == 'rownames.dat0.'] <- 'ProbeID'
  cpgs.missing <- checkClocks(dat0)

  # fill missing cpg row 0.5
  dispos <- cpgs.missing$Horvath
  dis <- matrix(data=0.5, nrow = length(dispos), ncol = length(colnames(dat0)), byrow = FALSE, dimnames = list(dispos,colnames(dat0)))
  dis <- data.frame(dis)
  dis$ProbeID <- rownames(dis)
  dat0 <- rbind(dat0,dis)

  age.gse <- DNAmAge(dat0, clocks='BNN')
  return(age.gse$BNN)
}


