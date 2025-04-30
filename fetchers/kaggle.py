import os
from kaggle.api.kaggle_api_extended import KaggleApi

# Function to authenticate with Kaggle API using Kaggle.json
def authenticate_kaggle():
    """
    Authenticate with Kaggle using the kaggle.json file.
    The `kaggle.json` file should be placed in the path: ~/.kaggle/kaggle.json
    """
    # Check if kaggle.json exists in the default location
    kaggle_json_path = os.path.expanduser('~/.kaggle/kaggle.json')
    if not os.path.exists(kaggle_json_path):
        print("❌ Kaggle API key not found! Please place kaggle.json in ~/.kaggle/")
        return None
    
    # Initialize the Kaggle API and authenticate
    api = KaggleApi()
    api.authenticate()
    print("✅ Kaggle authenticated successfully!")
    return api

# Function to download files from a Kaggle dataset
def download_kaggle_code_samples(dataset_name, download_path):
    """
    Download the files of a Kaggle dataset and unzip them into the specified path.
    """
    api = authenticate_kaggle()
    if api is None:
        return  # Exit if authentication fails
    
    # Download the dataset and unzip
    print(f"🔄 Downloading {dataset_name} dataset...")
    api.dataset_download_files(dataset_name, path=download_path, unzip=True)
    print(f"✅ Dataset {dataset_name} downloaded and unzipped to {download_path}")
