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
        return int(button_seat_number[0])
        
    def player_info(self, hand_info):
        """
        player_data example : [ ('Seat 3: NickSolo69', '$10', 'is sitting out'), ...]
        """

        pattern = re.compile(r'(.+?) \((\$[0-9.]+) in chips\)( is sitting out)?')
        player_data = pattern.findall(hand_info)

        players = {}

        for player in player_data:
            cleaned_string = player[0].strip()
            parts = cleaned_string.split(": ")
            player_chips = float(player[1][1:])
            sitting_out = (len(player[2]) != 0)

            players[int(f'{parts[0]}'[-1])] = [f'{parts[1]}', player_chips, sitting_out]

        for i in range(1, 6 + 1):
            if i not in players.keys():
                players[i]  = ['', 0, True]

        return players
    
    def players_posting_blind(self, hand_info):
        pattern = re.compile(r'([\ws-]+): posts (small|big) blind \$(\d+\.\d{2})')
        players_posting_blind = pattern.findall(hand_info)
        return players_posting_blind
    
    def number_of_players(self, player_info):
            return len(player_info)
    
    @staticmethod
    def number_of_sitouts(player_info):
        counter = 0
        for i in player_info:
            if player_info[i][2]:
                counter += 1
        return counter
    
    def mapping_func(self, x):
        if x <= 6:
            return x
        else:
            return x - 6
    
    def player_positions(self, player_info, button_seat_number):
        """
        small_blind = button number + 1
        big_blind = small blind + 1
        ...

        only need to check if each player is sitting out

        [1 2 3 4 5 6] -> [2 3 4 5 6]
        - if player 1 is sitting out: player_info['1'][2] == True

        """ 

        number_of_players = self.number_of_players(player_info)
        number_of_sitouts = self.number_of_sitouts(player_info)

        player_positions = {}
        
        if (number_of_sitouts == 0):
            player_positions  = {
                'SB': player_info[self.mapping_func(button_seat_number + 1)][:2],
                'BB': player_info[self.mapping_func(button_seat_number + 2)][:2],
                'LJ': player_info[self.mapping_func(button_seat_number + 3)][:2],
                'HJ': player_info[self.mapping_func(button_seat_number + 4)][:2],
                'CO': player_info[self.mapping_func(button_seat_number + 5)][:2],
                'BN': player_info[self.mapping_func(button_seat_number)][:2]
            }

        return player_positions    

    def json_builder(self):
        
        jsons = []

        hand_infos = self.hand_info()
        hand_numbers = self.hand_numbers()

        for i, hand_info in enumerate(hand_infos):
            player_info = self.player_info(hand_info)
            button_seat_number = self.button_seat_number(hand_info)
            
            json = {
                'hand_number': hand_numbers[i],
                'game_type': self.game_type(hand_info),
                'blind_sizes': self.blind_sizes(hand_info),
                'button_seat_number': button_seat_number,
                'player_info': player_info,
                'number_of_sitouts': self.number_of_sitouts(player_info),
                'players_posting_blind': self.players_posting_blind(hand_info),
                'player_positions': self.player_positions(player_info, button_seat_number)
            }

            jsons.append(json)

        return jsons

    def parse_into_json(self):
        with open('table_info.json', 'w') as fp:
            json_string = json.dumps(self.json_builder(), default=lambda o:__dict__, indent=2)
            fp.write(json_string)

