# Elections Canada results
#
# -----------------------------------------------------------------------------
#           Licensed under the Apache License, Version 2.0
# -----------------------------------------------------------------------------
#

from ElectionResultsClass import *

with open(CA_PARTIES_MAP_SHORT_JSON_FILENAME) as f: party_map = json.load(f)

PRELIM_ED_NUM = 0  # Column 2 is electoral district number
PRELIM_ED_NAME_EN = 1 # Column 1 is electoral district name
PRELIM_ED_NAME_FR = 2
PRELIM_ED_RESULT_TYPE_EN = 3
PRELIM_ED_RESULT_TYPE_FR = 4
PRELIM_CAN_LAST = 5
PRELIM_CAN_MIDDLE = 6
PRELIM_CAN_FIRST = 7
PRELIM_CAN_PARTY_EN = 8
PRELIM_CAN_PARTY_FR = 9
PRELIM_CAN_BALLOTS = 10
PRELIM_CAN_PERCENT_BALLOTS = 11
PRELIM_ED_REJECTED_BALLOTS = 12
PRELIM_ED_TOTAL_BALLOTS = 13


class ElectionResultsCaPrelim(ElectionResults):
    
    @staticmethod
    def district_init(district: dict) -> dict:
        ballots_valid = int(district[PRELIM_ED_TOTAL_BALLOTS])-int(district[PRELIM_ED_REJECTED_BALLOTS])
        ballots_rej_per = round(int(district[PRELIM_ED_REJECTED_BALLOTS])/int(district[PRELIM_ED_TOTAL_BALLOTS]), 1)
        if SGC_TO_ALPHA[district[PRELIM_ED_NUM][:2]]=='QC':
            ed_name = district[PRELIM_ED_NAME_FR]
            if ed_name == "Côte-du-Sud-Rivière-du-Loup-Kataskomiq-Témiscouata":
                ed_name = "Côte-du-Sud–Rivière-du-Loup–Kataskomiq–Témiscouata"
                print(" - Corrected",district[PRELIM_ED_NUM],"to",ed_name)
                # TODO: confirm this is not a thing in official 45 results
                # TODO: remove if this is fixed in later elections
        else:
            ed_name = district[PRELIM_ED_NAME_EN]

        return {
            'num': district[PRELIM_ED_NUM],
            'name': ed_name,
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
            'elected_candidate_maj': None,
            'elected_candidate_maj_per': None,
            'candidates': []
        }

    @classmethod
    def finalize_district(self, first: dict, second: dict, party_id: dict):
        """
        Sets the district's elected candidate data, and set's the candidates
        elected field to true.
        """
        # TODO: Align prelim and f96 candidate first/middle/last name usage
        name = first[PRELIM_CAN_FIRST] + ' ' + first[PRELIM_CAN_LAST]
        maj = int(first[PRELIM_CAN_BALLOTS])-int(second[PRELIM_CAN_BALLOTS])
        maj_per = round(float(first[PRELIM_CAN_PERCENT_BALLOTS])-float(second[PRELIM_CAN_PERCENT_BALLOTS]), 1)

        self.districts[first[PRELIM_ED_NUM]]['elected_candidate_given'] = first[PRELIM_CAN_FIRST]
        self.districts[first[PRELIM_ED_NUM]]['elected_candidate_last'] = first[PRELIM_CAN_LAST]
        self.districts[first[PRELIM_ED_NUM]]['elected_candidate_party'] = party_id[first[PRELIM_CAN_PARTY_EN]]
        self.districts[first[PRELIM_ED_NUM]]['elected_candidate_maj'] = maj
        self.districts[first[PRELIM_ED_NUM]]['elected_candidate_maj_per'] = maj_per

        for candidate in self.districts[first[PRELIM_ED_NUM]]['candidates']:
            if candidate['name'] == name and candidate['party'] == party_id[first[PRELIM_CAN_PARTY_EN]]:
                candidate['elected'] = True

    @classmethod
    def parse(self) -> None:
        print("1")
        self.parse_candidates()
        print("2")
        print(json.dumps(self.districts, indent=2))
        print("3")

    @classmethod
    def parse_candidates(self) -> dict:
        # Initialize variables
        invalid_parties = set()
        last_result_type = None
        last_ed = None
        first = None
        second = None

        print(" - loading parties map data")
        with open(CA_PARTIES_MAP_JSON_FILENAME) as party_id_file:
            party_id = json.load(party_id_file)
            party_names = party_id.keys()

        # Process all lines. Skip 2 header lines, skip footnotes (at end).
        print(" - loading preliminary results")
        prelim_file = open(election['sources']['preliminary'], encoding='utf8')

        table_reader = csv.reader(prelim_file, delimiter='\t')
        next(table_reader) # skip the headers
        next(table_reader)

        for candidate in table_reader:
            if candidate[0][0] == '*': continue # Skip if a footnote
            
            # Check if next district, or validated results for district
            # This will overwrite preliminary results, if present.
            if candidate[PRELIM_ED_RESULT_TYPE_EN] != last_result_type or candidate[PRELIM_ED_NUM] != last_ed:
                if first: self.finalize_district(first=first, second=second,  party_id=party_id)
                self.districts[candidate[PRELIM_ED_NUM]] = self.district_init(candidate)
                first = candidate
                second = None
                last_result_type = candidate[PRELIM_ED_RESULT_TYPE_EN]
                last_ed = candidate[PRELIM_ED_NUM]
            else:
                if int(candidate[PRELIM_CAN_BALLOTS]) > int(first[PRELIM_CAN_BALLOTS]):
                    second = first
                    first = candidate
                elif not second or int(candidate[PRELIM_CAN_BALLOTS]) > int(second[PRELIM_CAN_BALLOTS]):
                    second = candidate

            if candidate[PRELIM_CAN_MIDDLE]:
                name = candidate[PRELIM_CAN_FIRST] + ' ' + candidate[PRELIM_CAN_MIDDLE] + ' ' + candidate[PRELIM_CAN_LAST]
            else:
                name = candidate[PRELIM_CAN_FIRST] + ' ' + candidate[PRELIM_CAN_LAST]
            if candidate[PRELIM_CAN_PARTY_EN] in party_names:
                party = party_id[candidate[PRELIM_CAN_PARTY_EN]]
            else:
                invalid_parties.add(candidate[PRELIM_CAN_PARTY_EN])
                invalid_parties.add(candidate[PRELIM_CAN_PARTY_FR])
                party = None

            self.districts[candidate[PRELIM_ED_NUM]]['candidates'].append({
                'name': name,
                'party': party,
                'ballots': candidate[PRELIM_CAN_BALLOTS],
                'per_ballots': candidate[PRELIM_CAN_PERCENT_BALLOTS],
                'per_electors': None,
                'per_pop': None,
                'elected': False,
                'incumbent': False
            })
        # Add winning candidate for the last district
        self.finalize_district(first=first, second=second, party_id=party_id)
        prelim_file.close()
        print(" - parsed",len(self.districts),"districts")
        if len(invalid_parties) > 0: print(' - parties not found in party map:',invalid_parties)


if __name__ == "__main__":
    for election in CA_GE_ELECTIONS.values():
        print('Processing election',election['id'],election['type'], '...')

        if election['format'] == 'preliminary':
            e = ElectionResultsCaPrelim(election)
        else:
            print(" - Skip",election['format'])