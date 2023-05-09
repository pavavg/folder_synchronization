import filecmp
import os
import shutil
from unittest.mock import MagicMock

import pytest

from src.synchronization import FolderSynchronizer


def create_source_folder(folder_path: str):
    os.makedirs(folder_path)

    os.makedirs(os.path.join(folder_path, 'empty_folder'))

    os.makedirs(os.path.join(folder_path, 'not_empty_folder'))
    with open(os.path.join(folder_path, 'not_empty_folder', 'a_file.txt'), 'w') as f:
        f.write('SOMETHING IN THE FILE')

    with open(os.path.join(folder_path, 'b_file.txt'), 'w') as f:
        f.write('SOMETHING ELSE')


def create_replica_folder_case_2(folder_path: str):
    create_source_folder(folder_path)


def create_replica_folder_case_3(folder_path: str):
    create_source_folder(folder_path)

    os.makedirs(os.path.join(folder_path, 'another_empty_folder'))

    os.makedirs(os.path.join(folder_path, 'another_not_empty_folder'))
    with open(os.path.join(folder_path, 'another_not_empty_folder', 'a_file.txt'), 'w') as f:
        f.write('SOMETHING IN THE FILE OMG!')


def create_replica_folder_case_4(folder_path: str):
    os.makedirs(folder_path)

    os.makedirs(os.path.join(folder_path, 'empty_folder_whatever'))

    with open(os.path.join(folder_path, 'b_file.txt'), 'w') as f:
        f.write('SOMETHING ELSE WOWWWWW!')


"""
Test cases:
CASE 1: Replica folder does not contain anything.
CASE 2: Replica folder contains same items as source folder.
CASE 3: Replica folder contains more items than source folder, with different data.
CASE 4: Replica folder contains less items than source folder, with different data.
"""


@pytest.mark.parametrize('test_case', [1, 2, 3, 4])
def test_folder_synchronization(test_case: int):
    source_path = 'test_data/source'
    replica_path = 'test_data/replica'
    create_source_folder(source_path)

    if test_case == 2:
        create_replica_folder_case_2(replica_path)
    elif test_case == 3:
        create_replica_folder_case_3(replica_path)
    elif test_case == 4:
        create_replica_folder_case_4(replica_path)

    folder_synchronizer = FolderSynchronizer(source_path, replica_path, logger=MagicMock())
    folder_synchronizer.synchronize()

    assert folders_are_identical(source_path, replica_path)

    shutil.rmtree('test_data')


def folders_are_identical(source_path, replica_path):
    result = filecmp.dircmp(source_path, replica_path)
    if result.diff_files or result.left_only or result.right_only:
        return False
    for subdir in result.common_dirs:
        if not folders_are_identical(
                f"{source_path}/{subdir}", f"{replica_path}/{subdir}"
        ):
            return False
    return True
