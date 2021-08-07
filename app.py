import os
import datetime
import logging
import hashlib
from pathlib import Path
import shutil
import argparse
import sys 
import time

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.DEBUG):
    """To setup as many loggers as you want"""

    logger = logging.getLogger(name)
    logger.setLevel(level)

    fileHandler = logging.FileHandler(log_file)        
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(level)
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    return logger    

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def get_md5_hash(filename):
    return hashlib.md5(open(filename,'rb').read()).hexdigest()

def create_folder_path(path):
    Path(path).mkdir(parents=True, exist_ok=True)

# Setup Logging Files
logger = setup_logger('output', 'output.log')
logger_output = logging.getLogger('output')

logger = setup_logger('copied', 'copied.log')
logger_copied = logging.getLogger('copied')

logger = setup_logger('mismatch', 'mismatch.log')
logger_mismatch = logging.getLogger('mismatch')


def walk_directory(args):
    files_copied = 0
    files_skipped = 0
    source_path = args.source_path
    destination_path = args.destination_path

    if source_path:
        print (f'--source_path : {source_path}')
        source_path_exists = os.path.isdir(source_path) 
        if not source_path_exists:
            logger_output.error(f'Source Path Doesnt Exist! : {source_path}')
            logger_output.error(f'exiting...')
            exit(1)

    if destination_path:
        print (f'--destination_path : {destination_path}')
    else:
        logger_output.error(f'Please set --destination_path')
        logger_output.error(f'exiting...')
        exit(1)  

    if args.sync:
        logger_output.info(f'--sync parameter set')
    else:
        logger_output.info(f'--sync parameter not set, RUNNING IN SIMULATION MODE')

    input("Press Enter to continue...")
    
    start_time = datetime.datetime.now()
    
    for subdir, dirs, files in os.walk(source_path):
        for file in files:
            source_file_path = os.path.join(subdir, file)
            logger_output.info(f'Source File               : {source_file_path}')
            
            source_file_creation_date = modification_date(source_file_path)
            logger_output.info(f'Source File Creation Date : {source_file_creation_date}')
            
            source_file_md5_hash = get_md5_hash(source_file_path)
            logger_output.info(f'Source File MD5 Checksum  : {source_file_md5_hash}')
            
            source_file_extension = Path(file).suffix
            source_file_extensions = Path(file).suffixes

            logger_output.info("")

            destination_folder_year = source_file_creation_date.strftime("%Y")
            destination_folder_day = source_file_creation_date.strftime("%Y%m%d")
            destination_file_name = source_file_creation_date.strftime("%Y%m%d_%H%M%S")
            destination_folder_path = os.path.join(destination_path, 
                                                destination_folder_year, 
                                                destination_folder_day)

            destination_file_path = os.path.join(destination_folder_path, 
                                                destination_file_name + "_" + source_file_md5_hash[:12].upper() + source_file_extension)

            logger_output.info(f'Destination Folder        : {destination_folder_path}')
            logger_output.info(f'Destination File          : {destination_file_path}')

            destination_folder_exists = os.path.isdir(destination_folder_path) 
            logger_output.info(f'Destination Folder Exists : {destination_folder_exists}')

            destination_file_exists = os.path.isfile(destination_file_path) 
            logger_output.info(f'Destination File Exists   : {destination_file_exists}')

            if not destination_folder_exists:
                if args.sync:
                    create_folder_path(destination_folder_path)
                logger_output.info(f'Created Destination Folder: {destination_folder_path}')

            if destination_file_exists:
                destination_file_md5_hash = get_md5_hash(destination_file_path)
                logger_output.info(f'Destination File MD5 Hash : {destination_file_md5_hash}')
                if source_file_md5_hash == destination_file_md5_hash:
                    logger_output.info(f'MD5 Checksum Matches : {source_file_md5_hash} --> {destination_file_md5_hash}')
                else:
                    logger_mismatch.info(f'MD5 Checksum Does Not Match! : {source_file_md5_hash} --> {destination_file_md5_hash}')
                logger_output.info(f'File Copy Skipped...')                         
                files_skipped += 1

            else:
                if args.sync:
                    logger_copied.info(f'Copying File : {source_file_path} --> {destination_file_path}')
                    shutil.copyfile(source_file_path, destination_file_path)
                    files_copied += 1

                else:
                    logger_output.info(f'Copying File (Simulation) : {source_file_path} --> {destination_file_path}')



            #create_folder_path
            logger_output.info("------------")

    elapsed_time =  datetime.datetime.now() - start_time
    logger_output.info('')
    logger_output.info(f'Photo Sync Completed !!!')
    logger_output.info('')
    logger_output.info(f'Files Skipped : {files_skipped}')
    logger_output.info(f'Files Copied  : {files_copied}')
    logger_output.info(f'Elapsed Time  : {elapsed_time}')
   

if __name__ == "__main__":
    pictures = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Pictures')

    parser = argparse.ArgumentParser()
    parser.add_argument("--source_path"     , help="Source Folder Path", default=pictures)
    parser.add_argument("--destination_path", help="Destination Folder Path")
    parser.add_argument("--sync"            , help="Copy files across", action='store_true')
    if len(sys.argv) < 2:
        parser.print_help()
        exit()
    args = parser.parse_args()
    walk_directory(args)
    