from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
import sys

# Configuration
FOLDER_ID = '1vRrVYCH6wE5pwK7oNJGpyfpCUxFNgKYS'  # Google Drive folder ID
DOWNLOAD_DIR = ''  # Leave empty to replicate Google Drive structure locally

# Map vegetation types to their Google Drive folder names
VEGETATION_FOLDERS = {
    "native": "native",
    "ryegrass": "ryegrass",
    "sudangrass": "sudangrass",
}

# IMPORTANT: Ensure the file client_secrets.json is in the same directory as this script.
# This file is required for authenticating with the Google Drive API.
# For more information about PyDrive2, visit: https://github.com/iterative/PyDrive2

# Authentication
def authenticate():
    """Authenticate to Google Drive using PyDrive2."""
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Opens the browser for authentication
    return GoogleDrive(gauth)

def list_files_in_folder(drive, folder_id):
    """List all files and folders in a specific Google Drive folder."""
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    return file_list

def find_folder_id(drive, parent_id, folder_name):
    """Find the ID of a subfolder with a specific name."""
    folders = list_files_in_folder(drive, parent_id)
    for folder in folders:
        if folder['mimeType'] == 'application/vnd.google-apps.folder' and folder['title'] == 'dataset':
            return find_folder_id(drive, folder['id'], folder_name)
        elif folder['mimeType'] == 'application/vnd.google-apps.folder' and folder['title'] == folder_name:
            return folder['id']
        
    raise ValueError(f"Folder '{folder_name}' not found in parent ID '{parent_id}'")

def download_files_recursive(drive, folder_id, relative_path=''):
    """Recursively download files and subfolders from Google Drive."""
    # Compute the local directory path based on DOWNLOAD_DIR and relative_path
    local_path = os.path.join(DOWNLOAD_DIR, relative_path) if DOWNLOAD_DIR else os.path.normpath(relative_path)

    # Ensure the local directory exists
    os.makedirs(local_path, exist_ok=True)

    # List all files and folders in the current Google Drive folder
    file_list = list_files_in_folder(drive, folder_id)
    
    for file in file_list:
        file_name = file['title']
        file_id = file['id']

        # Check if the current file is a folder
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            print(f"Entering folder: {file_name}")
            # Recursively download the subfolder
            download_files_recursive(drive, file_id, os.path.join(relative_path, file_name))
        else:
            # Download the file
            print(f"Downloading file: {file_name}")
            file_path = os.path.join(local_path, file_name)
            file.GetContentFile(file_path)
            print(f"Downloaded: {file_name}")

def main():
    # Parse vegetation type from command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python download.py <vegetation_type>")
        print(f"Available options: {', '.join(VEGETATION_FOLDERS.keys())}")
        sys.exit(1)

    vegetation_type = sys.argv[1].lower()
    if vegetation_type not in VEGETATION_FOLDERS:
        print(f"Invalid vegetation type: {vegetation_type}")
        print(f"Available options: {', '.join(VEGETATION_FOLDERS.keys())}")
        sys.exit(1)

    # Set the current working directory to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Current working directory set to: {os.getcwd()}")

    print("Authenticating...")
    drive = authenticate()
    print("Authenticated successfully!")

    # Find the folder ID for the selected vegetation type
    print(f"Locating folder for vegetation type: {vegetation_type}")
    folder_name = VEGETATION_FOLDERS[vegetation_type]
    vegetation_folder_id = find_folder_id(drive, FOLDER_ID, folder_name)
    print(f"Found folder ID for {vegetation_type}: {vegetation_folder_id}")

    # Download files from the selected folder
    print(f"Downloading files for vegetation type: {vegetation_type}")
    download_files_recursive(drive, vegetation_folder_id, os.path.join('dataset', vegetation_type))
    print(f"Download complete for vegetation type: {vegetation_type}")

if __name__ == "__main__":
    main()
