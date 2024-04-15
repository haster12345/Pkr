from read_file import FileContent
from pokerstars_parser import PokerStarsParser
from create_tables import create_hand_info_table
import os
from local_db import dynamodb


def concat_hands(folder_path):
    """
    iterate through a directory and pass each file into the parser
    """
    item_list = []

    for filename in os.listdir(folder_path):

        if filename[-3:]  == 'txt':
            hands = FileContent(folder_name=folder_path,file_name=filename).hands()
            items = PokerStarsParser(hands).parse()[2]
            item_list += items

    return item_list

def populate_table(folder_path):
    item_list = concat_hands(folder_path)
    table = dynamodb.Table('hand_info')
    with table.batch_writer() as batch:
        for item in item_list:
            try:
                batch.put_item(Item=item)
            except:
                create_hand_info_table()
                populate_table(item_list)
    return

