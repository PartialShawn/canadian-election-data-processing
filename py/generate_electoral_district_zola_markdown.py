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

# Load districts
federal_districts_json = open('data/ca-districts-index.json', 'r')
federal_districts = json.load(federal_districts_json)
federal_districts_json.close()


for id,district in districts.items():

    if id in federal_districts:
        district_name = federal_districts[id]['en']
    else:
        district_name = "Missing Riding Name"
        print("- Error: Missing riding name for",id)
    

    district_file = open(PATH_TO_EXPORT_ZOLA+id+'.md', 'w', encoding='utf8')
    district_file.write(f"""+++
title = "{district_name}"
[extra]
district_id = "{id}"
district_name = "{district_name}"
+++
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
    # print(id, end=" ")
    # print(district[0],end=" ")
    # print(district.items())
    # print(ed_num,"t", end=" ")