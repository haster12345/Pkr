from table_info import TableInfo
from pre_flop_info import PreFlop
import json

class PokerStarsParser:
    """
    we take in hands and we call, in order, each parser. Each parser should take in the previous
    parser as an argument, so that each stage can use the information from the last one.
    """
    def __init__(self, hands):
        self.hands = hands

    def parse(self):
        json_table, json_pre = [], []
        for hand in self.hands:
            table_info  = TableInfo(hand).table_info()
            pre_flop = PreFlop(hand, table_info).pre_flop_info()
            json_table.append(table_info)
            json_pre.append(pre_flop)
        return json_table, json_pre
    
    def parse_into_json(self):
        table_info, pre_flop = self.parse()

        with open('pre_flop.json', 'w') as fp:
            json_string = json.dumps(pre_flop, default=lambda o: __dict__, indent=2)
            fp.write(json_string)

        with open('table_info.json', 'w') as fp:
            json_string = json.dumps(table_info, default=lambda o: __dict__, indent=2)
            fp.write(json_string)
        
        return 
