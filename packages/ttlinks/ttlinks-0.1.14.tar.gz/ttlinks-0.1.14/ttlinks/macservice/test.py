from ttlinks.macservice.oui_file_parsers import OuiFileParser

if __name__ == '__main__':
    # file_path = 'resources/default_iab.txt'
    # file_path = 'resources/default_iab.csv'
    # file_path = 'resources/default_mas.txt'
    # file_path = 'resources/default_mas.csv'
    # file_path = 'resources/default_mam.txt'
    # file_path = 'resources/default_mam.csv'
    # file_path = 'resources/default_mal.txt'
    # file_path = 'resources/default_mal.csv'
    # file_path = 'resources/default_cid.txt'
    file_path = 'resources/default_cid.csv'
    result = OuiFileParser.parse_oui_file(file_path)
    for oui_unit in result['oui_units']:
        print(oui_unit.record)
