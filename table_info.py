import re
import os
import json

class Files:

    def __init__(self, folder_path):
        self.folder_path = folder_path
    
    def read_files(self):

        file_content_list = []

        for filename in os.listdir(self.folder_path):
            
            print(f'{self.folder_path}/{filename}')
            with open(f'hastermaster/{filename}', 'r') as file:
                file_content = file.read()

            file_content_list.append(file_content)

        return file_content_list


class TableInfo:

    def __init__(self, file_contnet):
        self.file_content = file_contnet

    def hand_numbers(self):
        pattern = re.compile(r'PokerStars Hand #(\d+):')
        match = pattern.findall(self.file_content)
        match = [int(i) for i in match]
        return match

    def hand_info(self):
        pattern = re.compile(r'([\s\S]*?)\*\*\* HOLE CARDS \*\*\*')
        hand_info :list = pattern.findall(self.file_content)

        return hand_info
    
    def game_type(self, hand_info):
        pattern = re.compile(r'(?<=Hand #\d{12}: )(.*?)(?=\s-\s\d{4}\/\d{2}\/\d{2})')
        game_type = pattern.findall(hand_info)
        return game_type[0]

    def blind_sizes(self, hand_info):
        game_type = self.game_type(hand_info)
        pattern = re.compile(r'\d+\.\d+')
        blind_sizes = pattern.findall(game_type)
        return blind_sizes

    def button_seat_number(self, hand_info):
        pattern = re.compile(r'Seat #(\d+) is the button')
        button_seat_number = pattern.findall(hand_info)
        return button_seat_number
        
    def player_info(self, hand_info):
        pattern = re.compile(r'(.+?) \((\$[0-9.]+) in chips\)( is sitting out)?')
        player_info = pattern.findall(hand_info)
        return player_info

    def players_posting_blind(self, hand_info):
        pattern = re.compile(r'([\ws-]+): posts (small|big) blind \$(\d+\.\d{2})')
        players_posting_blind = pattern.findall(hand_info)
        return players_posting_blind
    
    def json_builder(self):
        
        jsons = []

        hand_infos = self.hand_info()
        hand_numbers = self.hand_numbers()

        for i, hand_info in enumerate(hand_infos):

            json = {
                'hand_number': hand_numbers[i],
                'game_type': self.game_type(hand_info),
                'blind_sizes': self.blind_sizes(hand_info),
                'button_seat_number': self.button_seat_number(hand_info),
                'playr_info': self.player_info(hand_info),
                'players_posting_blind': self.players_posting_blind(hand_info)
            }

            jsons.append(json)

        return jsons

    def parse_into_json(self):
        with open('table_info.json', 'w') as fp:
            json_string = json.dumps(self.json_builder(), default=lambda o:__dict__, indent=2)
            fp.write(json_string)

