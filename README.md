# Tournament Planner #
This program implements a Swiss-system tournament tracker.

Allows tracking of players and matches and automates pairing of players with a similar number of points.

Features:
- Supports multiple tournaments
- Supports even or odd number of players via "bye" system (odd players allowed equivalent of one free match win per tournament)
- Supports draws (both players receive 1 point for the match rather than 3 points to the winner and 0 to the loser)
- Database table design prevents rematches between players in a single tournament


## Requirements ##
- Python 2.7
- psycopg2
- PostgreSQL
- psql


## Quick Start ##
- Ensure you have the required software installed (see Requirements)
- Clone the repo:
        git clone https://github.com/ppjk1/tournament-tracker.git
- Use a terminal to navigate into the **tournament-tracker** directory
- Use the psql command line to import **tournament.sql**:
```
$ psql
=> \i tournament.sql
=> \q
```
- Run the test suite to verify base functionality:
        python tournament_test.py
- You should see the following output:
```
1 All data can be successfully deleted.
2 After deleting, countAllPlayers() returns zero.
3 After creating a player, countAllPlayers() returns 1.
4 After deleting, countTournaments() returns zero.
5 After creating a tournament, countTournaments() returns 1.
6 After tournament creation, countRegisteredPlayers() returns zero.
7 After registering a player, countRegisteredPlayers() returns 1.
8 Players can be registered and deleted.
9 Newly registered players appear in the standings with no matches.
10 After a match, players have updated standings.
11 After one match, players with equal or nearly-equal number of
Success!  All tests pass!
```


## What's Included ##
Within the download, you'll find the following files:
```
tournament/
  |--- README.md
  |--- tournament.py
  |--- tournament.sql
  |--- tournament_test.py
```


## Table Design ##
Master tables:
- **tournament**: stores tournament names and ids
- **player**: stores player names and ids

Reference tables:
- **player_tournaments**: maps players to the tournaments for which they are registered
- **match**: stores player pairs, the appropriate tournament id, and the outcome of the match:
    - player1 win
    - player2 win
    - draw
    - bye
- **player_points**: stores player points per tournament along with a boolean value for whether they have already been given a bye


### Credits ###
Base requirements and unit tests were provided by [Udacity](https://udacity.com) in the project starter kit.

Additional credits:
- [Checking local variable existence in Python](http://stackoverflow.com/questions/843277/how-do-i-check-if-a-variable-exists-in-python)
- [Reverse list traveral in Python (with access to index)](http://stackoverflow.com/questions/529424/traverse-a-list-in-reverse-order-in-python)
