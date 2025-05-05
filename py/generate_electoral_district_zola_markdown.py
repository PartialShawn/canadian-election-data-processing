# Generate Zola markdown files for all federal electoral districts.
#
# -----------------------------------------------------------------------------
#           Licensed under the Apache License, Version 2.0
# -----------------------------------------------------------------------------
#

import __init__, json
PATH_TO_EXPORT_ZOLA = '../votes-count-zola/content/ca/'

# Load preliminary results
election_results_json = open('data/preliminary_results.json', 'r')
districts = json.load(election_results_json)
election_results_json.close()

print(PATH_TO_EXPORT_ZOLA)
for id,district in districts.items():
    district_file = open(PATH_TO_EXPORT_ZOLA+id+'.md', 'w')
    district_file.write(f"""+++
title = '{id}'
[extra]
district_id = '{id}'
+++
{id}
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