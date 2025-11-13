# ==============================================================
# Unified Methylation Data Parser
# Supports separate phenotype information, separate expression matrix, and mixed formats
# Supports CpG and ch. prefixed site names
# Enhanced GEO accession auto-detection (from file content or filename)
# Outputs standardized {GEO_accession}_beta.csv.gz and {GEO_accession}_pheno.xlsx
# ==============================================================

parse_methylation_data <- function(input_path = "DownloadList.txt",
                                   output_dir = "parsed_output",
                                   idat_method = c("minfi", "sesame")) { 
  suppressPackageStartupMessages({
    library(stringr)
    library(data.table)
    library(tools)
    library(R.utils)
    library(dplyr)
  })
  
  # Check if writexl package is available for Excel output
  if (!requireNamespace("writexl", quietly = TRUE)) {
    stop("Please install the writexl package: install.packages('writexl')")
  }
  
  idat_method <- match.arg(idat_method)
  if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)

  # Step 1: read input paths
  if (file.exists(input_path) && grepl("\\.txt$", input_path)) {
    files <- readLines(input_path)
    files <- files[files != ""]
  } else {
    files <- input_path
  }

  for (f in files) {
    message("\n🧩 Processing file: ", f)
    if (!file.exists(f) && !dir.exists(f)) {
      warning("⚠️ File does not exist: ", f)
      next
    }

    # Initialize variables
    beta <- NULL
    pheno <- NULL
    geo_accession <- NULL
    geo_metadata <- NULL

    # ======================================================
    # 1️⃣ IDAT directory
    # ======================================================
    if (dir.exists(f) && length(list.files(f, pattern = "\\.idat$", ignore.case = TRUE)) > 0) {
      message("📁 Detected IDAT directory, using ", idat_method)
      
      if (!requireNamespace("minfi", quietly = TRUE)) {
        stop("Please install the minfi package: install.packages('BiocManager'); BiocManager::install('minfi')")
      }
      
      targets <- tryCatch(minfi::read.metharray.sheet(f), error = function(e) NULL)
      if (is.null(targets)) {
        warning("⚠️ Unable to read IDAT sample sheet, skipping: ", f)
        next
      }
      
      rgSet <- minfi::read.metharray.exp(targets = targets)
      mSet <- minfi::preprocessNoob(rgSet)
      beta_raw <- minfi::getBeta(mSet)
      pheno_raw <- Biobase::pData(mSet)
      
      # Convert beta matrix format: first column as site names
      beta <- as.data.frame(beta_raw)
      beta <- cbind(CpG_Site = rownames(beta), beta)
      rownames(beta) <- NULL
      
      # Process phenotype data: keep all columns
      pheno <- as.data.frame(pheno_raw)
      if (!"SampleID" %in% colnames(pheno)) {
        pheno <- cbind(SampleID = rownames(pheno), pheno)
      }
      rownames(pheno) <- NULL
      
      # For IDAT files, use the directory name as the dataset name
      geo_accession <- basename(f)

    # ======================================================
    # 2️⃣ GEO / SeriesMatrix / mixed tables / CSV.GZ files
    # ======================================================
    } else if (grepl("series_matrix|soft|txt|csv", f, ignore.case = TRUE)) {
      message("🧠 Detected GEO or table file, attempting intelligent split...")
      
      # Read file content
      if (grepl("\\.gz$", f)) {
        con <- gzfile(f, "rt")
        lines <- readLines(con)
        close(con)
      } else {
        lines <- readLines(f)
      }
      
      # Extract GEO accession (!Series_geo_accession)
      geo_accession_line <- grep("^!Series_geo_accession", lines, value = TRUE)
      if (length(geo_accession_line) > 0) {
        geo_accession <- str_extract(geo_accession_line, 'GSE\\d+')
        if (is.na(geo_accession)) {
          # If no GSE number, try other extraction methods
          geo_accession <- gsub('^!Series_geo_accession\\s+', '', geo_accession_line)
          geo_accession <- gsub('\"', '', geo_accession)
          geo_accession <- gsub('\t', '', geo_accession)
        }
        message("🔍 Detected GEO accession from file content: ", geo_accession)
      }
      
      # If no GEO accession found from content, try extracting from filename
      if (is.null(geo_accession) || geo_accession == "") {
        geo_accession <- .extract_geo_accession_from_filename(f)
        if (!is.null(geo_accession)) {
          message("🔍 Detected GEO accession from filename: ", geo_accession)
        }
      }
      
      # If still no GEO accession found, use filename
      if (is.null(geo_accession) || geo_accession == "") {
        base_name <- tools::file_path_sans_ext(basename(f))
        if (grepl("\\.gz$", base_name)) {
          base_name <- tools::file_path_sans_ext(base_name)
        }
        geo_accession <- base_name
        message("⚠️ Unable to detect GEO accession, using filename: ", geo_accession)
      }
      
      # Check file type: if it's .csv.gz and no !Series_geo_accession, it might be a pure expression matrix
      is_pure_beta_matrix <- (grepl("\\.csv\\.gz$", f, ignore.case = TRUE) && 
                             length(grep("^!Series_", lines)) == 0)
      
      if (is_pure_beta_matrix) {
        message("📊 Detected pure expression matrix file (.csv.gz format with no GEO metadata)")
        # Directly read as data frame
        dt <- .read_with_auto_delimiter(f)
        
        if (!is.null(dt) && nrow(dt) > 0) {
          # Intelligent data format recognition
          result <- .split_beta_and_pheno(dt)
          beta <- result$beta
          pheno <- result$pheno
        }
      } else {
        # Standard GEO file processing workflow
        # Extract GEO metadata (lines starting with !Sample_)
        metadata_lines <- grep("^!Sample_", lines, value = TRUE)
        if (length(metadata_lines) > 0) {
          geo_metadata <- .parse_geo_metadata(metadata_lines)
        }
        
        # Extract Series metadata (lines starting with !Series_, excluding geo_accession)
        series_metadata_lines <- grep("^!Series_", lines, value = TRUE)
        series_metadata_lines <- series_metadata_lines[!grepl("^!Series_geo_accession", series_metadata_lines)]
        if (length(series_metadata_lines) > 0) {
          series_metadata <- .parse_series_metadata(series_metadata_lines)
          # Add Series metadata to phenotype data (same for each sample)
          if (!is.null(series_metadata) && nrow(series_metadata) > 0) {
            if (is.null(geo_metadata)) {
              geo_metadata <- series_metadata
            } else {
              geo_metadata <- cbind(geo_metadata, series_metadata[rep(1, nrow(geo_metadata)), ])
            }
          }
        }
        
        # Check if there is a data table section
        data_start <- grep("^!series_matrix_table_begin", lines)
        data_end <- grep("^!series_matrix_table_end", lines)
        
        if (length(data_start) > 0 && length(data_end) > 0) {
          # Extract data table section
          data_lines <- lines[(data_start + 1):(data_end - 1)]
          if (length(data_lines) > 0) {
            writeLines(data_lines, "tmp_matrix.txt")
            dt <- tryCatch({
              fread("tmp_matrix.txt", header = TRUE, data.table = FALSE, sep = "\t")
            }, error = function(e) {
              # If tab delimiter fails, try auto-detect delimiter
              .read_with_auto_delimiter("tmp_matrix.txt")
            })
            unlink("tmp_matrix.txt")
          } else {
            dt <- NULL
          }
        } else {
          # If not standard GEO format, try reading directly as table
          message("🔍 Non-standard GEO format, attempting to read table directly...")
          dt <- .read_with_auto_delimiter(f)
        }
        
        # Intelligent data splitting (if data table exists)
        if (!is.null(dt) && nrow(dt) > 0) {
          result <- .split_beta_and_pheno(dt, geo_metadata)
          beta <- result$beta
          pheno <- result$pheno
        } else {
          # Only metadata, no data table
          message("ℹ️ File contains only metadata, no expression matrix data")
          pheno <- geo_metadata
        }
      }
      
    } else {
      warning("⚠️ Unrecognized file type, skipping: ", f)
      next
    }

    # ======================================================
    # 3️⃣ Output results - using GEO accession as filename
    # ======================================================
    
    # Clean GEO accession to ensure it is a valid filename
    geo_accession_clean <- gsub("[^A-Za-z0-9._-]", "_", geo_accession)
    
    # Output beta matrix (if exists)
    if (!is.null(beta) && nrow(beta) > 0 && ncol(beta) > 1) {
      beta_out <- file.path(output_dir, paste0(geo_accession_clean, "_beta.csv.gz"))
      
      # Ensure the first column name is "CpG_Site"
      if (!"CpG_Site" %in% colnames(beta)) {
        if (ncol(beta) > 0) {
          colnames(beta)[1] <- "CpG_Site"
        }
      }
      
      # Ensure subsequent column names are sample IDs
      sample_cols <- setdiff(colnames(beta), "CpG_Site")
      if (length(sample_cols) > 0) {
        # Clean sample column names: remove quotes and other special characters
        clean_sample_names <- gsub('\"', '', sample_cols)
        colnames(beta)[-1] <- clean_sample_names
      }
      
      # Use gzfile connection to write compressed file
      gz_con <- gzfile(beta_out, "w")
      write.csv(beta, gz_con, quote = FALSE, row.names = FALSE)
      close(gz_con)
      
      message("✅ Beta matrix output: ", basename(beta_out), 
              " (", nrow(beta), " CpG sites, ", ncol(beta)-1, " samples)")
    } else {
      message("ℹ️ No expression matrix data detected, skipping beta matrix output")
    }
    
    # Output phenotype data (if exists)
    if (!is.null(pheno) && nrow(pheno) > 0) {
      pheno_out <- file.path(output_dir, paste0(geo_accession_clean, "_pheno.xlsx"))
      
      # Process phenotype data according to the optimization requirements
      pheno <- .process_pheno_data(pheno)
      
      # Ensure there is a SampleID column
      if (!"SampleID" %in% colnames(pheno)) {
        if (ncol(pheno) > 0) {
          # Try to find a column containing sample IDs
          sample_id_col <- which(sapply(pheno, function(x) any(grepl("^GSM", x))))
          if (length(sample_id_col) > 0) {
            colnames(pheno)[sample_id_col[1]] <- "SampleID"
          } else {
            # If no GSM sample IDs, create sample IDs based on column names
            if (exists("beta") && !is.null(beta) && ncol(beta) > 1) {
              sample_ids <- colnames(beta)[-1]
              pheno <- data.frame(SampleID = sample_ids, stringsAsFactors = FALSE)
            } else {
              pheno <- cbind(SampleID = paste0("Sample", 1:nrow(pheno)), pheno)
            }
          }
        } else {
          pheno <- data.frame(SampleID = paste0("Sample", 1:nrow(pheno)))
        }
      }
      
      # Clean column names: remove special characters but preserve original information
      clean_colnames <- gsub('^!Sample_', '', colnames(pheno))
      clean_colnames <- gsub('^!Series_', 'Series_', clean_colnames)
      clean_colnames <- gsub('\"', '', clean_colnames)
      
      # Handle empty column names and ensure uniqueness
      clean_colnames <- ifelse(clean_colnames == "", paste0("Column", seq_along(clean_colnames)), clean_colnames)
      clean_colnames <- make.names(clean_colnames, unique = TRUE)
      colnames(pheno) <- clean_colnames

      # If ncol(pheno) has only one column, skip phenotype output
      if (ncol(pheno) == 1) {
        message("ℹ️ Phenotype data contains only SampleID column, skipping phenotype output")
        next
      }
      
      # Write to Excel file using writexl package
      writexl::write_xlsx(pheno, pheno_out)
      
      message("✅ Phenotype data output: ", basename(pheno_out), 
              " (", nrow(pheno), " samples, ", ncol(pheno), " variables)")
    } else {
      message("ℹ️ No phenotype data detected, skipping phenotype output")
    }
  }

  message("\n🎉 All files parsed successfully! Output directory: ", normalizePath(output_dir))
}

# ==============================================================
# Helper functions
# ==============================================================

# Extract GEO accession from filename
.extract_geo_accession_from_filename <- function(filename) {
  # Try multiple patterns to extract GSE number
  patterns <- c(
    "GSE\\d+",                    # Directly match GSE+number
    "acc=GSE\\d+",                # match acc=GSE12345
    "GSE\\d+%5F",                 # match GSE12345%5F (URL-encoded underscore)
    "%5FGSE\\d+%5F",              # match_GSE12345_
    "GSE\\d+_",                   # matchGSE12345_
    "_GSE\\d+"                    # match_GSE12345
  )
  
  for (pattern in patterns) {
    match <- str_extract(filename, pattern)
    if (!is.na(match)) {
      # Extract pure GSE number from the match
      geo_accession <- str_extract(match, "GSE\\d+")
      if (!is.na(geo_accession)) {
        return(geo_accession)
      }
    }
  }
  
  # If none of the above patterns match, return NULL
  return(NULL)
}

# Parse GEO sample metadata - COMPLETELY REWRITTEN to handle multiple characteristics properly
.parse_geo_metadata <- function(metadata_lines) {
  # Extract all metadata keys
  keys <- sub("^!Sample_(.*?)\t.*", "\\1", metadata_lines)
  unique_keys <- unique(keys)
  
  # Initialize result data frame
  result_df <- NULL
  
  # Process each unique key
  for (key in unique_keys) {
    # Get all lines for this key
    key_lines <- metadata_lines[keys == key]
    
    # Extract values for this key (remove the key part)
    values_list <- lapply(key_lines, function(line) {
      # Remove the key and tab
      value_part <- sub(paste0("^!Sample_", key, "\t"), "", line)
      # Split by tab and remove quotes
      values <- strsplit(value_part, "\t")[[1]]
      gsub('\"', '', values)
    })
    
    # For characteristics_ch1, we need special handling
    if (key == "characteristics_ch1") {
      # Process characteristics - each line contains multiple characteristics
      characteristics_list <- list()
      
      # For each sample, extract all characteristics
      for (sample_idx in seq_along(values_list[[1]])) {
        sample_chars <- list()
        
        # Collect all characteristics for this sample from all characteristic lines
        for (line_idx in seq_along(values_list)) {
          if (length(values_list[[line_idx]]) >= sample_idx) {
            char_value <- values_list[[line_idx]][sample_idx]
            if (!is.na(char_value) && char_value != "") {
              # Split by colon to extract field name and value
              if (grepl(":\\s*", char_value)) {
                split_val <- strsplit(char_value, ":\\s*")[[1]]
                if (length(split_val) >= 2) {
                  field_name <- trimws(split_val[1])
                  field_value <- trimws(paste(split_val[-1], collapse = ": "))
                  sample_chars[[field_name]] <- field_value
                }
              }
            }
          }
        }
        
        characteristics_list[[sample_idx]] <- sample_chars
      }
      
      # Convert to data frame columns
      all_field_names <- unique(unlist(lapply(characteristics_list, names)))
      
      for (field_name in all_field_names) {
        field_values <- sapply(characteristics_list, function(sample_chars) {
          if (!is.null(sample_chars[[field_name]])) {
            return(sample_chars[[field_name]])
          } else {
            return(NA)
          }
        })
        
        # Create safe column name
        safe_col_name <- make.names(field_name, unique = TRUE)
        
        if (is.null(result_df)) {
          result_df <- data.frame(field_values, stringsAsFactors = FALSE)
          colnames(result_df) <- safe_col_name
        } else {
          result_df[[safe_col_name]] <- field_values
        }
      }
      
    } else {
      # For regular keys, just use the values as is
      # We need to handle the case where there are multiple lines for the same key
      # by combining them appropriately
      
      if (length(values_list) == 1) {
        # Single line for this key
        values <- values_list[[1]]
      } else {
        # Multiple lines for this key - combine them
        # This handles cases like multiple !Sample_contributor lines
        values <- sapply(seq_along(values_list[[1]]), function(i) {
          line_values <- sapply(values_list, function(v) if (length(v) >= i) v[i] else NA)
          paste(na.omit(line_values), collapse = "; ")
        })
      }
      
      # Create safe column name
      safe_col_name <- make.names(key, unique = TRUE)
      
      if (is.null(result_df)) {
        result_df <- data.frame(values, stringsAsFactors = FALSE)
        colnames(result_df) <- safe_col_name
      } else {
        result_df[[safe_col_name]] <- values
      }
    }
  }
  
  # Ensure geo_accession column exists and is properly named
  if (!is.null(result_df) && "geo_accession" %in% colnames(result_df)) {
    # Rename to SampleID for consistency
    colnames(result_df)[colnames(result_df) == "geo_accession"] <- "SampleID"
  }
  
  # Ensure no empty column names
  if (!is.null(result_df)) {
    colnames(result_df) <- ifelse(colnames(result_df) == "", 
                                 paste0("Column", seq_len(ncol(result_df))),
                                 colnames(result_df))
  }
  
  return(result_df)
}

# Parse GEO Series Metadata
.parse_series_metadata <- function(metadata_lines) {
  metadata_list <- list()
  
  for (line in metadata_lines) {
    # Remove leading !Series_
    line_clean <- sub("^!Series_", "", line)
    
    # Split key-value pairs
    if (grepl("\t", line_clean)) {
      parts <- strsplit(line_clean, "\t")[[1]]
      key <- parts[1]
      values <- parts[-1]
      
      # Clean value: Remove quotes
      values_clean <- gsub('\"', '', values)
      
      # For Series metadata, usually only one value
      if (length(values_clean) > 0) {
        metadata_list[[key]] <- values_clean[1]
      }
    }
  }
  
  # Convert to single-row data frame
  if (length(metadata_list) > 0) {
    metadata_df <- as.data.frame(metadata_list, stringsAsFactors = FALSE)
    
    # Ensure no empty column names
    colnames(metadata_df) <- ifelse(colnames(metadata_df) == "", 
                                   paste0("Series_Column", seq_len(ncol(metadata_df))),
                                   colnames(metadata_df))
    
    return(metadata_df)
  }
  
  return(NULL)
}

# Auto-detect delimiter and read file
.read_with_auto_delimiter <- function(file_path) {
  # Read first few lines to detect delimiter
  if (grepl("\\.gz$", file_path)) {
    con <- gzfile(file_path, "rt")
    lines <- readLines(con, n = 10)
    close(con)
  } else {
    lines <- readLines(file_path, n = 10)
  }
  
  # Detect delimiter
  tab_count <- sum(str_count(lines, "\t"))
  comma_count <- sum(str_count(lines, ","))
  semicolon_count <- sum(str_count(lines, ";"))
  
  if (tab_count > comma_count && tab_count > semicolon_count) {
    sep <- "\t"
  } else if (semicolon_count > comma_count && semicolon_count > tab_count) {
    sep <- ";"
  } else {
    sep <- ","
  }
  
  message("🔍 Detected delimiter: ", dQuote(sep))
  
  # Use detected delimiter to read file
  if (grepl("\\.gz$", file_path)) {
    dt <- fread(file_path, header = TRUE, data.table = FALSE, sep = sep)
  } else {
    dt <- fread(file_path, header = TRUE, data.table = FALSE, sep = sep)
  }
  
  # Clean column names - remove empty names
  if (!is.null(dt)) {
    col_names <- colnames(dt)
    empty_cols <- col_names == ""
    if (any(empty_cols)) {
      col_names[empty_cols] <- paste0("Column", which(empty_cols))
      colnames(dt) <- col_names
    }
  }
  
  return(dt)
}

# Smart split of beta matrix and phenotype data
.split_beta_and_pheno <- function(dt, geo_metadata = NULL) {
  # Check if data frame is empty
  if (is.null(dt) || nrow(dt) == 0 || ncol(dt) == 0) {
    return(list(beta = NULL, pheno = geo_metadata))
  }
  
  # Clean column names - ensure no empty names
  colnames(dt) <- ifelse(colnames(dt) == "", 
                        paste0("Column", seq_len(ncol(dt))),
                        colnames(dt))
  
  # Identify methylation site rows (first column starts with cg or ch.)
  methyl_rows <- grep("^(cg|ch\\.)", dt[[1]], ignore.case = TRUE)
  
  if (length(methyl_rows) > 0) {
    # Case 1: Rows are methylation sites, columns are samples
    beta <- dt[methyl_rows, , drop = FALSE]
    
    # First column is site names, the rest are samples
    colnames(beta)[1] <- "CpG_Site"
    
    # Convert numeric columns
    for (i in 2:ncol(beta)) {
      beta[[i]] <- as.numeric(as.character(beta[[i]]))
    }
    
    # Extract non-methylation site rows as phenotype data
    non_methyl_rows <- setdiff(1:nrow(dt), methyl_rows)
    if (length(non_methyl_rows) > 0) {
      pheno_from_data <- dt[non_methyl_rows, , drop = FALSE]
      # Transpose: rows become samples, columns become variables
      pheno_from_data_t <- as.data.frame(t(pheno_from_data[-1]), stringsAsFactors = FALSE)
      colnames(pheno_from_data_t) <- pheno_from_data[[1]]
      pheno_from_data_t <- cbind(SampleID = rownames(pheno_from_data_t), pheno_from_data_t)
      rownames(pheno_from_data_t) <- NULL
    } else {
      pheno_from_data_t <- NULL
    }
    
  } else {
    # Case 2: Check if column names contain methylation sites
    methyl_cols <- grep("^(cg|ch\\.)", colnames(dt), ignore.case = TRUE)
    
    if (length(methyl_cols) > 0) {
      # Columns are methylation sites, rows are samples
      beta <- dt[, methyl_cols, drop = FALSE]
      beta <- as.data.frame(t(beta), stringsAsFactors = FALSE)
      beta <- cbind(CpG_Site = rownames(beta), beta)
      rownames(beta) <- NULL
      
      # Convert numeric columns
      for (i in 2:ncol(beta)) {
        beta[[i]] <- as.numeric(as.character(beta[[i]]))
      }
      
      # Extract non-methylation site columns as phenotype data
      non_methyl_cols <- setdiff(1:ncol(dt), methyl_cols)
      if (length(non_methyl_cols) > 0) {
        pheno_from_data <- dt[, non_methyl_cols, drop = FALSE]
        if (!"SampleID" %in% colnames(pheno_from_data)) {
          pheno_from_data <- cbind(SampleID = dt[[1]], pheno_from_data)
        }
      } else {
        pheno_from_data <- data.frame(SampleID = dt[[1]])
      }
      pheno_from_data_t <- pheno_from_data
      
    } else {
      # Unable to identify methylation sites, only phenotype data
      message("ℹ️ No methylation sites detected, file may contain only phenotype data")
      beta <- NULL
      pheno_from_data_t <- dt
    }
  }
  
  # Merge phenotype data
  if (!is.null(geo_metadata) && !is.null(pheno_from_data_t)) {
    # Merge GEO metadata and phenotype information extracted from data
    if ("SampleID" %in% colnames(pheno_from_data_t) && "SampleID" %in% colnames(geo_metadata)) {
      common_samples <- intersect(pheno_from_data_t$SampleID, geo_metadata$SampleID)
      if (length(common_samples) > 0) {
        pheno <- merge(pheno_from_data_t, geo_metadata, by = "SampleID", all = TRUE)
      } else {
        pheno <- cbind(pheno_from_data_t, geo_metadata)
      }
    } else {
      pheno <- cbind(pheno_from_data_t, geo_metadata)
    }
  } else if (!is.null(geo_metadata)) {
    pheno <- geo_metadata
  } else if (!is.null(pheno_from_data_t)) {
    pheno <- pheno_from_data_t
  } else {
    # Create basic phenotype data
    sample_ids <- if (exists("beta") && !is.null(beta) && ncol(beta) > 1) {
      colnames(beta)[-1]
    } else {
      paste0("Sample", 1:max(sapply(list(geo_metadata, pheno_from_data_t), 
                                   function(x) if (!is.null(x)) nrow(x) else 0)))
    }
    pheno <- data.frame(SampleID = sample_ids)
  }
  
  # Ensure no empty column names in final phenotype data
  colnames(pheno) <- ifelse(colnames(pheno) == "", 
                           paste0("Pheno_Column", seq_len(ncol(pheno))),
                           colnames(pheno))
  
  return(list(beta = beta, pheno = pheno))
}

# New function: Process phenotype data according to optimization requirements
.process_pheno_data <- function(pheno) {
  if (is.null(pheno) || nrow(pheno) == 0) return(pheno)
  
  # Create a copy to avoid modifying original data during iteration
  processed_pheno <- pheno
  
  # 1. Process each column to save unique values and handle naming conflicts
  col_names <- colnames(processed_pheno)
  unique_col_names <- character(length(col_names))
  
  for (i in seq_along(col_names)) {
    col_name <- col_names[i]
    col_data <- processed_pheno[[i]]
    
    # Remove NA, NULL, empty strings and other invalid values
    valid_data <- col_data[!is.na(col_data) & !is.null(col_data) & 
                           col_data != "" & !grepl("^\\s*$", col_data)]
    
    # Get unique values
    unique_vals <- unique(valid_data)
    
    # Create a safe column name
    safe_name <- make.names(col_name, unique = FALSE)
    
    # If the safe name already exists in our processed names, add suffix
    if (safe_name %in% unique_col_names[1:(i-1)]) {
      counter <- 1
      new_name <- paste0(safe_name, "_", counter)
      while (new_name %in% unique_col_names[1:(i-1)]) {
        counter <- counter + 1
        new_name <- paste0(safe_name, "_", counter)
      }
      safe_name <- new_name
    }
    
    unique_col_names[i] <- safe_name
  }
  
  colnames(processed_pheno) <- unique_col_names
  
  # 2. Handle columns with single colon where prefix is consistent across all rows
  new_columns <- list()
  cols_to_remove <- character(0)
  
  for (col_name in colnames(processed_pheno)) {
    col_data <- processed_pheno[[col_name]]
    
    # Check if column contains character data and has exactly one colon in each non-NA value
    if (is.character(col_data)) {
      non_na_data <- col_data[!is.na(col_data)]
      
      if (length(non_na_data) > 0) {
        # Count colons in each element
        colon_counts <- str_count(non_na_data, ":")
        
        # Check if all non-NA values have exactly one colon
        if (all(colon_counts == 1)) {
          # Split by colon
          split_data <- str_split_fixed(non_na_data, ":", 2)
          prefixes <- split_data[, 1]
          suffixes <- split_data[, 2]
          
          # Check if all prefixes are the same
          if (length(unique(prefixes)) == 1) {
            consistent_prefix <- unique(prefixes)[1]
            
            # Create new column name from the consistent prefix
            new_col_name <- make.names(consistent_prefix, unique = TRUE)
            
            # Ensure the new column name doesn't conflict with existing columns
            all_col_names <- c(colnames(processed_pheno), names(new_columns))
            if (new_col_name %in% all_col_names) {
              counter <- 1
              temp_name <- paste0(new_col_name, "_", counter)
              while (temp_name %in% all_col_names) {
                counter <- counter + 1
                temp_name <- paste0(new_col_name, "_", counter)
              }
              new_col_name <- temp_name
            }
            
            # Create the new column data (handle NAs properly)
            new_col_data <- rep(NA_character_, length(col_data))
            new_col_data[!is.na(col_data)] <- suffixes
            
            # Add to new columns list and mark original column for removal
            new_columns[[new_col_name]] <- new_col_data
            cols_to_remove <- c(cols_to_remove, col_name)
            
            message("🔀 Splitting column '", col_name, "' into new column '", 
                   new_col_name, "' with consistent prefix '", consistent_prefix, "'")
          }
        }
      }
    }
  }
  
  # Remove original columns that were split
  if (length(cols_to_remove) > 0) {
    processed_pheno <- processed_pheno[, !colnames(processed_pheno) %in% cols_to_remove, drop = FALSE]
  }
  
  # Add new columns
  if (length(new_columns) > 0) {
    for (new_col_name in names(new_columns)) {
      processed_pheno[[new_col_name]] <- new_columns[[new_col_name]]
    }
  }
  
  return(processed_pheno)
}


# do.call(parse_methylation_data, args_list)

# ==============================================================
# Usage Examples
# ==============================================================

# Example 1: Parse GEO series matrix file (contains expression matrix and phenotype information)
# parse_methylation_data("GSE123456_series_matrix.txt.gz", "output_dir")

# Example 2: Parse file with only phenotype information
# parse_methylation_data("GSE123456_pheno_only.txt", "output_dir")

# Example 3: Parse CSV.GZ file with only expression matrix  
# parse_methylation_data("GSE72777_datBetaNormalized.csv.gz", "output_dir")

# Example 4: Batch process download list
# parse_methylation_data("DownloadList.txt", "output_dir")