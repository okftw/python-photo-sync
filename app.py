import os
import datetime
import logging
import hashlib
from pathlib import Path


logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[
                        logging.FileHandler("debug.log"),
                        logging.StreamHandler()
                    ],
                    encoding='utf-8', 
                    level=logging.DEBUG)

source_path = "D:\Pictures-test"

destination_path = "E:\Pictures"

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def get_md5_hash(filename):
    return hashlib.md5(open(filename,'rb').read()).hexdigest()

logging.info(f'Source Folder : {source_path}')

for subdir, dirs, files in os.walk(source_path):
    for file in files:
        logging.info(f'Source File : {os.path.join(subdir, file)}')
        source_file_creation_date = modification_date(os.path.join(subdir, file))
        logging.info(f'Source File Creation Date : {source_file_creation_date}')
        source_file_md5_hash = get_md5_hash(os.path.join(subdir, file))
        logging.info(f'Source File MD5 Checksum : {source_file_md5_hash}')
        source_file_extension = Path(file).suffix
        source_file_extensions = Path(file).suffixes

        destination_folder_year = source_file_creation_date.strftime("%Y")
        destination_folder_day = source_file_creation_date.strftime("%Y%m%d")
        destination_file_name = source_file_creation_date.strftime("%Y%m%d_%H%M%S")
        destination_full_path = os.path.join(destination_path, 
                                                   destination_folder_year, 
                                                   destination_folder_day, 
                                                   destination_file_name + source_file_extension)
        logging.info(f'Destination File : {destination_full_path}')

        logging.info("------------")
        logging.info("")