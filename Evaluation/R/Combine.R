# Title     : TODO
# Objective : TODO
# Created by: zxz
# Created on: 2023/1/8

library(data.table)

Combine <- function (GEOID) {
  setwd('/home/data/Standardized/express/combine')

  files <- list.files()
  indexs = grep(GEOID, files)
  file = c()
  for (i in indexs) {
    file = c(file, files[i])
  }

  dat0 <- fread(file[1])
  dat0 <- data.frame(dat0)
  rownames(dat0)<-dat0$V1
  data <- dat0[,-1]

  for (i in seq(2, length(file))) {
    print(file[i])
    dat0 <- fread(file[i])
    dat0 <- data.frame(dat0)
    rownames(dat0)<-dat0$V1
    dat0 <- dat0[,-1]
    data = cbind(data, dat0)
  }

  print(colnames(data))
  name <- paste(GEOID, '_beta.csv', sep = "", collapse = NULL)
  write.csv(data, file = name)
}



