import json
import re


class PreFlop:

    def __init__(self, file_path):
        self.file_path = file_path

    @property
    def pokerstars_file_content(self):
        with open(self.file_path, 'r') as file:
            pokerstars_file_content = file.read()
        return pokerstars_file_content

    def hand_numbers(self):
        pattern = re.compile(r'PokerStars Hand #(\d+):')
        match = pattern.findall(self.pokerstars_file_content)
        match = [int(i) for i in match]
        return match

    def get_pre_flop(self) -> list:
        pattern = re.compile(r'HOLE CARDS([\s\S]*?)(?:FLOP|SUMMARY)')
        pre_flops = pattern.findall(self.pokerstars_file_content)

        return pre_flops


    def get_hand(self, pre_flop):
        pre_flop_re = re.compile(r"Dealt to (\w+) \[([2-9TJQKA][cdhs] [2-9TJQKA][cdhs])\]")
        hand = pre_flop_re.findall(pre_flop)
        return hand

    def get_position(self, hand_number):
        """
        this should query the database with the hand number and return the position
        """

        pass    
    
    def get_villain_position(self, hand_number):
        """
        this should query the database with the hand number and get the hero position
        then we check who is in the pot, and assign then positions
        """
        pass

    def get_palyers_in_pot(self):
        pass

    def get_action(self, text):
        """
        example output: [x c] = Check call
        """
        pattern = re.compile(r'(\S+):\s*(.*)')
        matches = pattern.findall(text)
        return matches

    def get_pot_size(self):
        """
        """
        pass
    
    def json_builder(self):

        print(len(self.get_pre_flop()))
        print(len(self.hand_numbers()))

        jsons = []

        for i, pre_flop in enumerate(self.get_pre_flop()):
            print(pre_flop)
            hand_number = self.hand_numbers()[i]
            print(hand_number)
            hand = self.get_hand(pre_flop)

            
            json = {
                'hand_number' : hand_number,
                'hand': hand,
                'position': self.get_position(hand_number),
                'action' : self.get_action(pre_flop),
                'players_in_pot' : self.get_palyers_in_pot(),
                'pot_size' : self.get_pot_size(),
                'villain_positions' : self.get_villain_position(hand_number)
            }                        

            jsons.append(json)

        return jsons

    def parse_into_json(self):
        with open('pre_flop.json', 'w') as fp:
            json_string = json.dumps(self.json_builder(), default=lambda o:__dict__, indent=2)
            fp.write(json_string)



inst = PreFlop(file_path="hastermaster/HH20231118_Aigyptios_-_0.05-0.10_-_USD_No_Limit_Holdem.txt")
inst.parse_into_json()