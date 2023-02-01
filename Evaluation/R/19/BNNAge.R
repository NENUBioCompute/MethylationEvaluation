BNNAge <- function (dat0, ph) {
  dat0 <- data.frame(rownames(dat0), dat0)
  names(dat0)[names(dat0) == 'rownames.dat0.'] <- 'ProbeID'

  age <- ph$Age
  age.gse <- methylclock::DNAmAge(dat0, age=age,toBetas=TRUE)
  return(age.gse$BNN)
}


