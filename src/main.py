#!/usr/bin/env python3
from populate_tables import populate_table


def main(folder_path):
    return populate_table(folder_path)

if __name__ == '__main__':
    main('../Samples/hastermaster/')
