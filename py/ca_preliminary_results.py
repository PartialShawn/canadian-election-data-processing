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

print()
print("Parsing preliminary elections results...")

print(" - loading parties map data")
with open(CA_PARTIES_MAP_JSON_FILENAME) as party_id_file:
    party_id = json.load(party_id_file)
    party_names = party_id.keys()

# Process all lines. Skip 2 header lines, skip footnotes (at end).
# Track if this is the first 

print(" - loading preliminary results")
with open(CA_GE_PRELIMINARY, encoding='utf8') as prelim_file:
    table_reader = csv.reader(prelim_file, delimiter='\t')
    next(table_reader) # skip the headers
    next(table_reader)

    for candidate in table_reader:

        # Check if validated results or new district
        """
            The preliminary results TSV lists all district results first as
            preliminary results, and then again as validated results. In
            either case, treat this as if starting a new district by creating
            (or clearing in the case of validated results) a blank dictionary
            for the district.

            This removes the preliminary results if there are validated
            results.
        """ 
        if candidate[PRELIM_ED_RESULT_TYPE_EN] != last_result_type or candidate[PRELIM_ED_NUM] != last_ed:
            last_result_type = candidate[PRELIM_ED_RESULT_TYPE_EN]
            last_ed = candidate[PRELIM_ED_NUM]
            first_result = True
        
        if candidate[0][0] == '*': continue # Skip if a footnote

        # Add to dictionary of electoral districts if first result.
        # This will overwrite preliminary results, if present.
        if first_result:
            districts[candidate[PRELIM_ED_NUM]] = {
                # 'population': ,
                # 'electors': ,
                'ballots': candidate[PRELIM_ED_TOTAL_BALLOTS],
                # 'ballots_percent_electors': ,
                'rejected_ballots': candidate[PRELIM_ED_REJECTED_BALLOTS],
                # 'rejected_percent': ,
                # 'valid_ballots': ,
                # 'valid_percent': ,
                'candidates': []
            }
            first_result = False
        districts[candidate[PRELIM_ED_NUM]]['candidates'].append({
            'name_first': candidate[PRELIM_CAN_FIRST],
            'name_middle': candidate[PRELIM_CAN_MIDDLE],
            'name_last': candidate[PRELIM_CAN_LAST],
            'party': candidate[PRELIM_CAN_PARTY_EN],
            'count_ballots': candidate[PRELIM_CAN_BALLOTS],
            'percent_ballots': candidate[PRELIM_CAN_PERCENT_BALLOTS]
        })
        
        # Check for missing data
        if candidate[PRELIM_CAN_PARTY_EN] not in party_names:
            parties.add(candidate[PRELIM_CAN_PARTY_EN])
            parties.add(candidate[PRELIM_CAN_PARTY_FR])

print(" - parsed",len(districts),"districts")

if len(parties) > 0:
    print(' - parties not found in party map:',parties)

print(' - writing JSON file')
# JSON export ridings
export_json = open(CA_ELECTIONS_RESULTS_OUTPUT[CA_GE_PRELIMINARY_ELECTION_NUMBER], 'w')
json.dump(districts, export_json, indent=2)
export_json.close()

print(' ... done.')
print()