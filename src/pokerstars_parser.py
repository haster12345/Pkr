from table_info import TableInfo
from pre_flop_info import PreFlop

class PokerStarsParser:
    """
    we take in hands and we call, in order, each parser. Each parser should take in the previous
    parser as an argument, so that each stage can use the information from the last one.
    """
    def __init__(self, hands):
        self.hands = hands

    def parse(self):
        json_table, json_pre = [], []
        item_list = []
        for hand in self.hands:
            table_info  = TableInfo(hand).table_info()
            pre_flop = PreFlop(hand, table_info).pre_flop_info()
            json_table.append(table_info)
            json_pre.append(pre_flop)
            item_list.append(table_info | pre_flop)
        return json_table, json_pre, item_list
