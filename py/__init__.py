# Elections Canada Files
CA_GE_PRELIMINARY = "data-source/ca_ge44_preliminary-2025-05-09.tsv"
CA_GE_DATAFILES = {
    44: {
        'TABLE1': 'data-source/ca_ge44_table_tableau01.csv',
        'TABLE2': 'data-source/ca_ge44_table_tableau02.csv',
        'TABLE3': 'data-source/ca_ge44_table_tableau03.csv',
        'TABLE4': 'data-source/ca_ge44_table_tableau04.csv',
        'TABLE5': 'data-source/ca_ge44_table_tableau05.csv',
        'TABLE6': 'data-source/ca_ge44_table_tableau06.csv',
        'TABLE7': 'data-source/ca_ge44_table_tableau07.csv',
        'TABLE8': 'data-source/ca_ge44_table_tableau08.csv',
        'TABLE9': 'data-source/ca_ge44_table_tableau09.csv',
        'TABLE10': 'data-source/ca_ge44_table_tableau10.csv',
        'TABLE11': 'data-source/ca_ge44_table_tableau11.csv',
        'TABLE12': 'data-source/ca_ge44_table_tableau12.csv',
    }
}

CA_ELECTIONS_RESULTS_OUTPUT = {
    '45': 'data/ca_ge45_results.json',
    '44': 'data/ca_ge44_results.json'
}

CA_PARTIES_MAP_SOURCE = "data-source/ca_parties_map.csv"
CA_PARTIES_SOURCE = "data-source/ca_parties.csv"
CA_PARTIES_MAP_JSON_FILENAME = "data/ca_parties_map.json"
CA_PARTIES_JSON_FILENAME = "data/ca_parties.json"

CA_DISTRICTS_INDEX_FILENAME = 'data/ca_districts_index.json'

# Zola export
ZOLA_FEDERAL_PATH = '../votes-count-zola/content/ca/'
ZOLA_FEDERAL_DISTRICTS_PATH = '../votes-count-zola/content/ca/districts/'
ZOLA_FEDERAL_ELECTIONS_PATH = '../votes-count-zola/content/ca/elections/'
ZOLA_FEDERAL_DISTRICTS_JSON = '../votes-count-zola/content/ca/districts/preliminary_results.json'

# Provincial/Territory SGC code to 2-letter province code & vice versa
SGC_TO_ALPHA = { '10': 'NL', '11': 'PE', '12': 'NS', '13': 'NB', '24': 'QC', '35': 'ON', '46': 'MB', '47': 'SK', '48': 'AB', '59': 'BC', '60': 'YK', '61': 'NT', '62': 'NU' }

ALPHA_TO_SGC = {'NL': '10', 'PE': '11', 'NS': '12', 'NB': '13', 'QC': '24', 'ON': '35', 'MB': '46', 'SK': '47', 'AB': '48', 'BC': '59', 'YK': '60', 'NT': '61', 'NU': '62'}

# Preliminary TSV columns
PRELIM_ED_NUM = 0  # Column 2 is electoral district number
PRELIM_ED_NAME_EN = 1 # Column 1 is electoral district name
PRELIM_ED_NAME_FR = 2
PRELIM_ED_RESULT_TYPE_EN = 3
PRELIM_ED_RESULT_TYPE_EN = 4
PRELIM_CAN_LAST = 5
PRELIM_CAN_MIDDLE = 6
PRELIM_CAN_FIRST = 7
PRELIM_CAN_PARTY_EN = 8
PRELIM_CAN_PARTY_FR = 9
PRELIM_CAN_BALLOTS = 10
PRELIM_CAN_PERCENT_BALLOTS = 11
PRELIM_ED_REJECTED_BALLOTS = 12
PRELIM_ED_TOTAL_BALLOTS = 13

# parties.csv columns
PARTIES_ID = 0
PARTIES_SHORT_EN = 1
PARTIES_SHORT_FR = 2
PARTIES_COMMON_EN = 3
PARTIES_COMMON_FR = 4
PARTIES_LONG_EN = 5
PARTIES_LONG_FR = 6
PARTIES_REGISTERED = 7
PARTIES_DEREGISTERED = 8
PARTIES_WEBSITE_EN = 9
PARTIES_WEBSITE_FR = 10