# Parse Elections Canada table 11 (format 1996) to get all riding names/numbers
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
SGC_TO_ALPHA = {
    '10': 'NL', '11': 'PE', '12': 'NS', '13': 'NB', '24': 'QC', '35': 'ON', '46': 'MB', '47': 'SK', '48': 'AB', '59': 'BC', '60': 'YK', '61': 'NT', '62': 'N'
} # Provincial/Territory SGC code to 2-letter province code
ED_NAME = 1 # Column 1 is electoral district name
ED_NUM = 2  # Column 2 is electoral district number
RIDING_CSV_FIELDNAMES = {'code', 'province', 'en', 'fr'}

# Initialize variables
districts = {} # All districts
communities = {} # All communities

with open('data-source/ca_ge44_table_tableau11.csv', encoding='utf8') as table11:
    table_reader = csv.reader(table11)
    next(table_reader)  # skip the headers

    for district in table_reader:
        # Parse English/French names
        names = district[ED_NAME].split('/')
        name_en = names[0]
        if(len(names) > 1):
            name_fr = names[1]
        else:
            name_fr = names[0]
        sgc_code = district[ED_NUM][:2]

        # Add to dictionary of electoral districts
        if SGC_TO_ALPHA[sgc_code] not in districts:
            districts[SGC_TO_ALPHA[sgc_code]] = {}
        districts[SGC_TO_ALPHA[sgc_code]][district[ED_NUM]] = {'code': district[ED_NUM], 'province': SGC_TO_ALPHA[sgc_code], 'en': name_en, 'fr': name_fr}

        # Parse Communities
        # Use French name if in 24 (QC)
        if sgc_code == '24':
            district_communities = name_fr.split('--')
        else:
            district_communities = name_en.split('--')
        
        if SGC_TO_ALPHA[sgc_code] not in communities:
            communities[SGC_TO_ALPHA[sgc_code]] = []
        
        for com in district_communities:
            communities[SGC_TO_ALPHA[sgc_code]].append(com)

# JSON export ridings
export_json = open('data/ca-ridings.json', 'w')
json.dump(districts, export_json)
export_json.close()

# JSON export communities
export_json = open('data/ca-communities.json', 'w')
json.dump(communities, export_json)
export_json.close()

# CSV export ridings
with open('data/ca-ridings.csv', 'w', newline='', encoding='utf8') as export_csv:
    riding_writer = csv.writer(export_csv)
    for prov, prov_districts in districts.items():
        for code, district in prov_districts.items():
            riding_writer.writerow(district.values())

# CSV export communities
with open('data/ca-communities.csv', 'w', newline='', encoding='utf8') as export_csv:
    riding_writer = csv.writer(export_csv)
    for prov, prov_communities in communities.items():
        for c in prov_communities:
            riding_writer.writerow([prov, c])