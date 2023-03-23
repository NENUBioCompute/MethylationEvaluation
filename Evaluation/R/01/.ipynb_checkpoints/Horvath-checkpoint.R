#### NO.01_fill Horvath Clocks ####

Horvath <- function(betaPath) {
  # get expression matrix data
  dat0 <- fread(betaPath)
  dat0 <- data.frame(dat0)
  rownames(dat0) <- dat0$V1
  dat0 <- dat0[,-1]

  source("/home/zongxizeng/MethylationEvaluation/Evaluation/R/01/NORMALIZATION.R")
  trafo= function(x,adult.age=20) { x<-(x+1)/(1+adult.age); y<-ifelse(x<=1, log( x),x-1);y }
  anti.trafo= function(x,adult.age=20) { ifelse(x<0, (1+adult.age)*exp(x)-1, (1+adult.age)*x+adult.age) }
  probeAnnotation21kdatMethUsed=read.csv("/home/zongxizeng/MethylationEvaluation/Evaluation/R/01/probeAnnotation21kdatMethUsed.csv")
  probeAnnotation27k=read.csv("/home/zongxizeng/MethylationEvaluation/Evaluation/R/01/datMiniAnnotation27k.csv")
  datClock=read.csv("/home/zongxizeng/MethylationEvaluation/Evaluation/R/01/AdditionalFile3.csv")

  dat0 <- data.frame(rownames(dat0), dat0)
  names(dat0)[names(dat0) == 'rownames.dat0.'] <- 'ProbeID'

  nSamples=dim(dat0)[[2]]-1
  nProbes= dim(dat0)[[1]]
  dat0[,1]= gsub(x=dat0 [,1],pattern="\"",replacement="")
  # create log data
  file.remove("./LogFile.txt")
  file.create("./LogFile.txt")
  DoNotProceed=FALSE
  cat(paste( "The methylation data set contains", nSamples, "samples (e.g. arrays) and ", nProbes, " probes."),file="LogFile.txt")

  if (nSamples==0) {
    DoNotProceed=TRUE
    cat(paste( "\n ERROR: There must be a data input error since there seem to be no samples.
               \n Make sure that you input a comma delimited file (.csv file)\n
               that can be read using the R command read.csv.sql . Samples correspond to
               columns in that file  ."), file="LogFile.txt",append=TRUE)
  }

  if (nSamples==0) {
    DoNotProceed=TRUE
    cat(paste( "\n ERROR: There must be a data input error since there seem to be no samples.
               \n Make sure that you input a comma delimited file (.csv file)\n that can be
               read using the R command read.csv.sql . Samples correspond to columns in that
               file  ."), file="LogFile.txt",append=TRUE)
  }

  if (  nSamples > nProbes  ) {
    cat(paste( "\n MAJOR WARNING: It worries me a lot that there are more samples than CpG probes.
               \n Make sure that probes correspond to rows and samples to columns.\n I wonder
               whether you want to first transpose the data and then resubmit them? In any event,
               I will proceed with the analysis."),file="LogFile.txt",append=TRUE)
  }

  if (  is.numeric(dat0[,1]) ) {
    DoNotProceed=TRUE
    cat(paste( "\n Error: The first column does not seem to contain probe identifiers
               (cg numbers from Illumina) since these entries are numeric values. Make
               sure that the first column of the file contains probe identifiers such as cg00000292.
               Instead it contains ", dat0[1:3,1]  ),file="LogFile.txt",append=TRUE)
  }

  if (  !is.character(dat0[,1]) ) {
    cat(paste( "\n Major Warning: The first column does not seem to contain probe identifiers
               (cg numbers from Illumina) since these entries are numeric values. Make sure
               that the first column of the file contains CpG probe identifiers such as cg00000292.
               Instead it contains ", dat0[1:3,1]  ),file="LogFile.txt",append=TRUE)
  }

  datout=data.frame(Error=c("Input error. Please check the log file for details","Please read
                            the instructions carefully."), Comment=c("", "email Steve Horvath."))

  nonNumericColumn=rep(FALSE, dim(dat0)[[2]]-1)
  for (i in 2:dim(dat0)[[2]] ){ nonNumericColumn[i-1]=! is.numeric(dat0[,i]) }
  if (  sum(nonNumericColumn) >0 ) { cat(paste( "\n MAJOR WARNING: Possible input error. The following samples contain non-numeric beta values: ", colnames(dat0)[-1][ nonNumericColumn], "\n Hint: Maybe you use the wrong symbols for missing data. Make sure to code missing values as NA in the Excel file. To proceed, I will force the entries into numeric values but make sure this makes sense.\n" ),file="LogFile.txt",append=TRUE)  }
  XchromosomalCpGs=as.character(probeAnnotation27k$Name[probeAnnotation27k$Chr=="X"])
  selectXchromosome=is.element(dat0[,1], XchromosomalCpGs )
  selectXchromosome[is.na(selectXchromosome)]=FALSE
  meanXchromosome=rep(NA, dim(dat0)[[2]]-1)
  if (   sum(selectXchromosome) >=500 )  {
  meanXchromosome= as.numeric(apply( as.matrix(dat0[selectXchromosome,-1]),2,mean,na.rm=TRUE)) }
  if (  sum(is.na(meanXchromosome)) >0 ) { cat(paste( "\n \n Comment: There are lots of missing values for X chromosomal probes for some of the samples. This is not a problem when it comes to estimating age but I cannot predict the gender of these samples.\n " ),file="LogFile.txt",append=TRUE)  }

  # fill missing cpg row 0.5
  dispos <- setdiff(probeAnnotation21kdatMethUsed$Name,dat0$ProbeID)
  dis <- matrix(data=0.5, nrow = length(dispos), ncol = length(colnames(dat0)), byrow = FALSE, dimnames = list(dispos,colnames(dat0)))
  dis <- data.frame(dis)
  dis$ProbeID <- rownames(dis)
  dat0 <- rbind(dat0,dis)

  # 2：Limit the data to 21k probes and make sure they are digital
  match1=match(probeAnnotation21kdatMethUsed$Name , dat0[,1])
  if(sum( is.na(match1))>0 ) stop(paste(sum( is.na(match1)), "CpG probes cannot be matched"))
  match2=na.omit(match1)


  dat1= dat0[match2,]
  asnumeric1=function(x) {as.numeric(as.character(x))}
  dat1[,-1]=apply(as.matrix(dat1[,-1]),2,asnumeric1)
  # 3：Create an output file named datout
  set.seed(1)

  # To normalize data or not (recommended)
  normalizeData=F

  fastImputation=FALSE
  #STEP 1: DEFINE QUALITY METRICS

  meanMethBySample =as.numeric(apply(as.matrix(dat1[,-1]),2,mean,na.rm=TRUE))
  minMethBySample   =as.numeric(apply(as.matrix(dat1[,-1]),2,min,na.rm=TRUE))
  maxMethBySample  =as.numeric(apply(as.matrix(dat1[,-1]),2,max,na.rm=TRUE))

  datMethUsed= t(dat1[,-1])
  colnames(datMethUsed)=as.character(dat1[,1])


  noMissingPerSample=apply(as.matrix(is.na(datMethUsed)),1,sum)
  # table(noMissingPerSample)

  #STEP 2: Imputing
  if (! fastImputation & nSamples>1 & max(noMissingPerSample,na.rm=TRUE)<3000 ){

  # run the following code if there is at least one missing
  if ( max(noMissingPerSample,na.rm=TRUE)>0 ){
  dimnames1=dimnames(datMethUsed)
  datMethUsed= data.frame(t(impute.knn(t(datMethUsed))$data))
  dimnames(datMethUsed)=dimnames1
  } # end of if
  } # end of if (! fastImputation )

  if ( max(noMissingPerSample,na.rm=TRUE)>=3000 ) fastImputation=TRUE


  if ( fastImputation | nSamples==1 ){
  noMissingPerSample=apply(as.matrix(is.na(datMethUsed)),1,sum)
  table(noMissingPerSample)
  if ( max(noMissingPerSample,na.rm=TRUE)>0 & max(noMissingPerSample,na.rm=TRUE) >= 3000 ) {normalizeData=FALSE}

  # run the following code if there is at least one missing
  if ( max(noMissingPerSample,na.rm=TRUE)>0 & max(noMissingPerSample,na.rm=TRUE) < 3000 ){
  dimnames1=dimnames(datMethUsed)
  for (i in which(noMissingPerSample>0) ){
  selectMissing1=is.na(datMethUsed[i,])
  datMethUsed[i,selectMissing1] = as.numeric(probeAnnotation21kdatMethUsed$goldstandard2[selectMissing1])
  } # end of for loop
  dimnames(datMethUsed)=dimnames1
  } # end of if
  } # end of if (! fastImputation )

  # STEP 3: Data normalization (each sample requires about 8 seconds). It would be straightforward to parallelize this operation.

  if (normalizeData ){
  datMethUsedNormalized=BMIQcalibration(datM=datMethUsed,goldstandard.beta= probeAnnotation21kdatMethUsed$goldstandard2,plots=FALSE)
  }
  if (!normalizeData ){ datMethUsedNormalized=datMethUsed }
  rm(datMethUsed); gc()





  #STEP 4: Predict age and create a data frame for the output (referred to as datout)
  selectCpGsClock=is.element(dimnames(datMethUsedNormalized)[[2]], as.character(datClock$CpGmarker[-1]))
  if ( sum( selectCpGsClock) < dim(datClock)[[1]]-1 ) {stop("The CpGs listed in column 1 of the input data did not contain the CpGs needed for calculating DNAm age. Make sure to input cg numbers such as cg00075967.")}
  if ( sum( selectCpGsClock) > dim(datClock)[[1]]-1 ) {stop("ERROR: The CpGs listed in column 1 of the input data contain duplicate CpGs. Each row should report only one unique CpG marker (cg number).")}
  if (nSamples>1 ) {
  datMethClock0=data.frame(datMethUsedNormalized[,selectCpGsClock])
  datMethClock= data.frame(datMethClock0[ as.character(datClock$CpGmarker[-1])])
  dim(datMethClock)
  predictedAge=as.numeric(anti.trafo(datClock$CoefficientTraining[1]+as.matrix(datMethClock)%*% as.numeric(datClock$CoefficientTraining[-1])))
  } # end of if


  if (nSamples==1 ) {
  datMethUsedNormalized2=data.frame(rbind(datMethUsedNormalized,datMethUsedNormalized))
  datMethClock0=data.frame(datMethUsedNormalized2[,selectCpGsClock])
  datMethClock= data.frame(datMethClock0[ as.character(datClock$CpGmarker[-1])])
  dim(datMethClock)
  predictedAge=as.numeric(anti.trafo(datClock$CoefficientTraining[1]+as.matrix(datMethClock)%*% as.numeric(datClock$CoefficientTraining[-1])))
  predictedAge=predictedAge[1]
  } # end of if



  # Let's add comments to the age prediction
  Comment=ifelse ( predictedAge <0, "Negative DNAm age.", ifelse ( predictedAge >100, "Old DNAm age.", rep("",length(predictedAge))))

  Comment[is.na(predictedAge)]="Age prediction was not possible. "


  if ( sum( selectCpGsClock) < dim(datClock)[[1]]-1 ) {
  Comment=rep("ERROR: The CpGs listed in column 1 of the input data did not contain the CpGs needed for calculating DNAm age. Make sure to input cg numbers such as cg00075967.",length(predictedAge) )}


  if ( sum( selectCpGsClock) > dim(datClock)[[1]]-1 ) {
  Comment=rep("ERROR: The CpGs listed in column 1 of the input data contain duplicate CpGs. Each row should report only one unique CpG marker (cg number).",length(predictedAge) )}


  restSamples=-minMethBySample>0.05 | maxMethBySample>1.05;
  restSamples[is.na(restSamples)]=FALSE
  lab1="MAJOR WARNING: Probably you did not input beta values since either minMethBySample<-0.05 or maxMethBySample>1.05.";Comment[restSamples]= paste(Comment[restSamples],lab1)

  restSamples= noMissingPerSample >0 & noMissingPerSample <=100;lab1="WARNING: Some beta values were missing, see noMissingPerSample."; Comment[restSamples]= paste(Comment[restSamples],lab1)
  restSamples= noMissingPerSample >3000;lab1="MAJOR WARNING: More than 3k missing values!!"; Comment[restSamples]= paste(Comment[restSamples],lab1)

  restSamples= noMissingPerSample >100 & noMissingPerSample <=3000 ;lab1="MAJOR WARNING: noMissingPerSample>100"
  Comment[restSamples]= paste(Comment[restSamples],lab1)
  restSamples=meanMethBySample>.35;
  restSamples[is.na(restSamples)]=FALSE
  lab1="Warning: meanMethBySample is >0.35";Comment[restSamples]= paste(Comment[restSamples],lab1)
  restSamples=meanMethBySample<.25;
  restSamples[is.na(restSamples)]=FALSE; lab1="Warning: meanMethBySample is <0.25"
  Comment[restSamples]= paste(Comment[restSamples],lab1)
  datout=data.frame(SampleID=colnames(dat1)[-1], DNAmAge=predictedAge, Comment, noMissingPerSample,meanMethBySample, minMethBySample, maxMethBySample)



  if ( !is.null( meanXchromosome) ){

  if ( length( meanXchromosome)==dim(datout)[[1]] ){
  predictedGender=ifelse(meanXchromosome>.4,"female",
  ifelse(meanXchromosome<.38,"male","Unsure"))
  datout=data.frame(datout,predictedGender=predictedGender,meanXchromosome=meanXchromosome)

  } # end of if

   } # end of if
  # 4: result
  if (  sum(  datout$Comment  != "" )   ==0 ) { cat(paste( "\n The individual samples appear to be fine. "),file="LogFile.txt",append=TRUE)  }
  if (  sum(  datout$Comment != "" )   >0 ) { cat(paste( "\n Warnings were generated for the following samples.\n", datout[,1][datout$Comment != ""], "\n Hint: Check the output file for more details."),file="LogFile.txt",append=TRUE)  }

  DNAmAge=as.numeric(datout$DNAmAge)
  return(DNAmAge)
}