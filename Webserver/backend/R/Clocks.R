# Title     : TODO
# Objective : TODO
# Created by: zxz
# Created on: 2023/1/5

library(data.table)
library(MEAT)
library(SummarizedExperiment)
library(GO.db)
library(WGCNA)
library(impute)
library(sqldf)
library(BiocGenerics)
library(Biobase)
library(dplyr)
library(methylclock)
library(tibble)


source('../R/01/Horvath.R')
source('../R/02/DNAmAgeSkinClock.R')
source('../R/03/ZhangAge.R')
source('../R/04/Hannum.R')
source('../R/05/WeidnerAge.R')
source('../R/06/LinAge.R')
source('../R/08/PedBE.R')
source('../R/14/MEAT.R')
source('../R/17/Levine.R')
source('../R/19/BNNAge.R')
source('../R/24/CorticalClock.R')
source('../R/27/VidalBraloAge.R')


ClocksTest <- function (GEOID) {
  # get pheno data
  ph_name <- paste('/home/data/Standardized/mapped_lv3/', GEOID, sep = "", collapse = NULL)
  ph_name <- paste(ph_name, '_pheno.csv', sep = "", collapse = NULL)
  ph <- fread(ph_name)
  ph <- data.frame(ph)
  ph[is.na(ph)] <- ""

  # get expression matrix data
  name <- paste('/home/data/Standardized/express/', GEOID, sep = "", collapse = NULL)
  name <- paste(name, '_beta.csv', sep = "", collapse = NULL)
  dat0 <- fread(name)
  dat0 <- data.frame(dat0)
  rownames(dat0) <- dat0$V1
  dat0 <- dat0[,-1]

  print(colnames(dat0) == ph$ID)

  len <- length(ph$Age) # age count

  # If the method cannot predict the age, the predicted age values are null.
  noPredAge <- rep(c(''), len)


  print('================NO.14=====================')
  MEATAge <- tryCatch({ MEAT(dat0, ph) }, warning = function(w){ noPredAge }, error = function(e){ noPredAge },finally = {}) # NO.14
  print('================NO.01=====================')
  HorvathAge <- tryCatch({ Horvath(dat0) }, warning = function(w){ noPredAge }, error = function(e){ noPredAge },finally = {}) # NO.1
  print('================NO.02=====================')
  SkinBloodAge <- tryCatch({ SkinBloodAge(dat0) }, warning = function(w){ noPredAge }, error = function(e){ noPredAge },finally = {}) # NO.2
  print('================NO.03=====================')
  ZhangAge <- tryCatch({ ZhangAge(dat0, ph) }, warning = function(w){ noPredAge }, error = function(e){ noPredAge },finally = {}) # NO.3
  print('================NO.04=====================')
  HannumAge <- tryCatch({ Hannum(dat0) }, warning = function(w){ noPredAge }, error = function(e){ noPredAge },finally = {}) # NO.4
  print('================NO.05=====================')
  WeidnerAge <- tryCatch({ WeidnerAge(dat0) }, warning = function(w){ noPredAge }, error = function(e){ noPredAge },finally = {}) # NO.5
  print('================NO.06=====================')
  LinAge <- tryCatch({ LinAge(dat0) }, warning = function(w){ noPredAge }, warning = function(w){ noPredAge }, error = function(e){ noPredAge },finally = {}) # NO.6
  print('================NO.08=====================')
  PedBEAge <- tryCatch({ PedBE(dat0) }, warning = function(w){ noPredAge }, error = function(e){ noPredAge },finally = {}) # NO.8
  print('================NO.17=====================')
  LevineAge <- tryCatch({ Levine(dat0) }, warning = function(w){ noPredAge }, error = function(e){ noPredAge },finally = {}) # NO.17
  print('================NO.19=====================')
  BNNAge <- tryCatch({ BNNAge(dat0, ph) }, warning = function(w){ noPredAge }, error = function(e){ noPredAge },finally = {}) # NO.19
  print('================NO.24=====================')
  CorticalClockAge <- tryCatch({ CorticalClock(dat0, ph) }, warning = function(w){ noPredAge }, error = function(e){ noPredAge },finally = {}) # NO.24
  print('================NO.27=====================')
  VidalBraloAge <- tryCatch({ VidalBraloAge(dat0) }, warning = function(w){ noPredAge }, error = function(e){ noPredAge },finally = {}) # NO.27

  df <- data.frame(
    ID = ph$ID,
    Age = as.numeric(ph$Age),
    Age_unit = ph$Age_unit,
    Tissue = ph$Tissue,
    Condition = ph$Condition,
    Disease = ph$Disease,
    Gender = ph$Gender,
    Race = ph$Race,
    #platform = ph$Platform,
    SkinBloodAge = SkinBloodAge,
    HannumAge = HannumAge,
    WeidnerAge = WeidnerAge,
    LinAge = LinAge,
    PedBEAge = PedBEAge,
    MEATAge = MEATAge,
    LevineAge = LevineAge,
    CorticalClockAge = CorticalClockAge,
    VidalBraloAge = VidalBraloAge,
    HorvathAge = HorvathAge,
    ZhangAge = ZhangAge,
    BNNAge = BNNAge
  )

  return(df)
}

