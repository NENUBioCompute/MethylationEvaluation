library(GEOquery)

setwd('/home/data/Download/')
data <- getGEO("GSE41169", filename="GSE41169_series_matrix.txt.gz", destdir = '', AnnotGPL=F, getGPL = F)


pheno <- pData(data)

beta <- exprs(data)

colnames(beta)
pheno$geo_accession


write.csv(pheno,"/home/data/Raw/Meta/GSE41169_pheno.csv",row.names=FALSE)
write.csv(beta,"/home/data/Raw/Beta/GSE41169_beta.csv",row.names=FALSE)


data <- getGEO('GSE41169', destdir = '/home/data/Download/', AnnotGPL=F, getGPL = F)

beta <- exprs(data[[1]])

pheno <- pData(data[[1]])

