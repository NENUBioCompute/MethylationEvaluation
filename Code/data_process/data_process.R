library(GEOquery)
library(methyLImp)
library(data.table)
library(stringr)
library(dplyr)



# 匹配样本名
match_sample_name <- function(GEOID, dat0) {
  gseData <- getGEO(GEOID, destdir = '.', AnnotGPL = FALSE, getGPL = F)
  ph = pData(gseData[[1]])
  gsm = c()
  titles = ph$title
  colsname = sub('X','',colnames(dat0))
  
  for (i in colsname) {
    if (i %in% titles) {
      print(which(titles == i))
      gsm = c(gsm, ph$geo_accession[which(titles == i)])
    } else {
      print(i)
    }
  }
  colsname(dat0) = gsm
  return(gsm)
}

# 调整表达矩阵顺序
adjust_expression_matrix <- function(dat0, meta) {
  data = cbind(dat0[,1])
  
  for(i in meta$ID) {
    if (i %in% colnames(dat0)) {
      data = cbind(data, dat0[which(colnames(dat0) == i)])
    } else {
      print(i)
    }
  }
  data = data[,-1]
  return(data)
}

# 调整头文件顺序
adjust_meta_data <- function(dat0, meta) {
  newMeta = rbind(meta[1,])
  
  for(i in gsm) {
    if (i %in% meta$ID) {
      newMeta = rbind(newMeta, meta[which(meta$ID == i),])
    } else {
      print(i)
    }
  }
  
  newMeta = newMeta[-1,]
  return(newMeta)
}

# 删除样本
delete_sample <- function(dat0) {
  for (i in colnames(dat0)) {
    if (i %in% meta$ID){
    } else {
      print(i)
      dat0 = select(dat0, -i)
    }
  }
  return(dat0)
}

# 填充缺失值
fill_NAvalue <- function(dat0) {
  dat0 = t(dat0)
  dat0 = methyLImp::methyLImp(dat0)
  dat0 = t(dat0)
  return(dat0)
}


