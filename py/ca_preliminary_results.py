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
ED_NUM = 0  # Column 2 is electoral district number
ED_NAME_EN = 1 # Column 1 is electoral district name
ED_NAME_FR = 2
ED_RESULT_TYPE_EN = 3
CAN_LAST = 5
CAN_MIDDLE = 6
CAN_FIRST = 7
CAN_PARTY_EN = 8
CAN_PARTY_FR = 9
CAN_BALLOTS = 10
CAN_PERCENT_BALLOTS = 11
ED_REJECTED_BALLOTS = 12
ED_TOTAL_BALLOTS = 14


# Initialize variables
districts = {} # All districts

with open('data-source/ca_ge44_preliminary-2025-02-05.tsv', encoding='utf8') as prelim_file:
    table_reader = csv.reader(prelim_file, delimiter='\t')
    next(table_reader)  # skip the headers
    next(table_reader)  # skip the headers

    for candidate in table_reader:
        if candidate[0][0] == '*':
            continue
        sgc_code = candidate[ED_NUM][:2]

        if SGC_TO_ALPHA[sgc_code] == 'QC':
            ed_name = candidate[ED_NAME_EN]
        else:
            ed_name = candidate[ED_NAME_FR]

        # Add to dictionary of electoral districts
        if candidate[ED_NUM] not in districts:
            districts[candidate[ED_NUM]] = []
        districts[candidate[ED_NUM]].append({
            'name_first': candidate[CAN_FIRST],
            'name_middle': candidate[CAN_MIDDLE],
            'name_last': candidate[CAN_LAST],
            'party': candidate[CAN_PARTY_EN],
            'count_ballots': candidate[CAN_BALLOTS],
            'percent_ballots': candidate[CAN_PERCENT_BALLOTS]
        })
        # if SGC_TO_ALPHA[sgc_code] not in districts:
        #     districts[SGC_TO_ALPHA[sgc_code]] = {}
        # districts[SGC_TO_ALPHA[sgc_code]][district[ED_NUM]] = {'code': district[ED_NUM], 'province': SGC_TO_ALPHA[sgc_code], 'en': name_en, 'fr': name_fr}

        # print("[",candidate[ED_NUM], candidate[CAN_PARTY_EN],"]", sep="", end="")
        # # Parse Communities
        # # Use French name if in 24 (QC)
        
        # if SGC_TO_ALPHA[sgc_code] not in communities:
        #     communities[SGC_TO_ALPHA[sgc_code]] = []
        
        # for com in district_communities:
        #     communities[SGC_TO_ALPHA[sgc_code]].append(com)

# JSON export ridings
export_json = open('data/preliminary_results.json', 'w')
json.dump(districts, export_json)
export_json.close()

# # JSON export communities
# export_json = open('data/ca-communities.json', 'w')
# json.dump(communities, export_json)
# export_json.close()

# CSV export ridings
with open('data/preliminary_results.csv', 'w', newline='', encoding='utf8') as export_csv:
    riding_writer = csv.writer(export_csv)
    for ed_num, candidates in districts.items():
        for candidate in candidates:
            riding_writer.writerow([ed_num, candidate['name_first'], candidate['name_middle'], candidate['name_last'], candidate['party'], candidate['count_ballots'], candidate['percent_ballots']])

# # CSV export communities
# with open('data/ca-communities.csv', 'w', newline='', encoding='utf8') as export_csv:
#     riding_writer = csv.writer(export_csv)
#     for prov, prov_communities in communities.items():
#         for c in prov_communities:
#             riding_writer.writerow([prov, c])