# F1 prediction Python and Scala implementations

## Contents
#### 1. Parser

## Parser

The goal of the parser (parser.py) is to get the data necessary for calculations from official F1 web-site (F1.com).

First it will ask the season, starting with which the data is needed. On web-page seasons from 1950 to current are available. The input format in '2015' or '1999'. In case of type you will be offered to re-enter.

After that the script will determine all the races needed from this period and start parsing. Before that, it will check if the date for the given period is already available. If not - it will proceed to parsing.

The data will be stored separately session by session in separate .csv files. The basic folder is './data', inside there are folders for each session type: practices from 1 to 3, qualifications and races.

After the work of the parser is done, the data will bw available for further processing.
