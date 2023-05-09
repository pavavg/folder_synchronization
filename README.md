## Requirements:
* Python 3.7
* Run `pip install -r requirements.txt`

## Usage:
`python src/main.py [-h] -fs FOLDER_SOURCE_PATH -fr FOLDER_REPLICA_PATH -si SYNCHRONIZATION_INTERVAL_IN_SECONDS -l LOG_FILE_PATH`

## Description:
This script synchronizes two folders. After synchronization the folders are identical.
The CREATE/COPY/DELETE operations are logged in the LOG_FILE_PATH that is provided as argument.
