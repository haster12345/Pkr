import json
import re


class PreFlop:

    def __init__(self, hand_text: str, table_info: dict):
        self.table_info = table_info
        self.hand_text = hand_text

    def hand_numbers(self, hand_content):
        pattern = re.compile(r'PokerStars Hand #(\d+):')
        match = pattern.findall(hand_content)
        match = [int(i) for i in match]
        return match

    def pre_flops(self, hand_content) -> list:
        pattern = re.compile(r'HOLE CARDS([\s\S]*?)(?:FLOP|SUMMARY)')
        pre_flops = pattern.findall(hand_content)

        return pre_flops[0]

    def hand_dealt(self, pre_flop):
        pre_flop_re = re.compile(r"Dealt to (\w+) \[([2-9TJQKA][cdhs] [2-9TJQKA][cdhs])\]")
        hand = pre_flop_re.findall(pre_flop)
        return hand
    
    @staticmethod
    def hero_name():
        return 'hastermaster'

    def hero_position(self):
        player_positions = self.table_info['player_positions']
        hero_position = ''

        for key, value in player_positions.items():
            if value[0] == self.hero_name():
                hero_position = key
                break

        return hero_position

    def villain_position(self, hero_position, players_in_pot):
        """
        example output [ "LJ vs HJ", "LJ vs BN"]
        """
        villain_positions = []

        if self.hero_name() in players_in_pot:
            for player, position in players_in_pot.items():

                if player != self.hero_name():
                    villain_positions.append(f'{hero_position} vs {position}')

        return villain_positions

    def player_positions(self):
        player_positions = {player[0]: position for (position, player) in self.table_info['player_positions'].items()}
        return player_positions

    def get_players_in_pot(self, action):
        """
        if a player folds then they are not in the pot
        """
        player_positions = self.player_positions()

        players_in_pot = dict()
        for action_line in action:
            player = action_line[0]
            player_action = action_line[1]

            if player_action != "folds ":
                players_in_pot[player] = player_positions[player] 
            
            elif (player in players_in_pot) and action != "doesn't show hand ":
                del players_in_pot[player]

        return players_in_pot

    def action(self, pre_flop):
        """
        output:
        CURRENT: 
          action: [['A', 'checks'], ['B', 'raises to $0.30']] - current
            - same as above but now names are added and more information about actions
        """
        pattern = re.compile(r'(\S+):\s*(.*)')
        action_player_list = pattern.findall(pre_flop)
        return action_player_list
    

    def blinds(self):
        """
        returns the value of total blinds posted
        """
        sb_size, bb_size = self.table_info['blind_sizes']
        players_posting_bb = len(self.table_info['players_posting_blind'])
        blinds_posted = float(sb_size) + players_posting_bb * float(bb_size)

        return blinds_posted

    def action_identifier(self, action_line: str):
        """
        given an action line, identify the action and if the action is agressive output the size of raise
        """
        split_str = action_line.split()
        action = split_str[0]
        amount = 0

        if split_str[-1] == 'all-in':
            amount = float(split_str[3][1:])

        elif action not in ("checks", "folds", "doesn't"):
            amount = float(split_str[-1][1:])

        return action, amount

    def pot_size(self, blinds, actions):
        """
        -keep track of blinds, bets, raises, calls
        iterate through actions, 
        """
        pot = blinds
        player_money = dict()

        for player_posting_blind in self.table_info['players_posting_blind']:
            player = player_posting_blind[0]
            amount = float(player_posting_blind[2])
            player_money[player] = amount


        for action_line in actions:
            player = action_line[0]
            action, amount = self.action_identifier(action_line[1])

            if player in player_money:
                player_amount = player_money[player]

                if action == 'raises':
                    player_money[player] = amount

                else:
                    player_money[player] = amount + player_amount
            else:
                player_money[player] = amount
        
        pot += round(sum(player_money.values()), 2)

        return pot

    def pre_flop_info(self):
        pre_flop = self.pre_flops(hand_content=self.hand_text)
        hand_number = self.hand_numbers(hand_content=self.hand_text)
        hand = self.hand_dealt(pre_flop)
        blinds = self.blinds()
        action = self.action(pre_flop)
        hero_position = self.hero_position()
        players_in_pot = self.get_players_in_pot(action)

        pre_flop_info = {
            'hand_number': hand_number[0],
            'hand': hand,
            'hero_position': self.hero_position(),
            'action': self.action(pre_flop),
            'players_in_pot': players_in_pot, 
            'pot_size': self.pot_size(blinds, action),
            'villain_positions': self.villain_position(hero_position, players_in_pot),
            'hero_position' : self.hero_position()
        }

        return pre_flop_info

    def parse_into_json(self):
        with open('pre_flop.json', 'w') as fp:
            json_string = json.dumps(self.json_builder(), default=lambda o: __dict__, indent=2)
            fp.write(json_string)
