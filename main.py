from populate_tables import populate_table_all_files


def main(folder_path):
    """
    iterate through a directory and pass each file into the parser
    """
    #for filename in os.listdir(folder_path):
    #    if filename[-3:]  == 'txt':
    #        hands = FileContent(folder_name=folder_path,file_name=filename).hands()
    #        PokerStarsParser(hands).parse_into_son()

    return populate_table_all_files(folder_path)

if __name__ == '__main__':
    main('~./Programmes/Pkr/hastermaster/')
