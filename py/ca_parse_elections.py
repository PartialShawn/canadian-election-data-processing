# Process all election data.
#
# -----------------------------------------------------------------------------
#           Licensed under the Apache License, Version 2.0
# -----------------------------------------------------------------------------
#

from __init__ import *
import json
import ca_f96, ca_prelim

def parse_all_elections():

    print()
    for election in CA_GE_ELECTIONS.values():
        print('Processing election',election['id'],election['type'], '...')

        if election['format'] == 'preliminary':
            districts = ca_prelim.parse_election(election)
        elif election['format'] == 'f96':
            districts, party_stats = ca_f96.parse_election(election)
        else:
            print(" - ERROR: invalid type")
            districts = None

        print(" - writing districts JSON file")
        election_json = open(election['data']['districts'], 'w')
        json.dump(districts, election_json, indent=2)
        election_json.close()

    
parse_all_elections()