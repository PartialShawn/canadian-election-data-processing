# Functions that parse Format 96 tables
#
# -----------------------------------------------------------------------------
#           Licensed under the Apache License, Version 2.0
# -----------------------------------------------------------------------------
#

from __init__ import *
import csv, json
import pandas as pd
import numpy as np

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

def calculate_percentile(group:list, percentile:int) -> float:
    """ Calculate percentile, used for pandas agg
    """
    return np.percentile(group, percentile)

def calc_party_stats(districts: dict) -> dict:
    global party_map
    stats = { 'ca':{} }
    data = { 'ed': [], 'region': [], 'party': [], 'ballots': [], 'per_ballots': [], 'per_electors': [], 'per_pop': [] }
    # data = { 'ed': ['a','b'], 'region': ['ca','ca'], 'party': ['c','c'], 'ballots': [5,7], 'per_ballots': [10.1,14.2], 'per_electors': [11,12], 'per_pop': [8,9] }
    

    for d in districts.values():
        region = SGC_TO_ALPHA[d['num'][:2]]
        ed_num = d['num']

        for c in d['candidates']:
            party = c['party']

            if party not in stats['ca']:
                stats['ca'][party] = {'elected': list()}
                # data['ca'][party] = {'num':[], 'ballots':[], 'per_ballots':[], 'per_electors':[], 'per_pop':[]}

            stats['ca'][party]['elected'].append(ed_num)
            data['ed'].append(ed_num)
            data['region'].append(region)
            data['party'].append(party)
            data['ballots'].append(c['ballots'])
            data['per_ballots'].append(c['per_ballots'])
            data['per_electors'].append(c['per_electors'])
            data['per_pop'].append(c['per_pop'])

            if region not in stats:
                stats[region] = {}
                # data[region] = {}
            if party not in stats[region]:
                stats[region][party] = {'elected': list()}
                # data[region][party] = {'num':[], 'ballots':[], 'per_ballots':[], 'per_electors':[], 'per_pop':[]}
            
            stats[region][party]['elected'].append(ed_num)
    


    
    # ----------------------------------------------
    #                PANDAS IT UP
    # ----------------------------------------------


    df = pd.DataFrame(data)

    agg_party = df.groupby(['party']).agg(
        pb_min=('per_ballots','min'),
        pb_max=('per_ballots', 'max'),
        pb_mean=('per_ballots', 'mean'),
        pb_median=('per_ballots', 'median'),
        pb_25=('per_ballots', lambda x: calculate_percentile(x, 25)),
        pb_50=('per_ballots', lambda x: calculate_percentile(x, 50)),
        pb_75=('per_ballots', lambda x: calculate_percentile(x, 75)),

        pe_min=('per_electors','min'),
        pe_max=('per_electors', 'max'),
        pe_mean=('per_electors', 'mean'),
        pe_median=('per_electors', 'median'),
        pe_25=('per_electors', lambda x: calculate_percentile(x, 25)),
        pe_50=('per_electors', lambda x: calculate_percentile(x, 50)),
        pe_75=('per_electors', lambda x: calculate_percentile(x, 75)),

        pp_min=('per_pop','min'),
        pp_max=('per_pop', 'max'),
        pp_mean=('per_pop', 'mean'),
        pp_median=('per_pop', 'median'),
        pp_50=('per_pop', lambda x: calculate_percentile(x, 50)),
        pp_25=('per_pop', lambda x: calculate_percentile(x, 25)),
        pp_75=('per_pop', lambda x: calculate_percentile(x, 75)),
    )


    agg_region_party = df.groupby(['region','party']).agg(
        pb_min=('per_ballots','min'),
        pb_max=('per_ballots', 'max'),
        pb_mean=('per_ballots', 'mean'),
        pb_median=('per_ballots', 'median'),
        pb_25=('per_ballots', lambda x: calculate_percentile(x, 25)),
        pb_50=('per_ballots', lambda x: calculate_percentile(x, 50)),
        pb_75=('per_ballots', lambda x: calculate_percentile(x, 75)),

        pe_min=('per_electors','min'),
        pe_max=('per_electors', 'max'),
        pe_mean=('per_electors', 'mean'),
        pe_median=('per_electors', 'median'),
        pe_25=('per_electors', lambda x: calculate_percentile(x, 25)),
        pe_50=('per_electors', lambda x: calculate_percentile(x, 50)),
        pe_75=('per_electors', lambda x: calculate_percentile(x, 75)),

        pp_min=('per_pop','min'),
        pp_max=('per_pop', 'max'),
        pp_mean=('per_pop', 'mean'),
        pp_median=('per_pop', 'median'),
        pp_50=('per_pop', lambda x: calculate_percentile(x, 50)),
        pp_25=('per_pop', lambda x: calculate_percentile(x, 25)),
        pp_75=('per_pop', lambda x: calculate_percentile(x, 75)),
    )

    for group,a in agg_party.iterrows():
        stats['ca'][group]['pb_min']  = round(float(a['pb_min']), 1)
        stats['ca'][group]['pb_max']  = round(float(a['pb_max']), 1)
        stats['ca'][group]['pb_mean'] = round(float(a['pb_mean']), 1)
        stats['ca'][group]['pb_median']=round(float(a['pb_median']), 1)
        stats['ca'][group]['pb_25']   = round(float(a['pb_25']), 1)
        stats['ca'][group]['pb_50']   = round(float(a['pb_50']), 1)
        stats['ca'][group]['pb_75']   = round(float(a['pb_75']), 1)

        stats['ca'][group]['pe_min']  = round(float(a['pe_min']), 1)
        stats['ca'][group]['pe_max']  = round(float(a['pe_max']), 1)
        stats['ca'][group]['pe_mean'] = round(float(a['pe_mean']), 1)
        stats['ca'][group]['pe_median']=round(float(a['pe_median']), 1)
        stats['ca'][group]['pe_25']   = round(float(a['pe_25']), 1)
        stats['ca'][group]['pe_50']   = round(float(a['pe_50']), 1)
        stats['ca'][group]['pe_75']   = round(float(a['pe_75']), 1)

        stats['ca'][group]['pp_min']  = round(float(a['pp_min']), 1)
        stats['ca'][group]['pp_max']  = round(float(a['pp_max']), 1)
        stats['ca'][group]['pp_mean'] = round(float(a['pp_mean']), 1)
        stats['ca'][group]['pp_median']=round(float(a['pp_median']), 1)
        stats['ca'][group]['pp_50']   = round(float(a['pp_50']), 1)
        stats['ca'][group]['pp_25']   = round(float(a['pp_25']), 1)
        stats['ca'][group]['pp_75']   = round(float(a['pp_75']), 1)

    for group,a in agg_region_party.iterrows():
        stats[group[0]][group[1]]['pb_min']  = round(float(a['pb_min']), 1)
        stats[group[0]][group[1]]['pb_max']  = round(float(a['pb_max']), 1)
        stats[group[0]][group[1]]['pb_mean'] = round(float(a['pb_mean']), 1)
        stats[group[0]][group[1]]['pb_median']=round(float(a['pb_median']), 1)
        stats[group[0]][group[1]]['pb_25']   = round(float(a['pb_25']), 1)
        stats[group[0]][group[1]]['pb_50']   = round(float(a['pb_50']), 1)
        stats[group[0]][group[1]]['pb_75']   = round(float(a['pb_75']), 1)

        stats[group[0]][group[1]]['pe_min']  = round(float(a['pe_min']), 1)
        stats[group[0]][group[1]]['pe_max']  = round(float(a['pe_max']), 1)
        stats[group[0]][group[1]]['pe_mean'] = round(float(a['pe_mean']), 1)
        stats[group[0]][group[1]]['pe_median']=round(float(a['pe_median']), 1)
        stats[group[0]][group[1]]['pe_25']   = round(float(a['pe_25']), 1)
        stats[group[0]][group[1]]['pe_50']   = round(float(a['pe_50']), 1)
        stats[group[0]][group[1]]['pe_75']   = round(float(a['pe_75']), 1)

        stats[group[0]][group[1]]['pp_min']  = round(float(a['pp_min']), 1)
        stats[group[0]][group[1]]['pp_max']  = round(float(a['pp_max']), 1)
        stats[group[0]][group[1]]['pp_mean'] = round(float(a['pp_mean']), 1)
        stats[group[0]][group[1]]['pp_median']=round(float(a['pp_median']), 1)
        stats[group[0]][group[1]]['pp_50']   = round(float(a['pp_50']), 1)
        stats[group[0]][group[1]]['pp_25']   = round(float(a['pp_25']), 1)
        stats[group[0]][group[1]]['pp_75']   = round(float(a['pp_75']), 1)

    return stats



def parse_candidates(election: dict, districts: dict) -> None:
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
                districts[candidate[T12_ED_NUM]]['elected_candidate_maj'] = candidate[T12_CAND_MAJ]
                districts[candidate[T12_ED_NUM]]['elected_candidate_maj_per'] = candidate[T12_CAND_MAJ_PER]
                elected = True
            else:
                elected = False
        except IndexError:
            elected = False
            print(' - Error: missing majority info (blank values missing ending commas?)')

        districts[candidate[T12_ED_NUM]]['candidates'].append({
            'name': cand_name,
            'party': cand_party,
            'ballots': int(candidate[T12_CAND_VOTES]),
            'per_ballots': float(candidate[T12_CAND_PER]),
            'per_electors': round(int(candidate[T12_CAND_VOTES])/int(districts[candidate[T12_ED_NUM]]['electors'])*100, 2),
            'per_pop': round(int(candidate[T12_CAND_VOTES])/int(districts[candidate[T12_ED_NUM]]['pop'])*100, 2),
            'elected': elected,
            'incumbent': incumbent
        })
    
    file.close()



def parse_district_result(election: dict) -> dict:
    """ Parse table 11 to get district data, creates dict.
    Also creates an empty candidates field for each district.
    
    Parameters
    ----------
    election : dict
        A value() from CA_GE_ELECTIONS

    Returns
    -------
    distrcits : dict
        A newly created dict of districts.
    stats : dict
        A newly created dict for regions of elected reps by party
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
        if '/' in district[T11_ED_NAME]:
            if SGC_TO_ALPHA[district[T11_ED_NUM][:2]]=='QC':
                ed_name = district[T11_ED_NAME].split('/')[1]
            else:
                ed_name = district[T11_ED_NAME].split('/')[0]
        else:
            ed_name = district[T11_ED_NAME]
        # TODO: Align prelim and f96 candidate first/middle/last name usage
        districts[district[T11_ED_NUM]] = {
            'num': district[T11_ED_NUM],
            'name': ed_name,
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
            'elected_candidate_maj': None,
            'elected_candidate_maj_per': None,
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
    stats = calc_party_stats(districts)

    return districts, stats



def debug():
    print()
    print("Debug")
    print()
    for election in CA_GE_ELECTIONS.values():
        print('Processing election',election['id'])
        if election['format'] == 'f96':
            districts, stats = parse_election(election)

            election_json = open(election['data']['districts'], 'w')
            json.dump(districts, election_json, indent=2)
            election_json.close()

            election_json = open(election['data']['parties'], 'w')
            json.dump(stats, election_json, indent=2)
            election_json.close()
debug()