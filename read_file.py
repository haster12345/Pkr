import os
import re

class FileContent:

    def __init__(self, file_name, folder_name):
        self.folder_name = folder_name
        self.file_name = file_name

    def read_file(self):
        with open(f'{self.folder_name}{self.file_name}') as file:
            return file.read()

    def hands(self):
        pattern = re.compile(r'PokerStars Hand #\d+:[\s\S]*?(?=\n\n\nPokerStars Hand #|\Z|\n*$)')
        hands = [pattern.findall(file_content) for file_content in self.read_file()]
        return hands