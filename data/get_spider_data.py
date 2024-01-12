""" 
This script downloads and extracts data from a remote source. 
It checks if the data file and directory already exist. 
If they do, it prints a message and returns. 
If not, it proceeds to download the data file from a specified URL. 
It then checks the MD5 sum of the downloaded file to ensure its integrity. 
If the MD5 sum is valid, the function proceeds to extract the file and create the ontology and hints directory structures. 
If the MD5 sum is not valid, the file is removed. 
Finally, the function prints a message indicating the completion of the process."""

import os
import hashlib
import zipfile
import shutil
import requests

def download_and_extract_data(data_url, data_file, data_md5, data_dir, ontology_dir, hints_dir):
    """
    Downloads and extracts data from a remote source.

    This function checks if the data file and directory already exist. 
    If they do, it prints a message and returns. 
    If not, it proceeds to download the data file from a specified URL. 
    It then checks the MD5 sum of the downloaded file to ensure its integrity. 
    If the MD5 sum is valid, the function proceeds to extract the file and create the ontology and hints directory structures. 
    If the MD5 sum is not valid, the file is removed. 
    Finally, the function prints a message indicating the completion of the process.

    Parameters:
    data_url (str): The URL of the data file.
    data_file (str): The name of the data file.
    data_md5 (str): The MD5 sum of the data file.
    data_dir (str): The name of the data directory.
    ontology_dir (str): The name of the ontology directory.
    hints_dir (str): The name of the hints directory.

    Returns:
    None
    """
    # Check if the data file exists
    if os.path.isfile(data_file):
        print(f"Data file {data_file} exists. Removing it now and before proceeding.")
        os.remove(data_file)

    # Check if the data dir exists and remove it if it exists.
    if os.path.isdir(data_dir):
        print(f"Data directory {data_dir} exists. Removing it now and before proceeding.")
        shutil.rmtree(data_dir)

    # Get data
    print("Getting spider dataset ...")
    response = requests.get(data_url, timeout=10)

    # Check if we got the file
    if response.status_code == 200:
        with open(data_file, 'wb') as f:
            f.write(response.content)
        print("File downloaded.")

        # Check md5 sum
        print("Checking md5 sum ... ")
        md5_hash = hashlib.md5()
        
        with open(data_file,"rb") as f:
            for byte_block in iter(lambda: f.read(4096),b""):
                md5_hash.update(byte_block)
                
        if md5_hash.hexdigest() == data_md5:
            print("OK.")
            print("Uncompressing ...")
            
            with zipfile.ZipFile(data_file, 'r') as zip_ref:
                # unzip to parent folder
                zip_ref.extractall(os.path.dirname(data_file))
            print("Done.")
            
        else:
            print("NOT VALID. File will be removed.")

        # Remove the zip file
        print(f"Removing {data_file} ...")
        os.remove(data_file)

        # Create Ontology Directory Structure (not overwriting if exists)
        print("Creating Ontology Directory Structure (not overwriting if exists) ...")
        for _, subdirs, _ in os.walk(os.path.join(data_dir, "database")):
            
            for subdir in subdirs:
                ont = os.path.join(ontology_dir, data_dir, subdir)
                print(f"Working on db {subdir} ... ")
                
                if os.path.isdir(ont):
                    print("EXISTS.")
                else:
                    os.makedirs(ont, exist_ok=True)
                    print("CREATED.")

        # Create Hints Directory Structure (not overwriting if exists)
        print("Creating Hints Directory Structure (not overwriting if exists) ...")
        hnt = os.path.join(hints_dir, data_dir)
        print(f"Creating {hnt} ...")
        
        if os.path.isdir(hnt):
            print("EXISTS.")
        else:
            os.makedirs(hnt, exist_ok=True)
            
            print("CREATED.")

        print("Done")
    else:
        print(f"Error in downloading {data_file}.")


if __name__ == "__main__":
    DATA_URL = "https://huggingface.co/datasets/spider/resolve/main/data/spider.zip"
    DATA_FILE = "spider.zip"
    DATA_MD5 = "8cc3974a3b246622127a9562f6994c88"
    DATA_DIR = os.path.join("..", "data", "spider")

    ONTOLOGY_DIR = os.path.join("..", "ontology")
    HINTS_DIR = os.path.join("..", "hints")
    # Call the function
    download_and_extract_data(
        data_url=DATA_URL,
        data_file=DATA_FILE,
        data_md5=DATA_MD5,
        data_dir=DATA_DIR,
        ontology_dir=ONTOLOGY_DIR,
        hints_dir=HINTS_DIR
    )
    