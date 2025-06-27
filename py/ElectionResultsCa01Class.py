# Elections Canada results
#
# -----------------------------------------------------------------------------
#           Licensed under the Apache License, Version 2.0
# -----------------------------------------------------------------------------
#

from ElectionResultsClass import *
import csv

DATE_COL = 0
TYPE_COL = 1
PARL_COL = 2
PROV_COL = 3
RIDING_COL = 4
CAN_LAST_COL = 5
CAN_FIRST_COL = 6
CAN_GENDER_COL = 7
CAN_OCCUPATION_COL = 8
CAN_PARTY_COL = 9
CAN_BALLOTS_COL = 10
CAN_BALLOTS_PER_COL = 11
CAN_ELECTED_COL = 12


class ElectionResultsCa01(ElectionResults):

    elections:dict = {}

    @classmethod
    def agg_party_data(self):
        return
    
    @staticmethod
    def calc_agg_party_data(df:pd.DataFrame, grouping:list) -> pd.DataFrame:
        return df.groupby(grouping).agg(
            pb_min=('per_ballots','min'),
            pb_max=('per_ballots', 'max'),
            pb_mean=('per_ballots', 'mean'),
            pb_median=('per_ballots', 'median'),
            pb_25=('per_ballots', lambda x: ElectionResults.calc_percentile(x, 25)),
            pb_50=('per_ballots', lambda x: ElectionResults.calc_percentile(x, 50)),
            pb_75=('per_ballots', lambda x: ElectionResults.calc_percentile(x, 75))

            # pe_min=('per_electors','min'),
            # pe_max=('per_electors', 'max'),
            # pe_mean=('per_electors', 'mean'),
            # pe_median=('per_electors', 'median'),
            # pe_25=('per_electors', lambda x: ElectionResults.calc_percentile(x, 25)),
            # pe_50=('per_electors', lambda x: ElectionResults.calc_percentile(x, 50)),
            # pe_75=('per_electors', lambda x: ElectionResults.calc_percentile(x, 75)),

            # pp_min=('per_pop','min'),
            # pp_max=('per_pop', 'max'),
            # pp_mean=('per_pop', 'mean'),
            # pp_median=('per_pop', 'median'),
            # pp_50=('per_pop', lambda x: ElectionResults.calc_percentile(x, 50)),
            # pp_25=('per_pop', lambda x: ElectionResults.calc_percentile(x, 25)),
            # pp_75=('per_pop', lambda x: ElectionResults.calc_percentile(x, 75)),
        )
    
    @staticmethod
    def district_init(district: dict) -> dict:
        # ballots_valid = int(district[PRELIM_ED_TOTAL_BALLOTS])-int(district[PRELIM_ED_REJECTED_BALLOTS])
        # ballots_rej_per = round(int(district[PRELIM_ED_REJECTED_BALLOTS])/int(district[PRELIM_ED_TOTAL_BALLOTS]), 1)
        # if SGC_TO_ALPHA[district[PRELIM_ED_NUM][:2]]=='QC':
        #     ed_name = district[PRELIM_ED_NAME_FR]
        #     if ed_name == "Côte-du-Sud-Rivière-du-Loup-Kataskomiq-Témiscouata":
        #         ed_name = "Côte-du-Sud–Rivière-du-Loup–Kataskomiq–Témiscouata"
        #         print(" - Corrected",district[PRELIM_ED_NUM],"to",ed_name)
                # TODO: confirm this is not a thing in official 45 results
                # TODO: remove if this is fixed in later elections
        # else:
        #     ed_name = district[PRELIM_ED_NAME_EN]

        return {
            'num': None,
            'name': district[RIDING_COL],
            'status': 'Official',
            'pop': None,
            'electors': None,
            'ballots': None,
            'turnout': None,
            'ballots_valid': None,
            'ballots_valid_per': None,
            'ballots_rej': None,
            'ballots_rej_per': None,
            'electors_abstained': None,
            'electors_abstained_per': None,
            'electors_abstained_per_pop': None,
            'ineligible': None,
            'ineligible_per': None,
            'elected_candidate_given': None,
            'elected_candidate_last': None,
            'elected_candidate_party': None,
            'elected_candidate_party_en': None,
            'elected_candidate_party_fr': None,
            'elected_candidate_maj': None,
            'elected_candidate_maj_per': None,
            'candidates': []
        }

    @classmethod
    def finalize_district(self, first: dict, second: dict):
        """
        Sets the district's elected candidate data, and set's the candidates
        elected field to true.
        """
        # TODO: Align prelim and f96 candidate first/middle/last name usage
        name = first[CAN_FIRST_COL] + ' ' + first[CAN_LAST_COL]
        if second and first[CAN_BALLOTS_COL] != "" and second[CAN_BALLOTS_COL] != '':
            maj = int(first[CAN_BALLOTS_COL]) - int(second[CAN_BALLOTS_COL])
        if second and first[CAN_BALLOTS_PER_COL] != "" and second[CAN_BALLOTS_PER_COL] != '':
            maj_per = round(float(first[CAN_BALLOTS_PER_COL]) - float(second[CAN_BALLOTS_PER_COL]), 1)
        else:
            maj = None
            maj_per = None
        self.districts[first[RIDING_COL]]['elected_candidate_given'] = first[CAN_FIRST_COL]
        self.districts[first[RIDING_COL]]['elected_candidate_last'] = first[CAN_LAST_COL]
        self.districts[first[RIDING_COL]]['elected_candidate_party_en'] = first[CAN_PARTY_COL]

        self.districts[first[RIDING_COL]]['elected_candidate_maj'] = maj
        self.districts[first[RIDING_COL]]['elected_candidate_maj_per'] = maj_per


    @classmethod
    def insert_agg_summary(self, r:str, p:str, a:list):
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

        # self.party_stats[r][p]['pe_min']  = round(float(a['pe_min']), 1)
        # self.party_stats[r][p]['pe_max']  = round(float(a['pe_max']), 1)
        # self.party_stats[r][p]['pe_mean'] = round(float(a['pe_mean']), 1)
        # self.party_stats[r][p]['pe_median']=round(float(a['pe_median']), 1)
        # self.party_stats[r][p]['pe_25']   = round(float(a['pe_25']), 1)
        # self.party_stats[r][p]['pe_50']   = round(float(a['pe_50']), 1)
        # self.party_stats[r][p]['pe_75']   = round(float(a['pe_75']), 1)

        # self.party_stats[r][p]['pp_min']  = round(float(a['pp_min']), 1)
        # self.party_stats[r][p]['pp_max']  = round(float(a['pp_max']), 1)
        # self.party_stats[r][p]['pp_mean'] = round(float(a['pp_mean']), 1)
        # self.party_stats[r][p]['pp_median']=round(float(a['pp_median']), 1)
        # self.party_stats[r][p]['pp_50']   = round(float(a['pp_50']), 1)
        # self.party_stats[r][p]['pp_25']   = round(float(a['pp_25']), 1)
        # self.party_stats[r][p]['pp_75']   = round(float(a['pp_75']), 1)

    @classmethod
    def parse(self) -> None:
        self.parse_candidates()

    @classmethod
    def parse_candidates(self) -> dict:
        # Initialize variables
        invalid_parties = set()
        last_ed = None
        first = None
        second = None

        # Process all lines. Skip 2 header lines, skip footnotes (at end).
        print(" - loading Ca01 results")
        candidates_file = open(self.election['sources']['candidates'], encoding=self.election['encoding'])

        table_reader = csv.reader(candidates_file)
        next(table_reader) # skip the headers

        for candidate in table_reader:
            # if candidate[0][0] == '*': continue # Skip if a footnote
            # Check if next district, or validated results for district
            # This will overwrite preliminary results, if present.
            if candidate[RIDING_COL] != last_ed:
                if first: self.finalize_district(first=first, second=second)
                self.districts[candidate[RIDING_COL]] = self.district_init(candidate)
                first = candidate
                second = None
                last_ed = candidate[RIDING_COL]
            
            elif candidate[CAN_BALLOTS_COL] != '' and candidate[CAN_BALLOTS_COL] != 'accl.' and candidate[CAN_BALLOTS_COL] != 'NULL':

                if int(candidate[CAN_BALLOTS_COL]) > int(first[CAN_BALLOTS_COL]):
                    second = first
                    first = candidate
                elif not second or int(candidate[CAN_BALLOTS_COL]) > int(second[CAN_BALLOTS_COL]):
                    second = candidate
            elif candidate[CAN_BALLOTS_COL] == 'accl.':
                first = candidate
                second = None

            name = candidate[CAN_FIRST_COL] + ' ' + candidate[CAN_LAST_COL]
            
            self.districts[candidate[RIDING_COL]]['candidates'].append({
                'name': name,
                'party': None,
                'party_en': candidate[CAN_PARTY_COL],
                'ballots': candidate[CAN_BALLOTS_COL],
                'per_ballots': candidate[CAN_BALLOTS_PER_COL],
                'per_electors': None,
                'per_pop': None,
                'elected': False,
                'incumbent': False
            })
            self.elections[candidate[PARL_COL]][candidate[RIDING_COL]]['candidates'] = self.districts[candidate[RIDING_COL]]['candidates']
        # Add winning candidate for the last district
        self.finalize_district(first=first, second=second)
        candidates_file.close()
        print(" - parsed",len(self.districts),"districts")

    @classmethod
    def write_files(self):
        for e_num,data in self.elections:
            print(" - Writing:", e_num)
            super().write_files(e_num, data, party_stats={})

if __name__ == "__main__":
    for election in CA_GE_ELECTIONS.values():
        print('Processing election',election['id'],election['type'], '...')

        if election['format'] == 'Ca01':
            e = ElectionResultsCa01(election)