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


ZOLA_DISTRICT_TEMPLATE = """+++
title = "$district_name"
[extra]
election_id = $election_id
district_id = "$district_id"
district_name = "$district_name"
+++
"""

ZOLA_ELECTION_TEMPLATE = """+++
title = '$election_title'
page_template = 'ca_election_district.html'
template = 'ca_election_overview.html'
sort_by = 'slug'
weight = $election_weight
[extra]
election_id = $election_number
+++
"""

ZOLA_CA_SECTION_FILE_PATH_TEMPLATE = '$section/$id.md'
ZOLA_CA_ELECTION_FILE_TEMPLATE = '$section/$election_id/$district_id.md'
ZOLA_CA_ELECTION_PATH_TEMPLATE = '$section/$election_id'

# Zola export
# ZOLA_FEDERAL_PATH = '../votes-count-zola/content/ca/'
ZOLA_FEDERAL_ELECTIONS_PATH = '../votes-count-zola/content/ca/election'
# ZOLA_FEDERAL_DISTRICTS_PATH = '../votes-count-zola/content/ca/district'
# ZOLA_FEDERAL_DISTRICTS_JSON = '../votes-count-zola/content/ca/district/preliminary_results.json'


def generate_election_files(election: dict):
    file_path = Template(ZOLA_CA_ELECTION_FILE_TEMPLATE)
    district_content = Template(ZOLA_DISTRICT_TEMPLATE)
    election_content = Template(ZOLA_ELECTION_TEMPLATE)
    election_path = Template(ZOLA_CA_ELECTION_PATH_TEMPLATE)
    election_weight = 100-int(election['id'])

    print()
    print('Generating ',election['id'])

    if not os.path.isdir(election_path.substitute(section=ZOLA_FEDERAL_ELECTIONS_PATH, election_id=election['id'])):
        os.makedirs(election_path.substitute(section=ZOLA_FEDERAL_ELECTIONS_PATH, election_id=election['id']))

    with open(file_path.substitute(section=ZOLA_FEDERAL_ELECTIONS_PATH, election_id=election['id'], district_id='_index'), 'w') as election_file:
        election_file.write(election_content.substitute(election_title='General Election '+election['id'], election_number=election['id'], election_weight=election_weight))

    print(' - Created default file')
    
    election_results_json = open(election['data']['results'], 'r')
    districts = json.load(election_results_json)
    election_results_json.close()

    for id,district in districts.items():
        district_file = open(file_path.substitute(section=ZOLA_FEDERAL_ELECTIONS_PATH, election_id=election['id'], district_id=id), 'w', encoding='utf8')
        district_file.write(district_content.substitute(election_id=election['id'], district_id=id, district_name=district['name']))

    print(' - created',len(districts.items()),'district files')
    print(' ... done')



for election in CA_GE_ELECTIONS.values():
    generate_election_files(election)