import json
import re


class PreFlop:

    def __init__(self, file_content):
        # self.file_path = file_path
        self.file_content = file_content

    # @property
    # def pokerstars_file_content(self):
    #     with open(self.file_path, 'r') as file:
    #         pokerstars_file_content = file.read()
    #     return pokerstars_file_content

    def hand_numbers(self):
        pattern = re.compile(r'PokerStars Hand #(\d+):')
        match = pattern.findall(self.file_content)
        match = [int(i) for i in match]
        return match

    def get_pre_flop(self) -> list:
        pattern = re.compile(r'HOLE CARDS([\s\S]*?)(?:FLOP|SUMMARY)')
        pre_flops = pattern.findall(self.file_content)

        return pre_flops


    def get_hand(self, pre_flop):
        pre_flop_re = re.compile(r"Dealt to (\w+) \[([2-9TJQKA][cdhs] [2-9TJQKA][cdhs])\]")
        hand = pre_flop_re.findall(pre_flop)
        return hand

    def get_position(self, hand_number):
        """
        this should query the database with the hand number and return position of players
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
        """"
        output ideas:
        1) action : [c f r f f c f]
            -  this doesnt provide with much info by itself, everything must be implied
            - maybe this is better as notation is more comapct but needs functions to map actions to players
              and values for raises and calls is needed
        2) action: [['A', 'checks'], ['B', 'raises']]
            - same as above but now names are added and more information about actions


        """
        pattern = re.compile(r'(\S+):\s*(.*)')
        action_player_list = pattern.findall(text)
        actions = []        
        return action_player_list

    def get_pot_size(self):
        """
        """
        pass
    
    def json_builder(self):

        jsons = []

        for i, pre_flop in enumerate(self.get_pre_flop()):
            hand_number = self.hand_numbers()[i]
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
