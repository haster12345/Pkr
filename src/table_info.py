import re
from decimal import Decimal

class TableInfo:

    def __init__(self, hand_text):
        self.hand_text = hand_text

    def hand_numbers(self, hand_content):
        pattern = re.compile(r'PokerStars Hand #(\d+):')
        match = pattern.findall(hand_content)
        match = [int(i) for i in match]
        return match

    def hand_info(self, hand_content):
        pattern = re.compile(r'([\s\S]*?)\*\*\* HOLE CARDS \*\*\*')
        hand_info: list = pattern.findall(hand_content)

        return hand_info[0]

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

        returns:{
        1 : ['player', palyer_chips, sit_out_bool],
        ...
        }
        """

        pattern = re.compile(r'(.+?) \((\$[0-9.]+) in chips\)( is sitting out)?')
        player_data = pattern.findall(hand_info)

        players = {}

        for player in player_data:
            cleaned_string = player[0].strip()
            parts = cleaned_string.split(": ")
            player_chips = Decimal(player[1][1:])
            sitting_out = (len(player[2]) != 0)

            players[int(f'{parts[0]}'[-1])] = [f'{parts[1]}', player_chips, sitting_out]

        for i in range(1, 6 + 1):
            if i not in players.keys():
                players[i] = ['', 0, True]

        return players

    def players_posting_blind(self, hand_info):
        pattern = re.compile(r'([\ws-]+): posts (small|big) blind \$(\d+\.\d{2})')
        players_posting_blind = pattern.findall(hand_info)
        blinds = [(i, j, Decimal(k)) for (i, j, k) in players_posting_blind]
        return blinds

    def blind_positions(self, players_posting_blind, player_info):
        sb_player, bb_player = players_posting_blind[0][0], players_posting_blind[1][0]

        sb_seat = 0
        bb_seat = 0

        for seat, values in player_info.items():
            if sb_player in values:
                sb_seat = seat

        for seat, values in player_info.items():
            if bb_player in values:
                bb_seat = seat

        return sb_seat, bb_seat

    def number_of_players(self, player_info):
        return len(player_info)

    @staticmethod
    def number_of_sitouts(player_info):
        counter = 0
        for i in player_info:
            if player_info[i][2]:
                counter += 1
        return counter

    @staticmethod
    def mapping_func(x):
        if x <= 6:
            return x
        else:
            return x - 6

    def position_finder(self, player_info, previous_seat):
        """
        params:
        - player_postion: int, from 1, 6
        - button_seat_number: int, from 1, 6
        - players_in_blinds: dict, {small: 'player1', big: 'player2'}

        returns: 
        position 

        given the last position, finds the next player who has not seated out
        """
        counter = 1
        next_position_seat = self.mapping_func(previous_seat + counter)
        next_position_sit_out: bool = player_info[next_position_seat][2]

        while next_position_sit_out:
            counter += 1
            next_position_seat = self.mapping_func(previous_seat + counter)
            player_data = player_info[next_position_seat]
            next_position_sit_out = player_data[2]

        return next_position_seat

    def next_posistion(self, position):
        positions = ['BN', 'SB', 'BB', 'LJ', 'HJ', 'CO']
        for i in range(len(positions)):
            if positions[i] == position:
                try:
                    return positions[i + 1]
                except IndexError:
                    return 'BN'

    def player_positions(self, player_info, bn_seat, blinds):

        sb_seat, bb_seat = self.blind_positions(players_posting_blind=blinds, player_info=player_info)
        lj_seat = self.position_finder(player_info, bb_seat)
        hj_seat = self.position_finder(player_info, lj_seat)
        co_seat = self.position_finder(player_info, hj_seat)

        player_positions = {
            'SB': player_info.get(sb_seat, ['', 0, True])[:2],
            'BB': player_info.get(bb_seat, ['', 0, True])[:2],
            'LJ': player_info.get(lj_seat, ['', 0, True])[:2],
            'HJ': player_info.get(hj_seat, ['', 0, True])[:2],
            'CO': player_info.get(co_seat, ['', 0, True])[:2],
            'BN': player_info.get(bn_seat, ['', 0, True])[:2],
        }

        return player_positions 

    def table_info(self):

        hand_info = self.hand_info(hand_content=self.hand_text)
        hand_numbers = self.hand_numbers(hand_content=self.hand_text)
        player_info = self.player_info(hand_info)
        button_seat_number = self.button_seat_number(hand_info)
        blinds = self.players_posting_blind(hand_info)
        player_info_str_keys = {str(i): k for i, k in player_info.items()}

        table_info = {
            'hand_number': hand_numbers[0],
            'hand': '',
            'game_type': self.game_type(hand_info),
            'blind_sizes': self.blind_sizes(hand_info),
            'button_seat_number': button_seat_number,
            'player_info': player_info_str_keys,
            'number_of_players_in_table': 6 - self.number_of_sitouts(player_info),
            'players_posting_blind': blinds,
            'player_positions': self.player_positions(player_info, button_seat_number, blinds)
        }

        return table_info

