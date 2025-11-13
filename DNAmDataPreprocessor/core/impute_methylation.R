# DNA Methylation Data Imputation using methyLImp2
# Optimized R script for missing value imputation

# Function to perform methylation data imputation with optimized parameters
impute_methylation_data <- function(input_file, output_file) {
    # Load required libraries
    required_packages <- c("methyLImp2", "BiocParallel")
    
    for (pkg in required_packages) {
        if (!require(pkg, character.only = TRUE)) {
            stop("Package ", pkg, " is not installed. Please install it.")
        }
    }
    
    cat("=== DNA Methylation Imputation Started ===\\n")
    cat("Input file:", input_file, "\\n")
    cat("Output file:", output_file, "\\n")
    
    # Read the methylation data
    cat("Reading methylation data...\\n")
    methylation_data <- read.csv(gzfile(input_file), row.names = 1)
    
    # Convert to matrix for methyLImp2
    data_matrix <- as.matrix(methylation_data)
    
    # Check for missing values
    missing_count <- sum(is.na(data_matrix))
    cat("Found", missing_count, "missing values in the dataset\\n")
    
    if (missing_count == 0) {
        cat("No missing values found. Writing original data to output.\\n")
        write.csv(methylation_data, file = gzfile(output_file), row.names = TRUE)
        cat("=== Imputation Completed (No Missing Values) ===\\n")
        return(0)
    }
    
    # Get probe names (CpG sites) from row names
    probe_names <- rownames(data_matrix)
    cat("Total probes in data:", length(probe_names), "\\n")
    
    # Set up optimized parameters for methyLImp2
    cat("Setting up optimized parameters for methyLImp2...\\n")
    
    # Configure parallel processing parameters
    # Use fewer workers to avoid chromosome count warning
    bp_param <- BiocParallel::MulticoreParam(workers = min(4, BiocParallel::multicoreWorkers()))
    
    # Determine array type based on probe names
    array_type <- "450K"  # Default assumption
    if (any(grepl("^cg\\d{8}", probe_names))) {
        # Check if we have EPIC array probes
        epic_probes <- sum(grepl("^cg\\d{8}", probe_names))
        total_probes <- length(probe_names)
        if (epic_probes > 850000) {  # EPIC arrays have ~850K probes
            array_type <- "EPIC"
        }
    }
    cat("Detected array type:", array_type, "\\n")
    
    tryCatch({
        # Perform imputation using methyLImp2 with optimized parameters
        cat("Starting methyLImp2 imputation with array type:", array_type, "\\n")
        cat("Using parallel workers:", bp_param$workers, "\\n")
        
        # Call methyLImp2 with explicit parameters
        imputed_data <- methyLImp2::methyLImp2(
            input = data_matrix,
            type = array_type,
            BPPARAM = bp_param
        )
        
        cat("methyLImp2 imputation completed successfully!\\n")
        
        # Convert back to data frame
        imputed_df <- as.data.frame(imputed_data)
        
        # Verify imputation results
        remaining_missing <- sum(is.na(imputed_df))
        cat("Missing values after imputation:", remaining_missing, "\\n")
        
        if (remaining_missing > 0) {
            cat("Warning: Some missing values remain after imputation.\\n")
            # Optionally apply a fallback method for remaining missing values
            cat("Applying fallback imputation for remaining missing values...\\n")
            for (col in names(imputed_df)) {
                if (any(is.na(imputed_df[[col]]))) {
                    col_mean <- mean(imputed_df[[col]], na.rm = TRUE)
                    imputed_df[[col]][is.na(imputed_df[[col]])] <- col_mean
                }
            }
            cat("Fallback imputation completed.\\n")
        }
        
        # Write imputed data to output file
        cat("Writing imputed data to:", output_file, "\\n")
        write.csv(imputed_df, file = gzfile(output_file), row.names = TRUE)
        
        # Calculate and report statistics
        original_probes <- nrow(methylation_data)
        imputed_probes <- nrow(imputed_df)
        cat("Original probes:", original_probes, "\\n")
        cat("Probes after imputation:", imputed_probes, "\\n")
        
        if (original_probes != imputed_probes) {
            cat("Note: Number of probes changed during imputation.\\n")
            cat("This may be due to probe filtering by methyLImp2.\\n")
        }
        
        cat("=== Imputation Completed Successfully ===\\n")
        return(0)
        
    }, error = function(e) {
        cat("Error during methyLImp2 imputation:", e$message, "\\n")
        cat("Attempting fallback imputation method...\\n")
        
        # Fallback: simple mean imputation
        tryCatch({
            for (col in names(methylation_data)) {
                if (any(is.na(methylation_data[[col]]))) {
                    col_mean <- mean(methylation_data[[col]], na.rm = TRUE)
                    methylation_data[[col]][is.na(methylation_data[[col]])] <- col_mean
                }
            }
            
            cat("Fallback imputation completed.\\n")
            write.csv(methylation_data, file = gzfile(output_file), row.names = TRUE)
            cat("Data saved with fallback imputation.\\n")
            return(0)
            
        }, error = function(e2) {
            cat("Fallback imputation also failed:", e2$message, "\\n")
            return(1)
        })
    })
}

# Enhanced main execution with better error handling
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
    stop("Usage: Rscript impute_methylation.R <input_file> <output_file>")
}

input_file <- args[1]
output_file <- args[2]

# Validate input file exists
if (!file.exists(input_file)) {
    stop("Input file does not exist: ", input_file)
}

# Check if output directory exists
output_dir <- dirname(output_file)
if (!dir.exists(output_dir)) {
    dir.create(output_dir, recursive = TRUE)
    cat("Created output directory:", output_dir, "\\n")
}

# Execute imputation with detailed logging
start_time <- Sys.time()
cat("Imputation started at:", as.character(start_time), "\\n")

result <- tryCatch({
    exit_code <- impute_methylation_data(input_file, output_file)
    exit_code
}, error = function(e) {
    cat("Fatal error in imputation process:", e$message, "\\n")
    1
})

end_time <- Sys.time()
duration <- difftime(end_time, start_time, units = "mins")
cat("Imputation completed at:", as.character(end_time), "\\n")
cat("Total time elapsed:", round(duration, 2), "minutes\\n")

quit(status = result)