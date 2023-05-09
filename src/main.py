import argparse
import logging
import os
import time

from synchronization import FolderSynchronizer


def get_logger(file_path: str):

    head_path = os.path.split(file_path)[0]

    if head_path and not os.path.exists(head_path):
        os.makedirs(head_path)

    logger = logging.getLogger(__name__)
    shdlr = logging.StreamHandler()
    fhdlr = logging.FileHandler(file_path)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    fhdlr.setFormatter(formatter)
    shdlr.setFormatter(formatter)
    logger.addHandler(shdlr)
    logger.addHandler(fhdlr)
    logger.setLevel(logging.DEBUG)

    return logger


def _parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-fs', '--folder_source_path', required=True, type=str)
    parser.add_argument('-fr', '--folder_replica_path', required=True, type=str)
    parser.add_argument('-si', '--synchronization_interval_in_seconds', required=True, type=int)
    parser.add_argument('-l', '--log_file_path', required=True, type=str)

    args = parser.parse_args()

    return args.folder_source_path, \
        args.folder_replica_path, \
        args.synchronization_interval_in_seconds, \
        args.log_file_path


def main():
    """
    Synchronize 2 folders periodically.

    Usage: main.py [-h] -fs FOLDER_SOURCE_PATH -fr FOLDER_REPLICA_PATH
    -si SYNCHRONIZATION_INTERVAL_IN_SECONDS -l LOG_FILE_PATH
    """
    (source_folder_path, replica_folder_path, sync_interval, log_file_path) = _parse_arguments()

    logger = get_logger(file_path=log_file_path)

    synchronizer = FolderSynchronizer(source=source_folder_path,
                                      replica=replica_folder_path,
                                      logger=logger)

    while True:
        logger.info('Starting synchronization...')
        synchronizer.synchronize()
        logger.info(f"Folder {replica_folder_path} was successfully synchronized according to {source_folder_path}")

        time.sleep(sync_interval)


if __name__ == "__main__":
    main()
