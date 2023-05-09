import os
import shutil


BYTE_BLOCK_SIZE_TO_READ = 16384


class FolderSynchronizer:

    def __init__(self, source: str, replica: str, logger):
        self._source: str = source

        self._replica: str = replica
        if not os.path.exists(replica):
            os.makedirs(replica)
            logger.info(f"Replica directory did not exist and was created.")

        self._logger = logger

    def synchronize(self):
        source_folder_files, source_folder_subfolders = self._get_folder_items_paths(self._source)

        replica_folder_files, replica_folder_subfolders = self._get_folder_items_paths(self._replica)

        excess_replica_folder_files = [file for file in replica_folder_files if file not in source_folder_files]
        excess_replica_folder_subfolders = [folder for folder in replica_folder_subfolders if folder not in
                                            source_folder_subfolders]

        # Synchronize files
        for current_file_to_sync in source_folder_files:

            if current_file_to_sync in replica_folder_files:
                if not self._is_file_synchronized(current_file_to_sync):
                    self._logger.info(f"{current_file_to_sync} exists in replica folder and it is not synchronized. "
                                      f"Starting synchronizing...")
                    self._synchronize_file(current_file_to_sync)
                    self._logger.info(f"{current_file_to_sync} is now synchronized.")
            else:
                self._logger.info(f"{current_file_to_sync} does not exist in replica folder. Copying file...")
                self._synchronize_file(current_file_to_sync)
                self._logger.info(f"{current_file_to_sync} was successfully copied to the replica folder.")

        for excess_file in excess_replica_folder_files:
            os.remove(os.path.join(self._replica, excess_file))
            self._logger.info(f"{len(excess_replica_folder_files)} excess files were successfully removed from"
                              f" the replica folder.")

        # Synchronize folders.
        for subfolder in source_folder_subfolders:
            if subfolder not in replica_folder_subfolders and not os.path.exists(os.path.join(self._replica, subfolder)):
                os.makedirs(os.path.join(self._replica, subfolder))
                self._logger.info(f"{subfolder} folder was successfully created.")

        # There shouldn't be any files left in these excess subfolders, due to file synchronization.
        for excess_folder in excess_replica_folder_subfolders:
            try:
                shutil.rmtree(os.path.join(self._replica, excess_folder))
                self._logger.info(f"{excess_folder} subfolder and all its contents were successfully removed.")
            except:
                continue

    @staticmethod
    def _get_folder_items_paths(folder_path: str):

        subfolders_in_folder = []
        files_in_folder = []
        for root, dirs, files in os.walk(folder_path):
            root = root[len(folder_path)+1:]    # This is required, so we keep only the subjective path for the folder.
            subfolders_in_folder.append(root)
            for f in files:
                files_in_folder.append(os.path.join(root, f))

        return files_in_folder, subfolders_in_folder

    def _is_file_synchronized(self, file_path: str):

        with open(os.path.join(self._source, file_path), 'rb') as fs, open(os.path.join(self._replica, file_path),
                                                                           'rb') as fd:
            while True:
                source_file_data_batch = fs.read(BYTE_BLOCK_SIZE_TO_READ)
                replica_file_data_batch = fd.read(BYTE_BLOCK_SIZE_TO_READ)

                if not source_file_data_batch and not replica_file_data_batch:
                    return True

                if source_file_data_batch != replica_file_data_batch:
                    return False

    def _synchronize_file(self, file_path: str):
        head_path = os.path.split(file_path)[0]
        if not os.path.exists(os.path.join(self._replica, head_path)):
            os.makedirs(os.path.join(self._replica, head_path))

        with open(os.path.join(self._source, file_path), 'rb') as fs, open(os.path.join(self._replica, file_path),
                                                                           'wb') as fd:
            while True:
                data_batch = fs.read(BYTE_BLOCK_SIZE_TO_READ)
                if not data_batch:
                    break

                fd.write(data_batch)
