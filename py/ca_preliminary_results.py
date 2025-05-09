# Parse Elections Canada preliminary results to get all riding names/numbers
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


from __init__ import *
import csv, json


# Initialize variables
districts = {} # All districts
parties = set()
last_result_type = ""
last_ed = ""
first_result = True

with open(CA_PARTIES_MAP_JSON) as party_id_file:
    party_id = json.load(party_id_file)
    party_names = party_id.keys()

# Process all lines. Skip 2 header lines, skip footnotes (at end).
# Track if this is the first 

with open(CA_GE_PRELIMINARY, encoding='utf8') as prelim_file:
    table_reader = csv.reader(prelim_file, delimiter='\t')
    next(table_reader) # skip the headers
    next(table_reader)

    for candidate in table_reader:

        if candidate[PRELIM_ED_RESULT_TYPE_EN] != last_result_type or candidate[PRELIM_ED_NUM] != last_ed:
            last_result_type = candidate[PRELIM_ED_RESULT_TYPE_EN]
            last_ed = candidate[PRELIM_ED_NUM]
            first_result = True
        
        if candidate[0][0] == '*': continue # Skip if a footnote

        sgc_code = candidate[PRELIM_ED_NUM][:2] # TODO: remove if results not segmented by province

        if SGC_TO_ALPHA[sgc_code] != 'QC':
            ed_name = candidate[PRELIM_ED_NAME_EN]
        else:
            ed_name = candidate[PRELIM_ED_NAME_FR] # Use french name if in Quebec

        # Add to dictionary of electoral districts if first result.
        # This will overwrite preliminary results, if present.
        if first_result:
            districts[candidate[PRELIM_ED_NUM]] = []
            first_result = False
        districts[candidate[PRELIM_ED_NUM]].append({
            'name_first': candidate[PRELIM_CAN_FIRST],
            'name_middle': candidate[PRELIM_CAN_MIDDLE],
            'name_last': candidate[PRELIM_CAN_LAST],
            'party': candidate[PRELIM_CAN_PARTY_EN],
            'count_ballots': candidate[PRELIM_CAN_BALLOTS],
            'percent_ballots': candidate[PRELIM_CAN_PERCENT_BALLOTS]
        })
        
        if candidate[PRELIM_CAN_PARTY_EN] not in party_names:
            parties.add(candidate[PRELIM_CAN_PARTY_EN])
            parties.add(candidate[PRELIM_CAN_PARTY_FR])

# JSON export ridings
export_json = open('data/preliminary_results.json', 'w')
json.dump(districts, export_json)
export_json.close()

# CSV export ridings
with open('data/preliminary_results.csv', 'w', newline='', encoding='utf8') as export_csv:
    riding_writer = csv.writer(export_csv)
    for ed_num, candidates in districts.items():
        for candidate in candidates:
            riding_writer.writerow([ed_num, candidate['name_first'], candidate['name_middle'], candidate['name_last'], candidate['party'], candidate['count_ballots'], candidate['percent_ballots']])

print(parties)