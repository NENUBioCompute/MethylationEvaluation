from core.pipeline import DNAmPreprocessorPipeline

def main():
    # Initialize the preprocessing pipeline
    pipeline = DNAmPreprocessorPipeline("./config/default.yaml")
    
    # Check the current pipeline status
    status = pipeline.get_status()
    print("Pipeline status:", status)
    
    # # Run the full preprocessing pipeline
    results = pipeline.run_full_pipeline(
        download_list_path="./config/DownloadList.txt",
        overwrite=True, # Recommendation overwrite=True
    )
    
    print("Pipeline execution results:", results)
    
    # Or run step-by-step
    # pipeline.download_data(download_list_path="./config/DownloadList.txt")
    # pipeline.parse_data()
    # pipeline.validate_mappings()
    # pipeline.standardize_pheno_data()
    # pipeline.standardize_methyl_data(overwrite=True)


if __name__ == "__main__":
    main()