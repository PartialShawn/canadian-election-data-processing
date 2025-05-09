# Election Canada Auxiliary Data Files

`ca__voter_turnout.tsv`

- Copied from [Voter Turnout at Federal Elections and Referendums](https://www.elections.ca/content.aspx?section=ele&dir=turn&document=index&lang=e)
- Used corrected numbers as per footnotes
- Removed footnotes
- Added † marker for referendums, ignored footnote 3.
- For the GE45 I used the [Canada's population estimates, fourth quarter 2024](https://www150.statcan.gc.ca/n1/daily-quotidien/250319/dq250319a-eng.htm?HPA=1&indid=4098-1&indgeo=0) from Stats Can.
- I should find the quarterly population updated for future updates


`ca_ge.csv`

Election dates of elections, stolen from `ca__voter_turnout.tsv` (above). Dates in `d B Y` format.


`parties.csv` and `parties_map.csv`

- Copied from https://www.elections.ca/content.aspx?section=pol&document=index&dir=par&lang=e and https://www.elections.ca/content.aspx?section=pol&document=index&dir=par&lang=f
- Added IDs for each party.
- `parties.csv` gives data on parties
- `parties_map.csv` has mapping data from common party names to the ID