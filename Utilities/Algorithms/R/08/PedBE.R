PedBE <- function(dat0) {

  dat0 <- data.frame(rownames(dat0), dat0)
  names(dat0)[names(dat0) == 'rownames.dat0.'] <- 'ProbeID'
  
  datM=t(dat0[,-1])
  colnames(datM)=as.character(dat0[,1])
  anti.trafo= function(x,adult.age=20) {
    ifelse(x<0, (1+adult.age)*exp(x)-1, (1+adult.age)*x+adult.age) }
  datClock=read.csv("/home/zongxizeng/methyTest/R/datcoefInteresting94.csv")
  
  selectCpGsClock=is.element(dimnames(datM)[[2]], as.character(datClock[,1][-1]))
  datMethClock0=data.frame(datM[,selectCpGsClock])
  sum(selectCpGsClock)

  datMethClock= data.frame(datMethClock0[as.character(datClock[,1][-1])])
  
  PedBE_age=as.numeric(anti.trafo(datClock[1,2]+as.numeric(as.matrix(datMethClock)%*%as.numeric(datClock[,2][-1]))))

  return(PedBE_age)
}

