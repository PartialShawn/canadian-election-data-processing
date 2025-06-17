# Process all election data.
#
# -----------------------------------------------------------------------------
#           Licensed under the Apache License, Version 2.0
# -----------------------------------------------------------------------------
#

from __init__ import *
import json
from ElectionResultsClass import *
from ElectionResultsCa40Class import *
from ElectionResultsCaPrelimClass import *


print()
for election in CA_GE_ELECTIONS.values():
    print('Processing election',election['id'],election['type'], '...')

    try:
        if election['format'] == 'f96':
            e = ElectionResultsCa40(election)
        elif election['format'] == 'preliminary':
            e = ElectionResultsCaPrelim(election)
        else:
            raise ValueError("Invalid format: "+election['format'])

        # print(e.meta)

    except ValueError as err:
        print(err)



