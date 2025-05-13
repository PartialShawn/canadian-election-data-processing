# Generate Zola markdown files for all federal electoral districts.
#
# -----------------------------------------------------------------------------
#           Licensed under the Apache License, Version 2.0
# -----------------------------------------------------------------------------
#

from __init__ import *
from string import Template
import json
import os

# Load preliminary results
election_results_json = open(CA_ELECTIONS_RESULTS_OUTPUT[CA_GE_PRELIMINARY_ELECTION_NUMBER], 'r')
districts = json.load(election_results_json)
election_results_json.close()

# Load districts
federal_districts_json = open(CA_DISTRICTS_INDEX_FILENAME, 'r')
federal_districts = json.load(federal_districts_json)
federal_districts_json.close()

file_path = Template(ZOLA_CA_ELECTION_FILE_TEMPLATE)
election_path = Template(ZOLA_CA_ELECTION_PATH_TEMPLATE)
district_content = Template(ZOLA_DISTRICT_TEMPLATE)
election_content = Template(ZOLA_ELECTION_TEMPLATE)


print()
print('Creating election files...')

os.makedirs(election_path.substitute(section=ZOLA_FEDERAL_ELECTIONS_PATH, election_id=CA_GE_PRELIMINARY_ELECTION_NUMBER))

with open(file_path.substitute(section=ZOLA_FEDERAL_ELECTIONS_PATH, election_id=CA_GE_PRELIMINARY_ELECTION_NUMBER, district_id='_default'), 'w') as election_file:
    election_file.write(election_content.substitute(election_title='45th General Election', election_number=CA_GE_PRELIMINARY_ELECTION_NUMBER))

print(' ... done')
print()

print()
print('Creating district files...')

for id,district in districts.items():

    if id in federal_districts:
        district_name = federal_districts[id]['en']
    else:
        district_name = 'Missing Riding Name'
        print(' - Error: Missing riding name for',id)
    
    district_file = open(file_path.substitute(section=ZOLA_FEDERAL_ELECTIONS_PATH, election_id=CA_GE_PRELIMINARY_ELECTION_NUMBER, district_id=id), 'w', encoding='utf8')
    district_file.write(district_content.substitute(district_id=id, district_name=district_name))

print(' - created',len(districts.items()),'district files')
print(' ... done')

