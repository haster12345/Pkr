#!/usr/bin/env python3
from populate_tables import populate_table
import os
from read_file import FileContent
from pokerstars_parser import PokerStarsParser

def main(folder_path):
    return populate_table(folder_path)

def main_json(folder_path):
    for filename in os.listdir(folder_path):

        if filename[-3:]  == 'txt':
            hands = FileContent(folder_name=folder_path,file_name=filename).hands()
            PokerStarsParser(hands).parse_into_json()
        else:
            return "incorrect file type"
    return


if __name__ == '__main__':
    main('../Samples/hastermaster/')
