#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteAllData():
    """Removes all data from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT clean_data();")
    conn.commit()
    conn.close()


def countAllPlayers():
    """Returns the number of players in the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count(*) FROM player;")
    player_count = c.fetchone()[0]
    conn.close()
    return player_count


def createPlayer(player_name):
    """Adds a player to the database.

    The database assigns a unique serial id for the player.

    Args:
      player_name: the name of the player (need not be unique)
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO player (player_name) VALUES (%s) "
              "RETURNING player_id", (player_name,))
    player_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    return player_id


def countTournaments():
    """Returns the number of tournaments in the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count(*) FROM tournament;")
    tournament_count = c.fetchone()[0]
    conn.close()
    return tournament_count


def createTournament(tournament_name):
    """Adds a tournament to the tournament database.

    The database assigns a unique serial id for the tournament.

    Args:
      tournament_name: the name of the tournament (need not be unique)
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO tournament (tournament_name) VALUES (%s) "
              "RETURNING tournament_id", (tournament_name,))
    tournament_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    return tournament_id


def countRegisteredPlayers(tournament_id):
    """Returns the number of players registered for a given tournament.

    Args:
      tournament_id: the id number for the tournament
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count(*) FROM player_tournaments \
              WHERE tournament_id = %s", (tournament_id,))
    player_count = c.fetchone()[0]
    conn.close()
    return player_count


def registerPlayer(player_id, tournament_id):
    """Registers a player for a tournament.

    Args:
      player_id: the id number for the player
      tournament_id: the id number for the tournament
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO player_tournaments (player_id, tournament_id) \
              VALUES (%s, %s)", (player_id, tournament_id))
    conn.commit()
    conn.close()


def removeRegisteredPlayers(tournament_id):
    """Removes all player registrations for a given tournament.

    Args:
        tournament_id: the id number for the tournament
    """
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM player_tournaments \
               WHERE tournament_id = %s", (tournament_id,))
    conn.commit()
    conn.close()


def playerStandings(tournament_id):
    """Returns a list of the players and their records for a given
    tournament, sorted by points.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Args:
        tournament_id: the id number for the tournament

    Returns:
    A list of tuples, each of which contains (id, name, points, bye, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        points: the number of points the player has received; aggregates wins,
                draws, and byes
        bye: whether the player has received a bye in this tournament
        matches: the number of matches the player has played in this tournament
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM player_standings(%s)",
              (tournament_id,))
    standings = c.fetchall()
    conn.commit()
    conn.close()
    return standings


def updatePoints(player_id, tournament_id, points, bye='false'):
    """Updates a player's points following a match.

    Args:
      player_id: the id number of the player
      tournament_id: the id number of the tournament
      points: (integer) number of points player is receiving
      bye: a Boolean flag indicating whether the player received a bye for
           the match
    """
    conn = connect()
    c = conn.cursor()

    # Pull appropriate record to update
    c.execute("SELECT * FROM player_points WHERE player_id = %s \
            AND tournament_id = %s", (player_id, tournament_id))
    points_record = c.fetchall()

    # If record exists, update it. Otherwise, create a new record.
    if len(points_record) > 0:
        points = points + points_record[0][2]
        c.execute(
            "UPDATE player_points SET points = %s, bye = %s \
            WHERE player_id = %s AND tournament_id = %s",
            (points, bye, points_record[0][0], points_record[0][1]))
    else:
        c.execute(
            "INSERT INTO player_points VALUES (%s, %s, %s, %s)",
            (player_id, tournament_id, points, bye))

    conn.commit()
    conn.close()


def reportMatch(tournament_id, outcome, player1, player2):
    """Records the outcome of a single match between two players.

    Args:
      tournament_id: the id number for the tournament
                     in which the match took place
      outcome:
        0 for a draw
        1 for a player1 win
        2 for a player2 win
        3 for a bye
      player1: the id number of the first player
      player2: the id number of the second player;
               same as player1 in case of bye
    """
    conn = connect()
    c = conn.cursor()

    # Store the match
    c.execute("INSERT INTO match (player1, player2, outcome, tournament_id) \
               VALUES (%s, %s, %s, %s)",
              (player1, player2, outcome, tournament_id))

    # Update player points
    # Draw
    if outcome == 0:
        updatePoints(player1, tournament_id, 1)
        updatePoints(player2, tournament_id, 1)
    # Player 1 wins
    elif outcome == 1:
        updatePoints(player1, tournament_id, 3)
        updatePoints(player2, tournament_id, 0)
    # Player 2 wins
    elif outcome == 2:
        updatePoints(player1, tournament_id, 0)
        updatePoints(player2, tournament_id, 3)
    # Bye: assigned to player1 by default
    elif outcome == 3:
        updatePoints(player1, tournament_id, 3, 'true')

    conn.commit()
    conn.close()


def swissPairings(tournament_id):
    """Returns a list of pairs of players for the next round of a match.

    Each player is paired with another player with an equal or nearly-equal win
    record, that is, a player adjacent to him or her in the standings.

    In the event there is an odd number of players, the last pairing returned
    will contain the odd player paired against themself. They should be
    assigned a bye for the round. Only one bye is allowed per player per
    tournament.

    Args:
        tournament_id: the id number for the tournament

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings(tournament_id)

    # If we have an odd number of players, find the lowest ranked player
    # without a bye and pull them from the standings array.
    # Reference for traversing list in reverse (with access to index):
    #   http://stackoverflow.com/questions/529424/traverse-a-list-in-reverse-order-in-python  # noqa
    if len(standings) % 2 == 1:
        for i, player in reversed(list(enumerate(standings))):
            if player[3] == False:
                bye_player = standings.pop(i)
                break

    # Players are already sorted based on number of points and we now have
    # an even number of players.
    # Iterate in hops of two to get our pairings.
    pairings = []
    i = 0
    while(i < len(standings)-1):
        pairings.append(
            (standings[i][0],
             standings[i][1],
             standings[i+1][0],
             standings[i+1][1])
        )
        i = i + 2

    # Add bye player (if we have one)
    # Reference (checking if variable exists):
    #   http://stackoverflow.com/questions/843277/how-do-i-check-if-a-variable-exists-in-python  # noqa
    if "bye_player" in locals():
        pairings.append(
            (bye_player[0],
             bye_player[1],
             bye_player[0],
             bye_player[1])
        )
    return pairings
