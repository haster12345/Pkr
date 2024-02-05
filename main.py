from pre_flop_info import PreFlop
from table_info import Files
from table_info import TableInfo

def main(folder_path):
    files = Files(folder_path)
    file_content_list = files.read_files()
    
    for file in file_content_list:
        TableInfo(file).parse_into_json()
        PreFlop(file).parse_into_json()
    
    return

main('hastermaster/')