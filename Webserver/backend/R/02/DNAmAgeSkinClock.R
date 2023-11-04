#### NO.02 Skin & Blood Clocks ####

SkinBloodAge <- function(beta_path, fill_value) {

  dat0 <- fread(beta_path,)
  dat0 <- data.frame(dat0)
  rownames(dat0) <- dat0$V1
  dat0 <- dat0[,-1]

  dat0 <- data.frame(rownames(dat0), dat0)
  names(dat0)[names(dat0) == 'rownames.dat0.'] <- 'ProbeID'

  #dat0: is a dataframe of beta values with colnames; ProbeID, Sample1, Sample2, etc
  #directory is path where datSkinClock.csv file is stored

  #R functions for transforming age
  adult.age1=20
  trafo= function(x,adult.age=adult.age1){x=(x+1)/(1+adult.age); y=ifelse(x<=1,log( x),x-1);y}
  anti.trafo= function(x,adult.age=adult.age1) {ifelse(x<0, (1+adult.age)*exp(x)-1,(1+adult.age)*x+adult.age) }

  datClock=read.csv("R/02/datSkinClock.csv")

  # fill missing cpg row fill_value
  dispos <- setdiff(datClock[-1,1], dat0$ProbeID)
  dis <- matrix(data=fill_value, nrow = length(dispos), ncol = length(colnames(dat0)), byrow = FALSE, dimnames = list(dispos,colnames(dat0)))
  dis <- data.frame(dis)
  dis$ProbeID <- rownames(dis)
  dat0 <- rbind(dat0,dis)

  selectCpGsClock=is.element(dat0[,1], as.character(datClock[-1,1])) #logical for x %in% y
  datMethClock0=data.frame(t(dat0[selectCpGsClock ,-1]))
  colnames(datMethClock0)=as.character(dat0[selectCpGsClock ,1])

  # Reality check: the following output should only contain numeric values.
  # Further, the column names should be CpG identifiers (cg numbers).
  datMethClock= data.frame(datMethClock0[as.character(datClock[-1,1])])

  # The number of rows should equal the number of samples (Illumina arrays)
  #dim(datMethClock)

  #Output DNAm age estimator for the skin & blood clock
  DNAmAgeSkin=as.numeric(anti.trafo(datClock$Coef[1]+as.matrix(datMethClock) %*% as.numeric(datClock$Coef[-1])))

  return(DNAmAgeSkin)
}
