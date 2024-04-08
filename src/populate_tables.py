from read_file import FileContent
from pokerstars_parser import PokerStarsParser
import os
from local_db import dynamodb


def populate_table_all_files(folder_path):
    """
    iterate through a directory and pass each file into the parser
    """
    item_list = []

    for filename in os.listdir(folder_path):
        if filename[-3:]  == 'txt':
            hands = FileContent(folder_name=folder_path,file_name=filename).hands()
            items = PokerStarsParser(hands).parse()[2]
            item_list += items

    return populate_table(item_list) 

def populate_table(item_list):
    table = dynamodb.Table('hand_info')
    with table.batch_writer() as batch:
        for item in item_list:
            print(item)
            batch.put_item(Item=item)
    return

