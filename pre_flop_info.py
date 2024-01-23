import re


class PreFlop:

    def __init__(self, file_path):
        self.file_path = file_path

    @property
    def pokerstars_file_content(self):
        with open(self.file_path, 'r') as file:
            pokerstars_file_content = file.read()
        return pokerstars_file_content

    def hand_numbers(self, text):
        pattern = re.compile(r'PokerStars Hand #(\d+):')
        match = pattern.findall(text)
        match = [int(i) for i in match]
        return match

    def get_pre_flop(self) -> list:
        pattern = re.compile(r'HOLE CARDS([\s\S]*?)(?:FLOP|SUMMARY)')
        pre_flops = pattern.findall(self.pokerstars_file_content)

        return pre_flops

    def get_hand(self):
        
        pre_flops = self.get_pre_flop()

        hands = []

        for pre_flop in pre_flops:

            hand_number = self.hand_numbers(pre_flop)
            pre_flop_re = re.compile(r"Dealt to (\w+) \[([2-9TJQKA][cdhs] [2-9TJQKA][cdhs])\]")
            hand = pre_flop_re.findall(self.pokerstars_file_content)
            hands.append((hand, hand_number))

        return hands


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

    def get_action(self):
        """
        example output: [x c] = Check call
        """
        pass

    def get_pot_size(self):
        """
        """
        pass
    
    def json_builder(self):

        for hand_number in self.hand_numbers():
            
            hand, hand_number = self.get_hand()

            json = {
                'hand_number' : int(hand_number),
                'hand': hand,
                'position': self.get_position(),
                'action' : self.get_action(),
                'players_in_pot' : int(),
                'pot_size' : float(),
                'villain_positions' : list() 
            }                        




inst = PreFlop(file_path="hastermaster/HH20231118 Aigyptios - $0.05-$0.10 - USD No Limit Hold'em.txt")
print(inst.get_pre_flop())
