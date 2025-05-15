# Elections Canada Format 1996 (F96)

F96 is the format for elections results using since 1996 in elections and by-elections.

- GE40-41 tables used cp1252 encoding.
- GE39-44 tables used utf8 encoding.

- GE40 (2008) table 12 omitted the empty comma separators at the end of the last line.
- GE39 (2006) tables 11 and 12 does not have the district number.

## Table 1: Number of electors and polling stations
-Province
-Population
-Electors
-Stationary Polls
-Mobile Polling Stations
-Advance Polls
-Total Polling Stations

## Table 2: Number of electors and polling stations for the 2019, 2015, 2011 and 2008 general elections
- Province
- Electors 2021
- Electors 2019
- Electors 2015
- Electors 2011
- Polling Stations 2021
- Polling Stations 2019
- Polling Stations 2015
- Polling Stations 2011
- Average Number of Electors per Poll 2021
- Average Number of Electors per Poll 2019
- Average Number of Electors per Poll 2015
- Average Number of Electors per Poll 2011

## Table 3: Number of ballots cast and voter turnout
-Province
-Population
-Electors
-Valid Ballots
-Percentage of Valid Ballots
-Rejected Ballots
-Percentage of Rejected Ballots
-Total Ballots Cast
- Percentage of Voter Turnout

## Table 4: Voter turnout for the 2019, 2015, 2011 and 2008 general elections

## Table 5: Distribution of valid votes by voting method

- Province
- Stationary Poll
- Mobile Poll
- Advance polling stations
- Special ballot
- Total ballots


Table 6: Distribution of valid votes under Special Voting Rules
Table 7: Distribution of seats by political affiliation and sex
Table 8: Number of valid votes by political affiliation
Table 9: Percentage of valid votes by political affiliation
Table 10: Number of candidates by percentage of valid votes received, by political affiliation


## Table 11 Columns

Table 11: Voting results by electoral district

Elected candidate from all ridings.

- Province
  - text/varchar, `/` as multilingual delimiter
- Electoral District Name/Nom de circonscription
  - text/varchar, `/` as multilingual delimiter
- Electoral District Number/Numéro de circonscription
- Population
- Electors/Électeurs
- Polling Stations/Bureaux de scrutin
- Valid Ballots/Bulletins valides
- Percentage of Valid Ballots /Pourcentage des bulletins valides
  - decimal to one decimal place
- Rejected Ballots/Bulletins rejetés
- Percentage of Rejected Ballots /Pourcentage des bulletins rejetés
  - decimal to one decimal place
- Total Ballots Cast/Total des bulletins déposés
- Percentage of Voter Turnout/Pourcentage de la participation électorale
  - decimal to one decimal place
- Elected Candidate/Candidat élu
  - text/varchar
  - then space character
  - then affiliation, `/` as multilingual delimiter

## Table 12 Columns:

Table 12: List of candidates by electoral district and individual results

All candidates from all ridings

- Province
  - text/varchar, `/` as multilingual delimiter
- Electoral District Name/Nom de circonscription
  - text/varchar, `/` as multilingual delimiter
- Electoral District Number/Numéro de circonscription
- Candidate/Candidat
- Candidate Residence/Résidence du candidat
  - text/varchar, `/` as multilingual delimiter
- Candidate Occupation/Profession du candidat
  - text/varchar, `/` as multilingual delimiter
- Votes Obtained/Votes obtenus
- Percentage of Votes Obtained /Pourcentage des votes obtenus
- Majority/Majorité
- Majority Percentage/Pourcentage de majorité

## Table 13

Table 13: List of returning officers

Not used.

## poll by poll - format 2
Used for rejected ballots only--but also has party short form name?

- Electoral District Number
- Electoral District Name_English
- Electoral District Name_French
- Polling Station Number
- Polling Station Name (A name that generally represents the locality of the polling division boundary.)
- Void Poll Indicator (Indicates that a poll exists but has no electors.)
- No Poll Held Indicator (Indicates that the returning officer intended to hold this poll, but unforeseen circumstances prevented it.)
- Merge With (Indicates the number of the polling station with which the results of this poll were merged.)
- Rejected Ballots for Polling Station
- Electors for Polling Station
- Candidate’s Family Name
- Candidate’s Middle Name
- Candidate’s First Name
- Political Affiliation Name_English 	The short-form English name of the candidate’s political affiliation.
- Political Affiliation Name_French 	The short-form French name of the candidate’s political affiliation.
- Incumbent Indicator (Y/N)
- Elected Candidate Indicator (Y/N)
- Candidate Poll Votes Count