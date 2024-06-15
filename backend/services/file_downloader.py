import os
import requests
from pathlib import Path
from urllib.parse import urlparse
from backend.utils.logger import Logger

class FileDownloader:
    def __init__(self, env_variables: list, download_dir: str, logger: Logger):
        """
        Initialize the FileDownloader.

        Args:
            env_variables (list): List of dictionaries containing URLs.
            download_dir (str): Directory where files will be downloaded.
            logger (Logger): Logger instance for logging.
        """
        self.env_variables = env_variables
        self.download_dir = download_dir
        self.logger = logger
        self.urls = []

    def extract_urls(self):
        """
        Extract URLs from the list of dictionaries where keys contain 'z-score'.
        """
        self.logger.info("Extracting URLs from environment variables")

        for entry in self.env_variables:
            self._extract_urls_from_dict(entry)

        self.logger.info("URLs extracted successfully")
        return self.urls

    def _extract_urls_from_dict(self, data):
        """
        Recursively extract URLs from a dictionary where keys contain 'z-score'.

        Args:
            data (dict): Dictionary data.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    self._extract_urls_from_dict(value)
                elif isinstance(value, str) and value.startswith("https://") and "z-score" in key:
                    self.urls.append(value)
        elif isinstance(data, tuple) and len(data) == 2:
            key, value = data
            if isinstance(value, dict):
                self._extract_urls_from_dict(value)
            elif isinstance(value, str) and value.startswith("https://") and "z-score" in key:
                self.urls.append(value)

    def download_files(self):
        """
        Download files from the extracted URLs.
        """
        self.logger.info("Starting file downloads")
        Path(self.download_dir).mkdir(parents=True, exist_ok=True)

        for url in self.urls:
            self._download_file(url)

    def _download_file(self, url):
        """
        Download a file from a URL.

        Args:
            url (str): URL of the file to download.
        """
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split('/')
        
        if 'indicators' in path_parts:
            indicators_index = path_parts.index('indicators')
            relevant_path = '/'.join(path_parts[indicators_index+1:])
        else:
            relevant_path = '/'.join(path_parts[-2:])

        file_name = os.path.join(self.download_dir, relevant_path)
        
        self.logger.info(f"Downloading {url} to {file_name}")

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            os.makedirs(os.path.dirname(file_name), exist_ok=True)

            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            self.logger.info(f"Downloaded {file_name}")
        except requests.RequestException as e:
            self.logger.error(f"Failed to download {url}: {e}")

if __name__ == "__main__":
    from utils.logger import Logger
    from utils.env_loader import load_env_variables

    logger = Logger()
    env_variables = load_env_variables(logger, '..\\..\\config.json')

    downloader = FileDownloader(env_variables, '..\\data', logger)
    downloader.extract_urls()
    # downloader.download_files()
