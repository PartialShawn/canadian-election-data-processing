# Functions that parse Format 96 tables
#
# -----------------------------------------------------------------------------
#           Licensed under the Apache License, Version 2.0
# -----------------------------------------------------------------------------
#

from __init__ import *
import csv, json

# Table CSV file Columns

T11_ED_PROV = 0
T11_ED_NAME = 1
T11_ED_NUM = 2
T11_ED_POP = 3
T11_ED_ELECTORS_TOTAL = 4
T11_ED_POLL_STATIONS_TOTAL = 5
T11_ED_BALLOTS_VALID = 6
T11_ED_BALLOTS_VALID_PER = 7
T11_ED_BALLOTS_REJ = 8
T11_ED_BALLOTS_REJ_PER = 9
T11_ED_BALLOTS_TOTAL = 10
T11_ED_TURNOUT_PER = 11
T11_ED_ELECTED_CANDIDATE = 12

T12_ED_PROV = 0
T12_ED_NAME = 1
T12_ED_NUM = 2
T12_CAND_NAME = 3
T12_CAND_RES = 4
T12_CAND_OCCUPATION = 5
T12_CAND_VOTES = 6
T12_CAND_PER = 7
T12_CAND_MAJ = 8
T12_CAND_MAJ_PER = 9

with open(CA_PARTIES_MAP_SHORT_JSON_FILENAME) as f: party_map = json.load(f)

def parse_candidates(election: dict, districts: dict):
    """ Parse table 12 to add candidate results to district data.
        
    Parameters
    ----------
    election : dict
        A value() from CA_GE_ELECTIONS.
    districts : dict
        A dict of all districts.
    """

    global party_map
    file = open(election['sources']['table12'], encoding=election['encoding'])
    election = csv.reader(file)
    next(election) # skip headers
    count = 0
    parties = set()

    for candidate in election:

        if not candidate:
            print(' - Skip blank line')
            continue # skip blank lines
        
        # Parse candidate/party name
        if '**' in candidate[T12_CAND_NAME]:
            incumbent = True
            name_party = candidate[T12_CAND_NAME].split('**')
            cand_name = name_party[0].strip()
            if name_party[1].strip() in party_map:
                cand_party = party_map[name_party[1].strip()]
            else:
                print(" - couldn't find party:", candidate[T12_CAND_NAME])
                
        else:
            incumbent = False
            cand_party = None
            for party,id in party_map.items():
                if party in candidate[T12_CAND_NAME]:
                    cand_party = id
                    cand_name = candidate[T12_CAND_NAME][:-len(party)-1]
            if not cand_party:
                print(" - couldn't find party:", candidate[T12_CAND_NAME])
                cand_name = candidate[T12_CAND_NAME]
                cand_party = candidate[T12_CAND_NAME]

        # parse elected candidate data
        try:
            if candidate[T12_CAND_MAJ]:
                districts[candidate[T12_ED_NUM]]['majority'] = candidate[T12_CAND_MAJ]
                districts[candidate[T12_ED_NUM]]['majority_per'] = candidate[T12_CAND_MAJ_PER]
                elected = True
            else:
                elected = False
        except IndexError:
            elected = False
            print(' - Error: missing majority info (blank values missing ending commas?)')

        districts[candidate[T12_ED_NUM]]['candidates'].append({
            'name': cand_name,
            'party': cand_party,
            'ballots': candidate[T12_CAND_VOTES],
            'per_ballots': candidate[T12_CAND_PER],
            'per_electors': round(int(candidate[T12_CAND_VOTES])/int(districts[candidate[T12_ED_NUM]]['electors'])*100, 2),
            'per_pop': round(int(candidate[T12_CAND_VOTES])/int(districts[candidate[T12_ED_NUM]]['pop'])*100, 2),
            'elected': elected,
            'incumbent': incumbent
        })
    
    file.close()



def parse_district_result(election: dict) -> dict:
    """ Parse table 11 to get district data, creates dict.
    Also creates an empty candidates entry for each district.
    
    Parameters
    ----------
    election : dict
        A value() from CA_GE_ELECTIONS

    Returns
    -------
    dict
        A newly created dict of districts.
    """

    global party_map
    districts = {}
    file = open(election['sources']['table11'], encoding=election['encoding'])
    reader_table = csv.reader(file)
    next(reader_table) # skip headers

    for district in reader_table:

        if not district:
            print(' - Skip blank lines')
            continue # skip blank lines
        
        # Parse candidate and party names
        cand_party = None
        cand_name = None
        for party,id in party_map.items():
            if party in district[T11_ED_ELECTED_CANDIDATE]:
                cand_party = id
                cand_name = district[T11_ED_ELECTED_CANDIDATE][:-len(party)-1].split(',')
                cand_name_last = cand_name[0]
                cand_name_given = cand_name[1].strip()
                break
        if not cand_party:
            print(" - couldn't find party:", district[T11_ED_ELECTED_CANDIDATE])
            cand_name_last = district[T11_ED_ELECTED_CANDIDATE]
            cand_name_given = ''
            cand_party = district[T11_ED_ELECTED_CANDIDATE]

        districts[district[T11_ED_NUM]] = {
            'num': district[T11_ED_NUM],
            'status': 'official',
            'pop': district[T11_ED_POP],
            'electors': district[T11_ED_ELECTORS_TOTAL],
            'ballots': district[T11_ED_BALLOTS_TOTAL],
            'turnout': district[T11_ED_TURNOUT_PER],
            'ballots_valid': district[T11_ED_BALLOTS_VALID],
            'ballots_valid_per': district[T11_ED_BALLOTS_VALID_PER],
            'ballots_rej': district[T11_ED_BALLOTS_REJ],
            'ballots_rej_per': district[T11_ED_BALLOTS_REJ_PER],
            'electors_abstained': int(district[T11_ED_ELECTORS_TOTAL]) - int(district[T11_ED_BALLOTS_TOTAL]),
            'electors_abstained_per': round((int(district[T11_ED_ELECTORS_TOTAL]) - int(district[T11_ED_BALLOTS_TOTAL]))/int(district[T11_ED_ELECTORS_TOTAL]) * 100, 1),
            'electors_abstained_per_pop': round((int(district[T11_ED_ELECTORS_TOTAL]) - int(district[T11_ED_BALLOTS_TOTAL]))/int(district[T11_ED_POP]) * 100, 1),
            'ineligible': int(district[T11_ED_POP]) - int(district[T11_ED_ELECTORS_TOTAL]),
            'ineligible_per': round((int(district[T11_ED_POP]) - int(district[T11_ED_ELECTORS_TOTAL])) / int(district[T11_ED_POP]) * 100, 1),
            'elected_candidate_given': cand_name_given,
            'elected_candidate_last': cand_name_last,
            'elected_candidate_party': cand_party,
            'candidates': []
        }
    
    file.close()
    return districts



def parse_election(election: dict):
    print(" - parse official results")
    districts = parse_district_result(election)
    print(' - processed',len(districts),'districts')
    parse_candidates(election, districts)
    print(' - processed candidates')

    return districts



def debug():
    print()
    print("Debug")
    print()
    for election in CA_GE_ELECTIONS.values():
        print('Processing election',election['id'])
        if election['format'] == 'f96': parse_election(election)    
debug()