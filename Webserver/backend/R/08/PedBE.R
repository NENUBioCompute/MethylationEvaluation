
PedBE <- function(beta_path, fill_value) {

  dat0 <- fread(beta_path,)
  dat0 <- data.frame(dat0)
  rownames(dat0) <- dat0$V1
  dat0 <- dat0[,-1]

  dat0 <- data.frame(rownames(dat0), dat0)
  names(dat0)[names(dat0) == 'rownames.dat0.'] <- 'ProbeID'

  datClock=read.csv("R/08/datcoefInteresting94.csv")

  # fill missing cpg row fill_value
  dispos <- setdiff(datClock[-1,1], dat0$ProbeID)
  dis <- matrix(data=fill_value, nrow = length(dispos), ncol = length(colnames(dat0)), byrow = FALSE, dimnames = list(dispos,colnames(dat0)))
  dis <- data.frame(dis)
  dis$ProbeID <- rownames(dis)
  dat0 <- rbind(dat0,dis)

  datM=t(dat0[,-1])
  colnames(datM)=as.character(dat0[,1])
  anti.trafo= function(x,adult.age=20) {
    ifelse(x<0, (1+adult.age)*exp(x)-1, (1+adult.age)*x+adult.age) }


  selectCpGsClock=is.element(dimnames(datM)[[2]], as.character(datClock[,1][-1]))
  datMethClock0=data.frame(datM[,selectCpGsClock])
  datMethClock= data.frame(datMethClock0[as.character(datClock[,1][-1])])

  PedBE_age=as.numeric(anti.trafo(datClock[1,2]+as.numeric(as.matrix(datMethClock)%*%as.numeric(datClock[,2][-1]))))

  return(PedBE_age)
}

