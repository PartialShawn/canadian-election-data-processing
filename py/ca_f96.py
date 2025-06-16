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


def agg_party_data(districts : dict, df_data:dict, party_stats:dict) -> None:
    """ Aggregate party data for pd.DataFrame and to write out
    
    Parameters
    ----------
    districts : dict
        Dictionary of district data
    df_data : dict
    party_stats : dict
    """

    for d in districts.values():
        region = SGC_TO_ALPHA[d['num'][:2]]
        ed_num = d['num']

        for c in d['candidates']:
            party = c['party']

            if party not in party_stats['CA']:
                party_stats['CA'][party] = {'elected': list()}
            party_stats['CA'][party]['elected'].append(ed_num)
            df_data['ed'].append(ed_num)
            df_data['region'].append(region)
            df_data['party'].append(party)
            df_data['ballots'].append(c['ballots'])
            df_data['per_ballots'].append(c['per_ballots'])
            df_data['per_electors'].append(c['per_electors'])
            df_data['per_pop'].append(c['per_pop'])

            if region not in party_stats:
                party_stats[region] = {}
            if party not in party_stats[region]:
                party_stats[region][party] = {'elected': list()}
            party_stats[region][party]['elected'].append(ed_num)



def calc_agg_party_data(df:pd.DataFrame, grouping:list) -> pd.DataFrame:
    return df.groupby(grouping).agg(
        pb_min=('per_ballots','min'),
        pb_max=('per_ballots', 'max'),
        pb_mean=('per_ballots', 'mean'),
        pb_median=('per_ballots', 'median'),
        pb_25=('per_ballots', lambda x: calc_percentile(x, 25)),
        pb_50=('per_ballots', lambda x: calc_percentile(x, 50)),
        pb_75=('per_ballots', lambda x: calc_percentile(x, 75)),

        pe_min=('per_electors','min'),
        pe_max=('per_electors', 'max'),
        pe_mean=('per_electors', 'mean'),
        pe_median=('per_electors', 'median'),
        pe_25=('per_electors', lambda x: calc_percentile(x, 25)),
        pe_50=('per_electors', lambda x: calc_percentile(x, 50)),
        pe_75=('per_electors', lambda x: calc_percentile(x, 75)),

        pp_min=('per_pop','min'),
        pp_max=('per_pop', 'max'),
        pp_mean=('per_pop', 'mean'),
        pp_median=('per_pop', 'median'),
        pp_50=('per_pop', lambda x: calc_percentile(x, 50)),
        pp_25=('per_pop', lambda x: calc_percentile(x, 25)),
        pp_75=('per_pop', lambda x: calc_percentile(x, 75)),
    )



def calc_percentile(group:list, percentile:int) -> float:
    """ Calculate percentile, used for pandas agg
    """
    return np.percentile(group, percentile)



def calc_party_stats(df_data: dict, party_stats: dict) -> None:
    """ Calculate party stats using pandas.

    Parameters
    ----------
    df_data : dict
        Data formatted for pd.DataFrame
    
    Returns
    _______
    party_data : dict
        Party stats for writing out
        
    """
    df = pd.DataFrame(df_data)

    agg_party = calc_agg_party_data(df=df, grouping=['party'])
    agg_region_party = calc_agg_party_data(df=df, grouping=['region', 'party'])
    for group,a in agg_party.iterrows():
        insert_agg_summary(r='CA', p=group, a=a, data=party_stats)
    for group,a in agg_region_party.iterrows():
        insert_agg_summary(r=group[1], p=group[0], a=a, data=party_stats)



def finalize_data(districts: dict) -> dict:
    """ Finalized the district info

    For each district:
    - Sort candidates by votes (highest first)
    - Save statistics information for pd.dataframe

    Parameters
    ----------
    districts : dict
        A dict of all districts
    data : dict
        Stats formatted for pd.dataframe
    
    Return
    ------
    stats : dict
        Stats to be saved out as a data file
    """
    party_stats = { 'CA':{} }
    df_data = { 'ed': [], 'region': [], 'party': [], 'ballots': [], 'per_ballots': [], 'per_electors': [], 'per_pop': [] }

    agg_party_data(districts=districts, party_stats=party_stats, df_data=df_data)
    calc_party_stats(df_data=df_data, party_stats=party_stats)

    return party_stats



def insert_agg_summary(r:str, p:str, a:list, data:dict):
    if r not in data: data[r] = {}
    if p not in data[r]: data[r][p] = {}
    
    data[r][p]['pb_min']  = round(float(a['pb_min']), 1)
    data[r][p]['pb_max']  = round(float(a['pb_max']), 1)
    data[r][p]['pb_mean'] = round(float(a['pb_mean']), 1)
    data[r][p]['pb_median']=round(float(a['pb_median']), 1)
    data[r][p]['pb_25']   = round(float(a['pb_25']), 1)
    data[r][p]['pb_50']   = round(float(a['pb_50']), 1)
    data[r][p]['pb_75']   = round(float(a['pb_75']), 1)

    data[r][p]['pe_min']  = round(float(a['pe_min']), 1)
    data[r][p]['pe_max']  = round(float(a['pe_max']), 1)
    data[r][p]['pe_mean'] = round(float(a['pe_mean']), 1)
    data[r][p]['pe_median']=round(float(a['pe_median']), 1)
    data[r][p]['pe_25']   = round(float(a['pe_25']), 1)
    data[r][p]['pe_50']   = round(float(a['pe_50']), 1)
    data[r][p]['pe_75']   = round(float(a['pe_75']), 1)

    data[r][p]['pp_min']  = round(float(a['pp_min']), 1)
    data[r][p]['pp_max']  = round(float(a['pp_max']), 1)
    data[r][p]['pp_mean'] = round(float(a['pp_mean']), 1)
    data[r][p]['pp_median']=round(float(a['pp_median']), 1)
    data[r][p]['pp_50']   = round(float(a['pp_50']), 1)
    data[r][p]['pp_25']   = round(float(a['pp_25']), 1)
    data[r][p]['pp_75']   = round(float(a['pp_75']), 1)



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



def parse_election(election: dict) -> tuple[dict, dict]:
    """ Parses an election.

    Parameters
    ----------
    election : dict
        Election info from __init__.CA_GE_ELECTIONS

    Returns
    -------
    districts : dict
        Dictionary of district data
    party_stats : dict
        Dictionary of party statistics

    """
    print(" - parse official results")
    districts = parse_district_result(election)
    print(' - processed',len(districts),'districts')
    parse_candidates(election, districts)
    print(' - processed candidates')
    party_stats = finalize_data(districts)

    return districts, party_stats



def debug():
    print()
    print("Debug")
    print()
    for election in CA_GE_ELECTIONS.values():
        print('Processing election',election['id'])
        if election['format'] == 'f96':
            districts, party_stats = parse_election(election)

            election_json = open(election['data']['districts'], 'w')
            json.dump(districts, election_json, indent=2)
            election_json.close()

            election_json = open(election['data']['parties'], 'w')
            json.dump(party_stats, election_json, indent=2)
            election_json.close()
# debug()