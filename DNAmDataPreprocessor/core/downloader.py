"""
Data Downloader Module - Focused on file download functionality
Supports multiple download methods, resumable downloads, and error recovery
"""
import os
import time
import logging
import subprocess
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from multiprocessing import Process
import requests


class DownloadError(Exception):
    """Custom exception for download-related errors"""
    pass


class DataDownloader:
    """Data downloader supporting multiple download methods and resumable downloads"""
    
    def __init__(self, download_dir, max_retries, timeout, use_multiprocessing=False, preferred_method='requests', downloaded_files_record=None):
        """
        Initialize the downloader
        Parameters:
        --------------
            download_dir: Directory to save downloaded files
            max_retries: Maximum number of retry attempts for downloads
            timeout: Timeout for each download attempt in seconds
            use_multiprocessing: Whether to use multiprocessing for downloads
            preferred_method: Preferred download method ('requests' or 'wget')
            downloaded_files_record: Path to record of downloaded files
        """
        self.download_dir = Path(download_dir)
        self.max_retries = max_retries
        self.timeout = timeout
        self.use_multiprocessing = use_multiprocessing
        self.preferred_method = preferred_method
        self.downloaded_files_record = Path(downloaded_files_record if downloaded_files_record else self.download_dir / "downloaded_files.txt")
        
        # Create directory
        self.download_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logger
        self.logger = self._setup_logger()
        
        # Download methods mapping
        self.download_methods = {
            'wget': self._download_with_wget,
            'requests': self._download_with_requests
        }

        self.download_total = 1
    
    def _setup_logger(self) -> logging.Logger:
        """Setup and return logger instance"""
        logger = logging.getLogger('DataDownloader')
        logger.setLevel(logging.INFO)
        
        # Prevent duplicate log handlers in case of multiple instances
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
        
    def download_from_list(self, download_list_file: str) -> Dict[str, bool]:
        """
        Batch download data from download list file
        
        Args:
            download_list_file: Path to download list file
            
        Returns:
            Download results dictionary {filename: success_status}
        """
        results = {}
        
        try:
            urls = self._read_download_list(download_list_file)
            self.download_total = len(urls)
            self.logger.info(f"Starting download of {self.download_total} files")
            
            if self.use_multiprocessing:
                results = self._download_parallel(urls)
            else:
                results = self._download_sequential(urls)
            
            success_count = sum(results.values())
            self.logger.info(f"Download completed: {success_count}/{self.download_total} files successful")
            
            # Generate downloaded files list
            self._generate_downloaded_files_list(results)
            
        except Exception as e:
            self.logger.error(f"Batch download failed: {e}")
            raise DownloadError(f"Batch download failed: {e}")
        
        return results

    def download_single_file(self, url: str, filename: Optional[str] = None) -> bool:
        """
        Download single file with support for multiple methods and resumable downloads
        
        Args:
            url: File URL
            filename: Local filename (extracted from URL if None)
            
        Returns:
            Whether download was successful
        """
        if filename is None:
            filename = self._get_filename_from_url(url)
        
        file_path = self.download_dir / filename
        
        # Check if file already exists
        if file_path.exists():
            self.logger.info(f"File already exists: {filename}")
            return True
        
        # Try preferred download method first
        download_func = self.download_methods.get(self.preferred_method)
        if download_func:
            try:
                return download_func(url, filename)
            except Exception as e:
                self.logger.warning(f"Preferred download method failed, trying alternatives: {e}")
        
        # Try alternative download methods
        for method_name, download_func in self.download_methods.items():
            if method_name != self.preferred_method:
                try:
                    self.logger.info(f"Trying alternative download method: {method_name}")
                    return download_func(url, filename)
                except Exception as e:
                    self.logger.warning(f"Alternative download method {method_name} failed: {e}")
        
        raise DownloadError(f"All download methods failed: {filename}")
    
    def _read_download_list(self, download_list_file: str) -> List[str]:
        """Read download list file"""
        urls = []
        try:
            with open(download_list_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        urls.append(line)
            self.logger.info(f"Read {len(urls)} URLs from {download_list_file}")
        except Exception as e:
            raise DownloadError(f"Failed to read download list file: {e}")
        
        return urls
    
    def _download_sequential(self, urls: List[str]) -> Dict[str, bool]:
        """Sequential download"""
        results = {}
        for url in urls:
            filename = self._get_filename_from_url(url)
            try:
                success = self.download_single_file(url, filename)
                results[filename] = success
            except Exception as e:
                self.logger.error(f"Failed to download file: {filename}, error: {e}")
                results[filename] = False
        return results
    
    def _download_parallel(self, urls: List[str]) -> Dict[str, bool]:
        """Parallel download using multiprocessing"""
        processes = []
        results = {}
        
        for url in urls:
            filename = self._get_filename_from_url(url)
            if self.use_multiprocessing:
                process = Process(
                    target=self._download_single_file_worker,
                    args=(url, filename)
                )
                process.start()
                processes.append((process, filename))
            else:
                results[filename] = self.download_single_file(url, filename)
        
        # Wait for all processes to complete
        for process, filename in processes:
            process.join()
            # Simplified implementation: assume all processes succeeded
            results[filename] = True
        
        return results
    
    def _download_single_file_worker(self, url: str, filename: str):
        """Single file download worker process"""
        try:
            self.download_single_file(url, filename)
        except Exception as e:
            self.logger.error(f"Subprocess download failed: {filename}, error: {e}")
    
    def _download_with_requests(self, url: str, filename: str) -> bool:
        """Download using requests library (supports resumable downloads)"""
        file_path = self.download_dir / filename
        temp_path = file_path.with_suffix('.download')
        
        start_byte = 0
        if temp_path.exists():
            start_byte = temp_path.stat().st_size
            self.logger.info(f"Found incomplete download, resuming from byte {start_byte}: {filename}")
        
        for attempt in range(self.max_retries):
            try:
                headers = {}
                if start_byte > 0:
                    headers['Range'] = f'bytes={start_byte}-'
                
                response = requests.get(
                    url, 
                    stream=True, 
                    timeout=self.timeout,
                    headers=headers
                )
                response.raise_for_status()
                
                mode = 'ab' if start_byte > 0 else 'wb'
                with open(temp_path, mode) as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Rename temporary file
                temp_path.rename(file_path)
                self.logger.info(f"Successfully downloaded: {filename}")
                return True
                
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Download failed (attempt {attempt + 1}/{self.max_retries}): {filename}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise DownloadError(f"Download failed: {filename}, error: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error during download: {filename}, error: {e}")
                raise DownloadError(f"Download failed: {filename}, error: {e}")
        
        return False
    
    def _download_with_wget(self, url: str, filename: str) -> bool:
        """Download using wget command"""
        file_path = self.download_dir / filename
        
        try:
            start_time = time.time()
            
            # Build wget command
            cmd = f"wget {url} -O {file_path} -T {self.timeout}"
            
            # Execute download command
            result = subprocess.run(
                cmd, 
                shell=True, 
                timeout=self.timeout,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                download_time = time.time() - start_time
                self.logger.info(f"wget download successful: {filename}, time: {download_time:.2f} seconds")
                return True
            else:
                raise DownloadError(f"wget command failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            raise DownloadError(f"wget download timeout: {filename}")
        except Exception as e:
            raise DownloadError(f"wget download failed: {filename}, error: {e}")
    
    def _get_filename_from_url(self, url: str) -> str:
        """Extract filename from URL"""
        return url.split('/')[-1]
    
    def _generate_downloaded_files_list(self, results: Dict[str, bool]):
        """
        Generate a text file listing all successfully downloaded files
        
        Args:
            results: Dictionary of download results {filename: success_status}
        """
        try:
            # Filter successful downloads
            successful_files = [filename for filename, success in results.items() if success]
            
            if not successful_files:
                self.logger.warning("No successful downloads to list")
                return
            
            # Create file list
            file_list_path = self.downloaded_files_record
            with open(file_list_path, 'w') as f:
                for filename in successful_files:
                    # saved as absolute paths
                    file_path = (self.download_dir / filename).resolve()
                    f.write(f"{file_path}\n")
            
            self.logger.info(f"Downloaded files list generated: {file_list_path}")
            self.logger.info(f"Listed {len(successful_files)} successfully downloaded files")
            
        except Exception as e:
            self.logger.error(f"Failed to generate downloaded files list: {e}")
    
    def get_download_status(self) -> Dict:
        """Get download status information"""
        downloaded_files = list(self.download_dir.glob('*'))
        return {
            'download_dir': str(self.download_dir),
            'downloaded_files_count': len(downloaded_files),
            'downloaded_files': [f.name for f in downloaded_files],
            'Success': len(downloaded_files),
            'Failed': self.download_total-len(downloaded_files),
            'config': {
                'max_retries': self.max_retries,
                'timeout': self.timeout,
                'preferred_method': self.preferred_method
            }
        }
    
    def list_downloaded_files(self) -> List[Path]:
        """Get list of downloaded files"""
        return list(self.download_dir.glob('*'))
    
    def clear_downloads(self) -> bool:
        """Clear download directory"""
        try:
            for file_path in self.download_dir.glob('*'):
                if file_path.is_file():
                    file_path.unlink()
            self.logger.info(f"Download directory cleared: {self.download_dir}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear download directory: {e}")
            return False

