#### NO.14 MEAT Clocks ####

MEAT <- function(betaPath) {

  # get expression matrix data
  dat0 <- fread(betaPath)
  dat0 <- data.frame(dat0)
  rownames(dat0) <- dat0$V1
  dat0 <- dat0[,-1]

  # get MEAT2.0 156 cpg
  data("CpGs_in_MEAT2.0",envir = environment())

  # fill missing cpg row 0.5
  dispos <- setdiff(CpGs_in_MEAT2.0$CpGs_in_MEAT2.0$CpG[-1],rownames(dat0))
  dis <- matrix(data=0.5, nrow = length(dispos), ncol = length(colnames(dat0)), byrow = FALSE, dimnames = list(dispos,colnames(dat0)))
  dis <- data.frame(dis)
  dat0 <- rbind(dat0,dis)

  GSE_SE <- SummarizedExperiment(assays = list(beta = dat0))
  GSE_SE_clean <- clean_beta(SE = GSE_SE, version = "MEAT2.0")
  GSE_SE_calibrated <- BMIQcalibration(SE = GSE_SE_clean, version = "MEAT2.0")
  GSE_SE_epiage <- epiage_estimation(SE = GSE_SE_calibrated, version = "MEAT2.0")

  MEATAge <- GSE_SE_epiage@colData@listData[["DNAmage"]]

  return(MEATAge)
}


