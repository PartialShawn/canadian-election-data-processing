# Elections Canada Format 1996 (F96)

F96 is the format for elections results using since 1996 in elections and by-elections.



Table 1: Number of electors and polling stations
Table 2: Number of electors and polling stations for the 2019, 2015, 2011 and 2008 general elections
Table 3: Number of ballots cast and voter turnout
Table 4: Voter turnout for the 2019, 2015, 2011 and 2008 general elections
Table 5: Distribution of valid votes by voting method
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