# Parse Elections Canada table 8 (format 1996) to get all party names
#
# -----------------------------------------------------------------------------
#           Licensed under the Apache License, Version 2.0
# -----------------------------------------------------------------------------
#



import csv, json

# Initialize variables
parties = []

with open('data-source/ca_ge44_table_tableau08.csv', encoding='utf8') as table8:
    table_reader = csv.reader(table8)
    next(table_reader)

    for party_data in table_reader:
        name_en, name_fr = party_data[0].split('/')
        parties.append(party_data[0])

export_json = open('data/ca_party_names_combined.json', 'w')
json.dump(parties, export_json)
export_json.close()