#!/usr/bin/env python3
from populate_tables import populate_table_all_files


def main(folder_path):
    """
    iterate through a directory and pass each file into the parser
    """
    return populate_table_all_files(folder_path)

if __name__ == '__main__':
    main('../Samples/hastermaster/')
