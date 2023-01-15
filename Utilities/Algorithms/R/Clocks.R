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


source('/home/zongxizeng/methyTest/R/01/Horvath.R')
source('/home/zongxizeng/methyTest/R/02/DNAmAgeSkinClock.R')
source('/home/zongxizeng/methyTest/R/03/ZhangAge.R')
source('/home/zongxizeng/methyTest/R/04/Hannum.R')
source('/home/zongxizeng/methyTest/R/05/WeidnerAge.R')
source('/home/zongxizeng/methyTest/R/06/LinAge.R')
source('/home/zongxizeng/methyTest/R/08/PedBE.R')
source('/home/zongxizeng/methyTest/R/14/MEAT.R')
source('/home/zongxizeng/methyTest/R/17/Levine.R')
source('/home/zongxizeng/methyTest/R/19/BNNAge.R')
source('/home/zongxizeng/methyTest/R/24/CorticalClock.R')
source('/home/zongxizeng/methyTest/R/27/VidalBraloAge.R')


ClocksTest <- function (GEOID) {
  # 读取头文件
  ph_name = paste('/home/data/Standardized/mapped_lv3/', GEOID, sep = "", collapse = NULL)
  ph_name = paste(ph_name, '_pheno.csv', sep = "", collapse = NULL)
  ph = fread(ph_name)
  ph <- data.frame(ph)

  # 读取表达矩阵csv
  name = paste('/home/data/Standardized/express/', GEOID, sep = "", collapse = NULL)
  name <- paste(name, '_beta.csv', sep = "", collapse = NULL)
  dat0 <- fread(name)
  dat0 <- data.frame(dat0)
  rownames(dat0) = dat0$V1
  dat0 <- dat0[,-1]

  print(colnames(dat0) == ph$ID)

  print('================NO.14=====================')
  MEATAge = MEAT(dat0, ph) # NO.14
  print('================NO.01=====================')
  HorvathAge = Horvath(dat0) # NO.1
  print('================NO.02=====================')
  SkinBloodAge = SkinBloodAge(dat0) # NO.2
  print('================NO.03=====================')
  ZhangAge = ZhangAge(dat0, ph) # NO.3
  print('================NO.04=====================')
  HannumAge = Hannum(dat0) # NO.4
  print('================NO.05=====================')
  WeidnerAge = WeidnerAge(dat0) # NO.5
  print('================NO.06=====================')
  LinAge = LinAge(dat0) # NO.6
  print('================NO.08=====================')
  PedBEAge = PedBE(dat0) # NO.8
  print('================NO.17=====================')
  LevineAge = Levine(dat0) # NO.17
  print('================NO.19=====================')
  BNNAge = BNNAge(dat0, ph) # NO.19
  print('================NO.24=====================')
  CorticalClockAge = CorticalClock(dat0, ph) # NO.24
  print('================NO.27=====================')
  VidalBraloAge = VidalBraloAge(dat0) # NO.27

  df = data.frame(
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

