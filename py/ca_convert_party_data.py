# Convert `parties.csv` and `parties_map.csv` to JSON lookup files.
#
# -----------------------------------------------------------------------------
#           Licensed under the Apache License, Version 2.0
# -----------------------------------------------------------------------------

from __init__ import *
import sys, csv, json



# Part 1: Open the parties CSV and create a dictionary of all party data
# with the party ID as key, and save out as JSON.

parties = {}

print()
print("Converting parties CSV file ...")

try:
    with open(CA_PARTIES_SOURCE, encoding='utf8') as parties_file:
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
        
        print(' - read', len(parties), 'lines')

except FileNotFoundError:
    print("\nError reading parties CSV file: file not found.")
    sys.exit(1)

with open(CA_PARTIES_JSON_FILENAME, 'w', encoding='utf8') as export_json:
    json.dump(parties, export_json)

print(' - JSON file written')


# Part 2: Open the parties map CSV file that maps various renderings of
# party names as the key to a party ID and save out as a JSON file

parties_map = {}

print()
print("Converting parties map...")

try:
    with open(CA_PARTIES_MAP_SOURCE, encoding='utf8') as parties_file:
        party_reader = csv.reader(parties_file)

        for party_data in party_reader:
            parties_map[party_data[0]] = party_data[1]

    print(" - read", len(parties_map), "lines")
except FileNotFoundError:
    print ("\nError reading file parties map CSV: file not found.")
    sys.exit(1)

with open(CA_PARTIES_MAP_JSON_FILENAME, 'w', encoding='utf8') as export_json:
    json.dump(parties_map, export_json)

print(' - JSON file written')

print()
print('Converting f96 parties map...')

parties_map = {}
try:
    with open(CA_PARTIES_MAP_SHORT_SOURCE, encoding='utf8') as parties_file:
        party_reader = csv.reader(parties_file)

        for party_data in party_reader:
            parties_map[party_data[0]] = party_data[1]

    print(" - read", len(parties_map), "lines")
except FileNotFoundError:
    print ("\nError reading file parties map CSV: file not found.")
    sys.exit(1)

with open(CA_PARTIES_MAP_SHORT_JSON_FILENAME, 'w', encoding='utf8') as export_json:
    json.dump(parties_map, export_json)

print(' - JSON file written')
