# Parse Elections Canada preliminary results (GE45) to get all riding names/numbers
# Parse riding names to get communities names.
#
# -----------------------------------------------------------------------------
#           Licensed under the Apache License, Version 2.0
# -----------------------------------------------------------------------------
#
# Parses table 11, extracting the names of all districts.
#
# Then parses district names as a possible set of names of the communities
# that make up that district. Uses French name when in QC. Otherwise,
# it is usually taking a division of a municipality (north, etc) and
# translating that, unless it's near something that has an official
# name, such as a lake.



import csv, json

# Set Constants

# Column numbers
ED_NUM = 0
ED_NAME_EN = 1
ED_NAME_FR = 2

# Initialize variables
districts_by_province = {} # All districts grouped by province
districts_index = {} # All districts with district number as key
communities = {} # All communities

SGC_TO_ALPHA = {
    '10': 'NL', '11': 'PE', '12': 'NS', '13': 'NB', '24': 'QC', '35': 'ON', '46': 'MB', '47': 'SK', '48': 'AB', '59': 'BC', '60': 'YK', '61': 'NT', '62': 'N'
} # Provincial/Territory SGC code to 2-letter province code

with open('data-source/ca_ge44_preliminary-2025-02-05.tsv', encoding='utf8') as prelim:
    table_reader = csv.reader(prelim, delimiter='\t')
    next(table_reader)  # skip the headers
    next(table_reader)

    for district in table_reader:

        if district[0][0] == '*': continue # Skip if a footnote
        sgc_code = district[ED_NUM][:2]
        # Add to dictionary of electoral districts
        districts_index[district[ED_NUM]] = {'code': district[ED_NUM], 'province': SGC_TO_ALPHA[sgc_code], 'en': district[ED_NAME_EN], 'fr': district[ED_NAME_FR]}


# JSON export index of all districts
export_json = open('data/ca-districts-index.json', 'w', encoding='utf8')
json.dump(districts_index, export_json)
export_json.close()