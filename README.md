# Canadian Election Data Processing

Elections Canada data files and Python script to parse the data and perform more calculations.

---

## Sources

Uses data from Elections Canada. I assume, all Elections Canada data is posted under the [Open Government Licence - Canada](https://open.canada.ca/en/open-government-licence-canada).

## Open Government data (under OGL-C):

* [Open Government search for "General election](https://open.canada.ca/data/en/organization/elections?q="General+Election")
  * Official Voting Results tables: [43GE](https://open.canada.ca/data/en/dataset/199e5070-2fd5-49d3-aa21-aece08964d18), [42GE](https://open.canada.ca/data/en/dataset/775f3136-1aa3-4854-a51e-1a2dab362525), [44GE](https://open.canada.ca/data/en/dataset/065439a9-c194-4259-9c95-245a852be4a1)
  * Poll-by-poll results: [39](https://open.canada.ca/data/en/dataset/d62cf7b7-c180-4115-b0a6-546a85d6419f), [38](https://open.canada.ca/data/en/dataset/3d44e2da-3e36-45cf-ab2a-037801eaaa6b), [40](https://open.canada.ca/data/en/dataset/d356c792-5cb0-46c1-be74-a86f804a0e93), [40](https://open.canada.ca/data/en/dataset/d356c792-5cb0-46c1-be74-a86f804a0e93), [41](https://open.canada.ca/data/en/dataset/b1fabdfd-72c5-42b0-a07e-a04e0148f7a4), [42](https://open.canada.ca/data/en/dataset/6a919bd5-491e-466e-a279-00cbf7a8e02c), [43](https://open.canada.ca/data/en/dataset/98654d8e-9fda-47d4-ad76-889ef3d5c801), [44](https://open.canada.ca/data/en/dataset/d5512235-cfb2-4ccf-a886-547913f4aa52)
  * Includes briefings, turnout by age, gender and province, and the poll-by-poll results of the 44GE transposed to to the new boundaries of the 45GE
* [History of the Federal Electoral Ridings, 1867-2010](https://open.canada.ca/data/en/dataset/ea8f2c37-90b6-4fee-857e-984d3060184e) will be processed in the future.

# Other election data

Might be Open Government data.

* [Past Elections (1996 (36GE) to present)](https://www.elections.ca/content.aspx?section=ele&dir=pas&document=index&lang=e)
* [Voter Turnout at Federal Elections and Referendums](https://www.elections.ca/content.aspx?section=ele&dir=turn&document=index&lang=e) might include data not in the above.


---

## Related projects

This project:

* [https://github.com/ktrieu/electoral-codex](https://github.com/ktrieu/electoral-codex): A cleaned, formatted dataset of Canadian federal elections from 2004 to 2015. Python. Includes raw data, some basic processed CSV. Creates .db files for each election year.
* [https://github.com/bwbecker/cdnFedElectionData](https://github.com/bwbecker/cdnFedElectionData): Canadian Federal Election Data. CSV, raw data. Bash files to clean the data?
* [https://github.com/fosskers/election](https://github.com/fosskers/election): Analysis of Canadian Federal Elections Data in Rust. Download your own data. Processes results.
* [https://github.com/krzysztofmajewski/voting](https://github.com/krzysztofmajewski/voting): Processing voting data in Python.
Libraries:
* [https://github.com/paleolimbot/electionca](https://github.com/paleolimbot/electionca): The goal of electionca is to provide Canadian (general) election data in an easily accessible format for R users. May include some data.

Some data files:

* [lchski/canada-2015-federal-election-data](https://github.com/lchski/canada-2015-federal-election-data): JSON data for the 2015 Canadian federal election.
* [https://github.com/dsartori/CanadianElectionResults](https://github.com/dsartori/CanadianElectionResults): A Microsoft SQL database of election results for 2015 and 2019 and the SSIS package to generate them from raw Elections Canada data.
* [https://github.com/mitchalexbailey/canadian_elections](https://github.com/mitchalexbailey/canadian_elections): . [View Canadian Elections Data Visualization](Canadian Elections Data Visualization) on Shiny App. It's basic and cool. Contains just the data for 2006-2015.
