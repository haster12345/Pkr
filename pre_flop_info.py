import json
import re


class PreFlop():

    def __init__(self, file_content, table_info):
        self.table_info = table_info
        self.file_content = file_content

    def hand_numbers(self, hand_content):
        pattern = re.compile(r'PokerStars Hand #(\d+):')
        match = pattern.findall(hand_content)
        match = [int(i) for i in match]
        return match

    def pre_flops(self, hand_content) -> list:
        pattern = re.compile(r'HOLE CARDS([\s\S]*?)(?:FLOP|SUMMARY)')
        pre_flops = pattern.findall(hand_content)

        return pre_flops

    def hand_dealt(self, pre_flop):
        pre_flop_re = re.compile(r"Dealt to (\w+) \[([2-9TJQKA][cdhs] [2-9TJQKA][cdhs])\]")
        hand = pre_flop_re.findall(pre_flop)
        return hand

    def get_position(self, hand_number):
        """
        """

        pass    
    
    def get_villain_position(self, hand_number):
        """
        then we check who is in the pot, and assign then positions
        """
        pass

    def get_palyers_in_pot(self):
        pass

    def action(self, pre_flop):
        """"
        output:
        FUTURE:
          action : [c f r f f c f]
            - easier to query, requires keeping track of players, player positions, raise and bet amounts
        CURRENT: 
          action: [['A', 'checks'], ['B', 'raises']] - current
            - same as above but now names are added and more information about actions
        """
        pattern = re.compile(r'(\S+):\s*(.*)')
        action_player_list = pattern.findall(pre_flop)
        return action_player_list

    def blinds(self):
        pass


    def get_pot_size(self, blinds):
        """
        -keep track of blinds, bets, raises, calls
        iterate through actions, 

        """
        pot = blinds
        pass
    
    def json_builder(self):

        jsons = []

        # for i, pre_flop in enumerate(self.pre_flops()):
        for hand in self.file_content:
            pre_flop = self.pre_flops(hand_content=hand)[0]
            hand_number = self.hand_numbers(hand_content=hand)[0]
            hand = self.hand_dealt(pre_flop)
            blinds = self.blinds
            
            json = {
                'hand_number' : hand_number,
                'hand': hand,
                'position': self.get_position(hand_number),
                'action' : self.action(pre_flop),
                'players_in_pot' : self.get_palyers_in_pot(),
                'pot_size' : self.get_pot_size(blinds),
                'villain_positions' : self.get_villain_position(hand_number)
            }                        

            jsons.append(json)

        return jsons

    def parse_into_json(self):
        with open('pre_flop.json', 'w') as fp:
            json_string = json.dumps(self.json_builder(), default=lambda o:__dict__, indent=2)
            fp.write(json_string)
