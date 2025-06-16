# Parse Elections Canada preliminary results (GE45) to get all district
# names and numbers. The 2024 boundary changes mean there are new
# districts not previously in the data files.
#
# -----------------------------------------------------------------------------
#           Licensed under the Apache License, Version 2.0
# -----------------------------------------------------------------------------
#
"""
    Scans thru data files and keeping a records of all district names and
    numbers. Exports these to a data files.
"""

from __init__ import *
import csv, json

districts_index = {} # All districts with district number as key

with open('data-source/ca_ge45_preliminary_candidates_2025-06-13.tsv', encoding='utf8') as prelim:
    table_reader = csv.reader(prelim, delimiter='\t')
    next(table_reader)  # skip the headers
    next(table_reader)

    for district in table_reader:

        if district[0][0] == '*': continue # Skip if a footnote
        sgc_code = district[PRELIM_ED_NUM][:2]
        # Add to dictionary of electoral districts
        districts_index[district[PRELIM_ED_NUM]] = {'code': district[PRELIM_ED_NUM], 'province': SGC_TO_ALPHA[sgc_code], 'en': district[PRELIM_ED_NAME_EN], 'fr': district[PRELIM_ED_NAME_FR]}


# JSON export index of all districts
export_json = open(CA_DISTRICTS_INDEX_FILENAME, 'w', encoding='utf8')
json.dump(districts_index, export_json)
export_json.close()