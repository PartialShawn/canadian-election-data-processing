# Generate Zola markdown files for all federal electoral districts.
#
# -----------------------------------------------------------------------------
#           Licensed under the Apache License, Version 2.0
# -----------------------------------------------------------------------------
#

import __init__, json
ZOLA_CONTENT_PATH = '../votes-count-zola/content/'
ELECTIONS_PATH = ZOLA_CONTENT_PATH+'election/'
DISTRICTS_PATH = ZOLA_CONTENT_PATH+'ca/'


# Load preliminary results
election_results_json = open('data/preliminary_results.json', 'r')
districts = json.load(election_results_json)
election_results_json.close()

for id,district in districts.items():
    district_file = open(DISTRICTS_PATH+id+'.md', 'w')
    district_file.write(f"""+++
title = '{id}'
[extra]
district_id = '{id}'
+++
{id}
""")

with open(ELECTIONS_PATH+'ge44.md', 'w') as election_file:
    election_file.write(f"""+++
title = '44th General Election'
[extra]
election_id = 44
""")
    # print('\n****',id,end=": ")
    # for candidate in district:
    #     "test"
    #    # print(candidate['party'],end=",")
    # print(ed_num, end="")
    print(id, end=" ")
    # print(district[0],end=" ")
    # print(district.items())
    # print(ed_num,"t", end=" ")