# Tournament Planner
This program implements a Swiss-system tournament tracker.

Allows tracking of players and matches and automates pairing of players with a similar number of wins.


## Requirements
- Python 2.7
- psycopg2
- PostgreSQL
- psql


## Quick Start
- Ensure you have the required software installed (see Requirements)
- Clone the repo: `git clone https://github.com/ppjk1/tournament-tracker.git`
- Use a terminal to navigate into the **tournament-tracker** directory
- Use the psql command line to import **tournament.sql**:
```
$ psql
=> \i tournament.sql
=> \q
```
- Run the test suite to verify base functionality: `python tournament_test.py`


## What's Included
Within the download, you'll find the following files:
```
tournament/
  |--- tournament.py
  |--- tournament.sql
  |--- tournament_test.py
```

### Credits
Base requirements, function definitions, and unit tests were provided by [Udacity][] in the project starter kit.

[Udacity]: https://udacity.com
