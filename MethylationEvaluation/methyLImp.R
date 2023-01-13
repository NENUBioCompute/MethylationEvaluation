methyLImp <- function (dat0) {


  dat0 = data.frame(dat0)
  print(dat0)
  cpgs = dat0[, 1]
  dat0 = dat0[, -1]
  dat0 = as.data.frame(lapply(dat0,as.numeric))
  print(dat0)

  if (sum(is.na(dat0)) > 0) {
    dat0 = t(dat0)
    dat0 = methyLImp::methyLImp(dat0)
    dat0 = t(dat0)
    rownames(dat0) = cpgs
    return(dat0)
  } else {
    rownames(dat0) = cpgs
    print(dat0)
    return(dat0)
  }


}

