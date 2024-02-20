from pre_flop_info import PreFlop
from table_info import Files
from table_info import TableInfo
from read_file import FileContent
import os


def main_1(folder_path):
    files = Files(folder_path)
    file_content_list = files.read_files()
    
    for file in file_content_list:
        TableInfo(file).parse_into_json()
        PreFlop(file).parse_into_json()
    
    return

def main(folder_path):
    for filename in os.listdir(folder_path):
        hands = FileContent(folder_name=folder_path,file_name=filename).hands()
        # print(hands)
        TableInfo(hands).parse_into_json()
        PreFlop(hands).parse_into_json()

main('hastermaster/')