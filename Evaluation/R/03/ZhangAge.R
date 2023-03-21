# Title     : TODO
# Objective : TODO
# Created by: zxz
# Created on: 2023/1/12

#### NO.03 Zhang Clocks ####
#ZhangAge <- function (dat0, ph) {
ZhangAge <- function (betaPath) {
  dat0 <- fread(betaPath)
  dat0 <- data.frame(dat0)
  rownames(dat0) <- dat0$V1
  dat0 <- dat0[,-1]

  read.table("/home/zongxizeng/MethylationEvaluation/Evaluation/R/03/blup.coef",stringsAsFactor=F,header=T)->blupcoef
  # fill missing cpg row 0.5
  dispos <- setdiff(blupcoef[,1][-1], rownames(dat0))
  dis <- matrix(data=0.5, nrow = length(dispos), ncol = length(colnames(dat0)), byrow = FALSE, dimnames = list(dispos,colnames(dat0)))
  dis <- data.frame(dis)
  dat0 <- rbind(dat0,dis)

  dat0 <- t(dat0)

  ############# for each probe, change to missing value to the mean value across all individuals #############
  addna<-function(methy){
    methy[is.na(methy)]<-mean(methy,na.rm=T)
    return(methy)
  }


  ############# 1. get the parameters ##################
  args<-commandArgs(TRUE)
  args<- as.character(args)

  ############# 2. data loading and QC ##################
  print("1. Data loading and QC")

  print("1.1 Reading the data")
  dat0 -> data        ########## IND * Probe, each row represents one individual, it should be "RAW BETA" DNA methylation value

  if(nrow(data) > ncol(data)){
    print("I guess you are using Probe in the row, data will be transformed!!!")
    data<-t(data)
  }

  print("1.2 Replacing missing values with mean value")
  dataNona<-apply(data,2,function(x) addna(x))   ###############  replace the NA with mean value for each probe

  dataNona<- dataNona[,apply(dataNona,2,function(x) sum(is.na(x)))!=nrow(dataNona)] ############ remove the probe when it has NA across all individuals
  print(paste0(ncol(data) - ncol(dataNona)," probe(s) is(are) removed since it has (they have) NA across all individuals"))


  print("1.3 Standardizing")
  #dataNona<-as.data.frame(lapply(dataNona, as.numeric))
  dataNona.norm<- apply(dataNona,1,scale)        ############### standardize the DNA methylation within each individual, remove the mean and divided by the SD of each individual     Probe * IND
  rownames(dataNona.norm)<-colnames(dataNona)


  ############# 3. get the coefficients of each probe from Elastic Net/BLUP method, !!!!WE HAVE TWO PREDICTORS!!!#############

  print("2. Loading predictors")
  read.table("/home/zongxizeng/MethylationEvaluation/Evaluation/R/03/en.coef",stringsAsFactor=F,header=T)->encoef
  read.table("/home/zongxizeng/MethylationEvaluation/Evaluation/R/03/blup.coef",stringsAsFactor=F,header=T)->blupcoef

  en_int<-encoef[1,2]
  blup_int<-blupcoef[1,2]

  encoef<-encoef[-1,]
  blupcoef<-blupcoef[-1,]

  rownames(encoef)<-encoef$probe
  rownames(blupcoef)<-blupcoef$probe

  ############# 4. get common probes between predictors and data ##############
  print("3. Checking misssing probes")

  encomm<- intersect(rownames(encoef),rownames(dataNona.norm))
  blupcomm<- intersect(rownames(blupcoef),rownames(dataNona.norm))

  endiff<- nrow(encoef) - length(encomm)
  blupdiff<- nrow(blupcoef) - length(blupcomm)

  print(paste0(endiff," probe(s) in Elastic Net predictor is(are) not in the data"))
  print(paste0(blupdiff," probe(s) in BLUP predictor is(are) not in the data"))
  print("BLUP can perform better if the number of missing probes is too large!")

  ############# 5. extract the common probes and do age prediction ###############
  print("4. Predicting")

  encoef<-encoef[encomm,]
  blupcoef<-blupcoef[blupcomm,]
  encoef$coef%*%dataNona.norm[encomm,]+en_int->enpred
  blupcoef$coef%*%dataNona.norm[blupcomm,]+blup_int->blupred


  ############# 6. Save the predicted result ###########
  blupred<-blupred[,rownames(dat0)]

  return(as.double(blupred))
}

