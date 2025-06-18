# Elections Canada results
#
# -----------------------------------------------------------------------------
#           Licensed under the Apache License, Version 2.0
# -----------------------------------------------------------------------------
#

from __init__ import *
import json
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod

class ElectionResults(ABC):
    """ Election Results
    """
    name:str
    districts : dict
    df_data:dict
    party_stats:dict
    election: dict

    @classmethod
    def __init__(self, election:dict):
        """
        Parse election data, aggregate data, calculate stats
        and write files.
        """
        self.districts = {}
        self.party_stats = { 'CA':{} }
        self.df_data = { 'ed': [], 'region': [], 'party': [], 'ballots': [], 'per_ballots': [], 'per_electors': [], 'per_pop': [] }
        self.election = election

        # Parse data files
        self.parse()

        # Aggregate and calculate statistics
        self.agg_party_data()
        self.calc_party_stats()
        
        # Write out processed data files
        self.write_files()
    
    @classmethod
    def agg_party_data(self) -> None:
        """ Aggregate party data for pd.DataFrame and to write out
        
        Parameters
        ----------
        districts : dict
            Dictionary of district data
        df_data : dict
        party_stats : dict
        """

        for d in self.districts.values():
            region = SGC_TO_ALPHA[d['num'][:2]]
            ed_num = d['num']

            for c in d['candidates']:
                party = c['party']

                if party not in self.party_stats['CA']:
                    self.party_stats['CA'][party] = {'elected': list()}
                self.party_stats['CA'][party]['elected'].append(ed_num)
                self.df_data['ed'].append(ed_num)
                self.df_data['region'].append(region)
                self.df_data['party'].append(party)
                self.df_data['ballots'].append(float(c['ballots']))
                self.df_data['per_ballots'].append(float(c['per_ballots']))
                if c['per_electors'] is not None:
                    self.df_data['per_electors'].append(float(c['per_electors']))
                else:
                    self.df_data['per_electors'].append(None)
                if c['per_pop'] is not None:
                    self.df_data['per_pop'].append(float(c['per_pop']))
                else:
                    self.df_data['per_pop'].append(None)

                if region not in self.party_stats:
                    self.party_stats[region] = {}
                if party not in self.party_stats[region]:
                    self.party_stats[region][party] = {'elected': list()}
                self.party_stats[region][party]['elected'].append(ed_num)

    @staticmethod
    def calc_agg_party_data(df:pd.DataFrame, grouping:list) -> pd.DataFrame:
        # Overridden in CaPrelim
        return df.groupby(grouping).agg(
            pb_min=('per_ballots','min'),
            pb_max=('per_ballots', 'max'),
            pb_mean=('per_ballots', 'mean'),
            pb_median=('per_ballots', 'median'),
            pb_25=('per_ballots', lambda x: ElectionResults.calc_percentile(x, 25)),
            pb_50=('per_ballots', lambda x: ElectionResults.calc_percentile(x, 50)),
            pb_75=('per_ballots', lambda x: ElectionResults.calc_percentile(x, 75)),

            pe_min=('per_electors','min'),
            pe_max=('per_electors', 'max'),
            pe_mean=('per_electors', 'mean'),
            pe_median=('per_electors', 'median'),
            pe_25=('per_electors', lambda x: ElectionResults.calc_percentile(x, 25)),
            pe_50=('per_electors', lambda x: ElectionResults.calc_percentile(x, 50)),
            pe_75=('per_electors', lambda x: ElectionResults.calc_percentile(x, 75)),

            pp_min=('per_pop','min'),
            pp_max=('per_pop', 'max'),
            pp_mean=('per_pop', 'mean'),
            pp_median=('per_pop', 'median'),
            pp_50=('per_pop', lambda x: ElectionResults.calc_percentile(x, 50)),
            pp_25=('per_pop', lambda x: ElectionResults.calc_percentile(x, 25)),
            pp_75=('per_pop', lambda x: ElectionResults.calc_percentile(x, 75)),
        )

    @classmethod
    def calc_party_stats(self) -> None:
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
        df = pd.DataFrame(self.df_data)

        agg_party = self.calc_agg_party_data(df=df, grouping=['party'])
        agg_region_party = self.calc_agg_party_data(df=df, grouping=['region', 'party'])
        for group,a in agg_party.iterrows():
            self.insert_agg_summary(r='CA', p=group, a=a)
        for group,a in agg_region_party.iterrows():
            self.insert_agg_summary(r=group[1], p=group[0], a=a)

    @staticmethod
    def calc_percentile(group:list, percentile:int) -> float:
        """ Calculate percentile, used for pandas agg
        """
        return np.percentile(group, percentile)

    @abstractmethod
    def parse(self) -> None:
        pass

    @classmethod
    def insert_agg_summary(self, r:str, p:str, a:list):
        # Overridden in CaPrelim

        if r not in self.party_stats: self.party_stats[r] = {}
        if p not in self.party_stats[r]: self.party_stats[r][p] = {}
        # TODO: Skip stuff not in preliminary
        self.party_stats[r][p]['pb_min']  = round(float(a['pb_min']), 1)
        self.party_stats[r][p]['pb_max']  = round(float(a['pb_max']), 1)
        self.party_stats[r][p]['pb_mean'] = round(float(a['pb_mean']), 1)
        self.party_stats[r][p]['pb_median']=round(float(a['pb_median']), 1)
        self.party_stats[r][p]['pb_25']   = round(float(a['pb_25']), 1)
        self.party_stats[r][p]['pb_50']   = round(float(a['pb_50']), 1)
        self.party_stats[r][p]['pb_75']   = round(float(a['pb_75']), 1)

        self.party_stats[r][p]['pe_min']  = round(float(a['pe_min']), 1)
        self.party_stats[r][p]['pe_max']  = round(float(a['pe_max']), 1)
        self.party_stats[r][p]['pe_mean'] = round(float(a['pe_mean']), 1)
        self.party_stats[r][p]['pe_median']=round(float(a['pe_median']), 1)
        self.party_stats[r][p]['pe_25']   = round(float(a['pe_25']), 1)
        self.party_stats[r][p]['pe_50']   = round(float(a['pe_50']), 1)
        self.party_stats[r][p]['pe_75']   = round(float(a['pe_75']), 1)

        self.party_stats[r][p]['pp_min']  = round(float(a['pp_min']), 1)
        self.party_stats[r][p]['pp_max']  = round(float(a['pp_max']), 1)
        self.party_stats[r][p]['pp_mean'] = round(float(a['pp_mean']), 1)
        self.party_stats[r][p]['pp_median']=round(float(a['pp_median']), 1)
        self.party_stats[r][p]['pp_50']   = round(float(a['pp_50']), 1)
        self.party_stats[r][p]['pp_25']   = round(float(a['pp_25']), 1)
        self.party_stats[r][p]['pp_75']   = round(float(a['pp_75']), 1)

    @classmethod
    def write_files(self):
        print(" - Writting files for GE", self.election['id'])
        election_json = open('data/ca_ge'+self.election['id']+'_districts.json', 'w')
        json.dump(self.districts, election_json, indent=2)
        election_json.close()

        party_json = open('data/ca_ge'+self.election['id']+'_parties.json', 'w')
        json.dump(self.party_stats, party_json, indent=2)
        party_json.close()
        

if __name__ == "__main__":
    print("ElectionResults is main")