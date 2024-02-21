from pre_flop_info import PreFlop
from table_info import Files
from table_info import TableInfo
from read_file import FileContent
import os


def main(folder_path):
    for filename in os.listdir(folder_path):
        hands = FileContent(folder_name=folder_path,file_name=filename).hands()
        TableInfo(hands).parse_into_json()
        PreFlop(hands).parse_into_json()

main('hastermaster/')