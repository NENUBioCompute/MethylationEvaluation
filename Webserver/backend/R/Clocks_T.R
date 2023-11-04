# Title     : TODO
# Objective : TODO
# Created by: zxz
# Created on: 2023/1/5

library(data.table)


ClocksTest <- function (GEOID) {
  # get pheno data
  ph_name <- paste('/home/data/Standardized/pheno/', GEOID, sep = "", collapse = NULL)
  ph_name <- paste(ph_name, '_pheno.csv', sep = "", collapse = NULL)
  ph <- fread(ph_name)
  ph <- data.frame(ph)
  ph[is.na(ph)] <- ""


  df <- data.frame(
    ID = ph$ID,
    Age = as.numeric(ph$Age),
    Age_unit = ph$Age_unit,
    Tissue = ph$Tissue,
    Condition = ph$Condition,
    Disease = ph$Disease,
    Gender = ph$Gender,
    Race = ph$Race,
    platform = ph$Platform
  )

  return(df)
}

