from read_file import FileContent
from pokerstars_parser import PokerStarsParser
import os


def main(folder_path):
    """
    iterate through a directory and pass each file into the parser
    """
    for filename in os.listdir(folder_path):
        if filename[-3:]  == 'txt':
            hands = FileContent(folder_name=folder_path,file_name=filename).hands()
            PokerStarsParser(hands).parse()


if __name__ == '__main__':
    main('hastermaster/')
