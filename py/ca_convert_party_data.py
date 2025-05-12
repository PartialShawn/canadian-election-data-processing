# Convert `parties.csv` and `parties_map.csv` to JSON lookup files.
#
# -----------------------------------------------------------------------------
#           Licensed under the Apache License, Version 2.0
# -----------------------------------------------------------------------------

from __init__ import *
import csv, json

# Part 1: Open the parties CSV and create a dictionary of all party data
# with the party ID as key, and save out as JSON.


# parties.csv columns
PARTIES_ID = 0
PARTIES_SHORT_EN = 1
PARTIES_SHORT_FR = 2
PARTIES_COMMON_EN = 3
PARTIES_COMMON_FR = 4
PARTIES_LONG_EN = 5
PARTIES_LONG_FR = 6
PARTIES_REGISTERED = 7
PARTIES_DEREGISTERED = 8
PARTIES_WEBSITE_EN = 9
PARTIES_WEBSITE_FR = 10

parties = {}

with open(CA_PARTIES) as parties_file:
    party_reader = csv.reader(parties_file)
    next(party_reader) # skip header

    for party_data in party_reader:
        parties[party_data[PARTIES_ID]] = {
            'id': party_data[PARTIES_ID],
            'short_en': party_data[PARTIES_SHORT_EN],
            'short_fr': party_data[PARTIES_SHORT_FR],
            'common_en': party_data[PARTIES_COMMON_EN],
            'common_fr': party_data[PARTIES_COMMON_FR],
            'long_en': party_data[PARTIES_LONG_EN],
            'long_fr': party_data[PARTIES_LONG_FR],
            'registered': party_data[PARTIES_REGISTERED],
            'deregistered': party_data[PARTIES_DEREGISTERED],
            'website_en': party_data[PARTIES_WEBSITE_EN],
            'website_fr': party_data[PARTIES_WEBSITE_FR]
        }

with open(CA_PARTIES_JSON, 'w') as export_json:
    json.dump(parties, export_json)


# Open the parties map CSV file that maps various renderings of
# party names as the key to a party ID and save out as a JSON file

parties_map = {}

with open(CA_PARTIES_MAP) as parties_file:
    party_reader = csv.reader(parties_file)

    for party_data in party_reader:
        parties_map[party_data[0]] = party_data[1]

with open(CA_PARTIES_MAP_JSON, 'w') as export_json:
    json.dump(parties_map, export_json)