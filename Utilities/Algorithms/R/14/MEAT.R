#### NO.14 MEAT Clocks ####

MEAT <- function(dat0, ph) {

  GSE_SE <- SummarizedExperiment(assays = list(beta = dat0), colData = ph)
  GSE_SE_clean <- clean_beta(SE = GSE_SE, version = "MEAT2.0")
  GSE_SE_calibrated <- BMIQcalibration(SE = GSE_SE_clean, version = "MEAT2.0")
  GSE_SE_epiage <- epiage_estimation(SE = GSE_SE_calibrated, version = "MEAT2.0", age_col_name = "Age")

  MEATAge = GSE_SE_epiage@colData@listData[["DNAmage"]]

  return(MEATAge)
}


