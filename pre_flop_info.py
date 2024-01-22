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

    def get_pre_flop(self):
        pattern = re.compile(r'HOLE CARDS([\s\S]*?)(?:FLOP|SUMMARY)')
        match = pattern.findall(self.pokerstars_file_content)

        for i in match:
            print(i)

        return match

    def get_hand(self):
        
        


        hands_re = re.compile(r"Dealt to (\w+) \[([2-9TJQKA][cdhs] [2-9TJQKA][cdhs])\]")
        hands = hands_re.findall(self.get_pre_flop())



        hands = [hand, hand_number]
        

        pass

    def get_position(self):
        pass
    

    def json_builder(self):

        for hand_number in self.hand_numbers():
            json = {
                'hand_number' : hand_number,
                'hand': self.get_hand(),
                'position': self.get_position() 
            }                        




inst = PreFlop(file_path="hastermaster/HH20231118 Aigyptios - $0.05-$0.10 - USD No Limit Hold'em.txt")
print(inst.get_pre_flop())
