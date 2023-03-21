# CorticalClock<-function(betas, pheno){
CorticalClock <- function(betaPath) {

  # get expression matrix data
  dat0 <- fread(betaPath)
  dat0 <- data.frame(dat0)
  rownames(dat0) <- dat0$V1
  dat0 <- dat0[,-1]

  # read in cortical clock coeffs
  braincoef<-read.table("/home/zongxizeng/MethylationEvaluation/Evaluation/R/24/CorticalClockCoefs.txt", stringsAsFactor=F,header=T)
  braincoef$probe<-as.character(braincoef$probe)

  # fill missing cpg row 0.5
  dispos <- setdiff(braincoef$probe, rownames(dat0))
  dis <- matrix(data=0.5, nrow = length(dispos), ncol = length(colnames(dat0)), byrow = FALSE, dimnames = list(dispos,colnames(dat0)))
  dis <- data.frame(dis)
  dat0 <- rbind(dat0,dis)

  betas <- dat0
  # find the overlap between the probes and your data
  overlap<-braincoef[which(braincoef$probe %in% rownames(betas)),]
  if (nrow(overlap) < nrow(braincoef) ){
    print("some probes are missing, we will need to impute values here - the final predictions will be less accurate")
  } else {
    print("all the probes overlap between your data and the clock probes - no need for imputing missing values")
  }

  ##############################################################################################################################
  ############# add reference betas to the missing probes (average DNAm across 700 control cortical samples)                 ###
  ### imputation method adapted from:  https://github.com/qzhang314/DNAm-based-age-predictor                                 ###
  ### cite: Zhang, Q., Vallerga, C. L., Walker, R. M., Lin, T., Henders, A. K., Montgomery, G. W., ... & Pitcher, T. (2019). ###
  ### Improved precision of epigenetic clock estimates across tissues and its implication for biological ageing.             ###
  ### Genome medicine, 11(1), 1-11.                                                                                          ###
  ##############################################################################################################################

  if (length(overlap) < nrow(braincoef)) {
    # transform betas to be cpg in col
    betas<-t(betas)

    # read in ref data and match
    load("/home/zongxizeng/MethylationEvaluation/Evaluation/R/24/Ref_DNAm_brain_values.rdat")
    ref<-ref[which(names(ref) %in% braincoef$probe) , drop=F]


    betas<-betas[,colnames(betas)%in%names(ref)]
    if(ncol(betas)<length(ref)){
      missprobe<-setdiff(names(ref),colnames(betas))
      refmiss<-ref[missprobe]
      refmiss<-matrix(refmiss,ncol=length(missprobe),nrow=nrow(betas),byrow=T)
      refmiss<-as.data.frame(refmiss)
      colnames(refmiss)<-missprobe
      rownames(refmiss)<-rownames(betas)
      betas<-cbind(betas,refmiss)
    }

    betas<-betas[,names(ref)]     # match betas

    # for each probe replace missing value with mean value from reference betas
    # impute function
    imputeNA<-function(betas){
      betas[is.na(betas)]<-mean(betas,na.rm=T)
      return(betas)
    }

    ## apply function
    betasNona<-apply(betas,2,function(x) imputeNA(x))


    ## tranform betas - CpG in row
    betas<-t(betasNona)

    ##############################################################################################
    ############# Age prediciton! - weighted sum of coefficients plus the intercept ##############
    ##############################################################################################

    braincoef<-braincoef[match(rownames(betas), braincoef$probe),]
    brainpred<-braincoef$coef%*%betas+0.577682570446177

    ##############################################################################################
    ### anti transform the results (accounting for logarithmic relationship in ages 0-20)      ###
    ### Same as Horvath's: Horvath, S. (2013).                                                 ###
    ### DNA methylation age of human tissues and cell types. Genome biology, 14(10), 3156.     ###                                                              #######
    ##############################################################################################

    anti.trafo<-function(x,adult.age=20) { ifelse(x<0, (1+adult.age)*exp(x)-1, (1+adult.age)*x+adult.age) }
    brainpred<-anti.trafo(brainpred)

    #################################################
    #############  Save brain predictions ###########
    #################################################
    # pheno<-pheno[match(colnames(betas), pheno$ID),]
    brainpred<-as.numeric(brainpred)

    ## if not impuation for missing values:

  } else {

    ##############################################################################################
    ############# Age prediciton! - weighted sum of coefficients plus the intercept ##############
    ##############################################################################################

    braincoef<-braincoef[match(rownames(betas), braincoef$probe),]
    brainpred<-braincoef$coef%*%betas+0.577682570446177

    ##############################################################################################
    ### anti transform the results (accounting for logarithmic relationship in ages 0-20)      ###
    ### Same as Horvath's: Horvath, S. (2013).                                                 ###
    ### DNA methylation age of human tissues and cell types. Genome biology, 14(10), 3156.     ###                                                              #######
    ##############################################################################################

    anti.trafo<-function(x,adult.age=20) { ifelse(x<0, (1+adult.age)*exp(x)-1, (1+adult.age)*x+adult.age) }
    brainpred<-anti.trafo(brainpred)

    brainpred<-as.numeric(brainpred)
    # Save brain predictions
    # pheno<-pheno[match(colnames(betas), pheno$ID),]
    # pheno$brainpred<-as.numeric(brainpred)
    # pheno$Age<-as.numeric(pheno$Age)

  }
  return(brainpred)
}
