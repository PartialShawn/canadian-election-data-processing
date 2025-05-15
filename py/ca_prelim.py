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


def district_init(district: dict) -> dict:
    ballots_valid = int(district[PRELIM_ED_TOTAL_BALLOTS])-int(district[PRELIM_ED_REJECTED_BALLOTS])
    ballots_rej_per = round(int(district[PRELIM_ED_REJECTED_BALLOTS])/int(district[PRELIM_ED_TOTAL_BALLOTS]), 1)
    return {
        'num': district[PRELIM_ED_NUM],
        'status': district[PRELIM_ED_RESULT_TYPE_EN],
        'pop': None,
        'electors': None,
        'ballots': district[PRELIM_ED_TOTAL_BALLOTS],
        'turnout': None,
        'ballots_valid': ballots_valid,
        'ballots_valid_per': None,
        'ballots_rej': district[PRELIM_ED_REJECTED_BALLOTS],
        'ballots_rej_per': ballots_rej_per,
        'electors_abstained': None,
        'electors_abstained_per': None,
        'electors_abstained_per_pop': None,
        'ineligible': None,
        'ineligible_per': None,
        'elected_candidate_given': None,
        'elected_candidate_last': None,
        'elected_candidate_party': None,
        'candidates': []
    }



def update_elected_candidate(districts: dict, highest: dict, party_id: dict):
    # TODO: Align prelim and f96 candidate first/middle/last name usage
    districts[highest[PRELIM_ED_NUM]]['elected_candidate_given'] = highest[PRELIM_CAN_FIRST]
    districts[highest[PRELIM_ED_NUM]]['elected_candidate_last'] = highest[PRELIM_CAN_LAST]
    districts[highest[PRELIM_ED_NUM]]['elected_candidate_party'] = party_id[highest[PRELIM_CAN_PARTY_EN]]

    name = highest[PRELIM_CAN_FIRST] + ' ' + highest[PRELIM_CAN_LAST]
    for candidate in districts[highest[PRELIM_ED_NUM]]['candidates']:
        if candidate['name'] == name and candidate['party'] == party_id[highest[PRELIM_CAN_PARTY_EN]]:
            candidate['elected'] = True

        


def parse_candidates(election: dict) -> dict:
    # Initialize variables
    districts = {} # All districts
    parties = set()
    last_result_type = None
    last_ed = None
    highest = None

    print(" - loading parties map data")
    with open(CA_PARTIES_MAP_JSON_FILENAME) as party_id_file:
        party_id = json.load(party_id_file)
        party_names = party_id.keys()

    # Process all lines. Skip 2 header lines, skip footnotes (at end).
    print(" - loading preliminary results")
    prelim_file = open(CA_GE_PRELIMINARY, encoding='utf8')

    table_reader = csv.reader(prelim_file, delimiter='\t')
    next(table_reader) # skip the headers
    next(table_reader)

    for candidate in table_reader:
        if candidate[0][0] == '*': continue # Skip if a footnote
        
        # Check if next district, or validated results for district
        # This will overwrite preliminary results, if present.
        if candidate[PRELIM_ED_RESULT_TYPE_EN] != last_result_type or candidate[PRELIM_ED_NUM] != last_ed:
            if highest: update_elected_candidate(districts, highest, party_id)
            districts[candidate[PRELIM_ED_NUM]] = district_init(candidate)
            highest = candidate
            last_result_type = candidate[PRELIM_ED_RESULT_TYPE_EN]
            last_ed = candidate[PRELIM_ED_NUM]
        else:
            if int(candidate[PRELIM_CAN_BALLOTS]) > int(highest[PRELIM_CAN_BALLOTS]):
                highest = candidate

        if candidate[PRELIM_CAN_MIDDLE]:
            name = candidate[PRELIM_CAN_FIRST] + ' ' + candidate[PRELIM_CAN_MIDDLE] + ' ' + candidate[PRELIM_CAN_LAST]
        else:
            name = candidate[PRELIM_CAN_FIRST] + ' ' + candidate[PRELIM_CAN_LAST]
        if candidate[PRELIM_CAN_PARTY_EN] in party_names:
            party = party_id[candidate[PRELIM_CAN_PARTY_EN]]
        else:
            parties.add(candidate[PRELIM_CAN_PARTY_EN])
            parties.add(candidate[PRELIM_CAN_PARTY_FR])
            party = None

        districts[candidate[PRELIM_ED_NUM]]['candidates'].append({
            'name': name,
            'party': party,
            'ballots': candidate[PRELIM_CAN_BALLOTS],
            'per_ballots': candidate[PRELIM_CAN_PERCENT_BALLOTS],
            'per_electors': None,
            'per_pop': None,
            'elected': False,
            'incumbent': False
        })
        
    prelim_file.close()
    print(" - parsed",len(districts),"districts")
    if len(parties) > 0: print(' - parties not found in party map:',parties)
    return districts



def parse_election(election: dict):
    print(" - parse preliminary results")
    districts = parse_candidates(election)
    # update_districts(districts)
    return districts
# parse_election(CA_GE_ELECTIONS['45'])