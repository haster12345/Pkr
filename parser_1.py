import re
import json


class Parser:

    def __init__(self, file_path):
        self.file_path = file_path

        with open(self.file_path, 'r') as file:
            self.pokerstars_file_content = file.read()

    def file_parser_table_info(self):

        table_info_re = re.compile(

            r"PokerStars Hand #(\d+):  (\S+) No Limit \(\$([0-9.]+)\/\$([0-9.]+) USD\) - "
            r"(\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2}) \w+ \[\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2} ET\]\s+"
            r"Table '(\w+)' (\d+-max) Seat #(\d+) is the button|Seat (\d+): "
            r"(.+?) \((\$[0-9.]+) in chips\)( is sitting out)?|"
            r"([\ws-]+): posts (small|big) blind \$(\d+\.\d{2})")

        table_info: list[tuple] = table_info_re.findall(self.pokerstars_file_content)

        return table_info

    @staticmethod
    def hand_number(hand_text):
        pattern = re.compile(r'PokerStars Hand #(\d+):')
        match = pattern.search(hand_text)

        if match:
            hand_number = match.group(1)
            return int(hand_number), True
        else:
            return 0, False

    def parser_table_info(self):

        table_info = self.file_parser_table_info()
        table_info_json = []
        table_info_dict = {}

        for index, tuples in enumerate(table_info):
            
            if tuples[0] != '':

                current_hand_number = tuples[0]
                seats: list = []
                blinds_dict: dict = {}

                table_info_dict = {'hand_number': int(tuples[0]),
                                   'game_type': tuples[1],
                                   'small_blind': float(tuples[2]),
                                   'big_blind': float(tuples[3]),
                                   'time': tuples[4],
                                   'table_name': tuples[5],
                                   'max_players': int(tuples[6][0]),
                                   'button_seat_number': int(tuples[7]),
                                   'seats': seats,
                                   'blinds': blinds_dict}

                for sub_tuple in table_info[index + 1:]:

                    if sub_tuple[0] != '' and sub_tuple[0] != current_hand_number:
                        break

                    if sub_tuple[12] != '':
                        break

                    seats_dict = {
                        "seat_number": int(sub_tuple[8]),
                        "player_name": sub_tuple[9],
                        "currency": sub_tuple[10][0],
                        "amount": float(sub_tuple[10][1:]),
                        "sitting_out": bool(sub_tuple[11]),
                        "position": ""
                    }

                    seats.append(seats_dict)

                blinds = []
                for sub_tuple in table_info[index + 1:]:

                    if sub_tuple[0] != '' and sub_tuple[0] != current_hand_number:
                        break

                    if sub_tuple[12] != '':
                        blinds.append(sub_tuple[12])

                table_info_dict['blinds'] = blinds
                table_info_dict['seats'] = seats

            table_info_json.append(table_info_dict)

        return table_info_json

    def parse_into_json(self):
        with open('table_info.json', 'w') as fp:
            json_string = json.dumps(self.parser_table_info(), default=lambda o: o.__dict__, indent=2)
            fp.write(json_string)


# Parser(file_path="hastermaster/HH20231118_Aigyptios_-_0.05-0.10_-_USD_No_Limit_Holdem.txt").parse_into_json()
