#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *


def testDeleteAllData():
    deleteAllData()
    print "1. All data can be successfully deleted."


def testCountAllPlayers():
    deleteAllData()
    c = countAllPlayers()
    if c == '0':
        raise TypeError(
            "countAllPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError(
            "After deleting, countAllPlayers() should return zero.")
    print "2. After deleting, countAllPlayers() returns zero."


def testCreatePlayer():
    deleteAllData()
    player_id = createPlayer("Chandra Nalaar")
    c = countAllPlayers()
    if c != 1:
        raise ValueError(
            "After creating one player, countAllPlayers() should be 1.")
    print "3. After creating a player, countAllPlayers() returns 1."


def testCountTournaments():
    deleteAllData()
    c = countTournaments()
    if c == '0':
        raise TypeError(
            "countTournaments() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError(
            "After deleting, countTournaments() should return zero.")
    print "4. After deleting, countTournaments() returns zero."


def testCreateTournament():
    deleteAllData()
    tournament_id = createTournament("Hocus Pocus the Getting Together")
    c = countTournaments()
    if c != 1:
        raise ValueError(
            "After creating one tournament, countTournaments() should be 1.")
    print "5. After creating a tournament, countTournaments() returns 1."


def testCountRegisteredPlayers():
    deleteAllData()
    tournament_id = createTournament("Hocus Pocus the Getting Together")
    c = countRegisteredPlayers(tournament_id)
    if c == '0':
        raise TypeError(
            "countRegisteredPlayers() should return numeric zero, not string "
            "'0'.")
    if c != 0:
        raise ValueError(
            "After initial tournament creation, countRegisteredPlayers() "
            "should return zero.")
    print "6. After tournament creation, countRegisteredPlayers() returns zero."


def testRegister():
    deleteAllData()
    tournament_id = createTournament("Hocus Pocus the Getting Together")
    player_id = createPlayer("Chandra Nalaar")
    registerPlayer(player_id, tournament_id)
    c = countRegisteredPlayers(tournament_id)
    if c != 1:
        raise ValueError(
            "After one player registers, countRegisteredPlayers() should be 1.")
    print "7. After registering a player, countRegisteredPlayers() returns 1."


def testRegisterCountDelete():
    deleteAllData()
    tournament_id = createTournament("The Big Four")
    players = ["Markov Chaney", "Joe Malik", "Mao Tsu-hsi", "Atlanta Hope"]
    player_ids = []
    for p in players:
        player_ids.append(createPlayer(p))
    for pid in player_ids:
        registerPlayer(pid, tournament_id)
    c = countRegisteredPlayers(tournament_id)
    if c != 4:
        raise ValueError(
            "After registering four players, countRegisteredPlayers() "
            "should be 4.")
    removeRegisteredPlayers(tournament_id)
    c = countRegisteredPlayers(tournament_id)
    if c != 0:
        raise ValueError(
            "After deleting, countRegisteredPlayers() should return zero.")
    print "8. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteAllData()
    tournament_id = createTournament("The Big Four")
    player1_id = createPlayer("Melpomene Murray")
    player2_id = createPlayer("Randy Schwartz")
    registerPlayer(player1_id, tournament_id)
    registerPlayer(player2_id, tournament_id)
    standings = playerStandings(tournament_id)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 5:
        raise ValueError("Each playerStandings row should have five columns.")
    [(id1, name1, points1, bye1, matches1),
     (id2, name2, points2, bye2, matches2)] = standings
    if (matches1 != 0 or matches2 != 0 or points1 is not None or
            points2 is not None):
        raise ValueError(
            "Newly registered players should have no matches or points.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError(
            "Registered players' names should appear in standings, even if "
            "they have no matches played.")
    print "9. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteAllData()
    tournament_id = createTournament("Tourney of the Year")
    players = ["Bruno Walton", "Boots O'Neal", "Perry Elbert",
               "George Wexford-Smythe III", "Mark Davies", "Elmer Drimsdale",
               "Calvin Fitzgart"]
    player_ids = []
    for p in players:
        player_ids.append(createPlayer(p))
    for pid in player_ids:
        registerPlayer(pid, tournament_id)
    standings = playerStandings(tournament_id)
    [id1, id2, id3, id4, id5, id6, id7] = [row[0] for row in standings]
    reportMatch(tournament_id, 0, id1, id2)  # Draw
    reportMatch(tournament_id, 1, id3, id4)  # Player 1 wins
    reportMatch(tournament_id, 2, id5, id6)  # Player 2 wins
    reportMatch(tournament_id, 3, id7, id7)  # Bye assigned to odd player
    standings = playerStandings(tournament_id)
    for (i, n, p, b, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id2) and p != 1:
            raise ValueError(
                "Each match draw participant should have one point recorded.")
        elif i in (id3, id6) and p != 3:
            raise ValueError(
                "Each match winner should have three points recorded.")
        elif i in (id4, id5) and p != 0:
            raise ValueError(
                "Each match loser should have zero points recorded.")
        elif i in (id7, id7) and p != 3:
            raise ValueError(
                "Each bye recipient should have three points recorded.")
    print "10. After a match, players have updated standings."


def testPairings():
    deleteAllData()
    tournament_id = createTournament("My Little Pony Ultimate Frisbee")
    players = ["Twilight Sparkle", "Rainbow Dash", "Fluttershy", "Pinkie Pie",
               "Applejack", "Rarity", "Princess Celestia"]
    player_ids = []
    for p in players:
        player_ids.append(createPlayer(p))
    for pid in player_ids:
        registerPlayer(pid, tournament_id)
    standings = playerStandings(tournament_id)
    [id1, id2, id3, id4, id5, id6, id7] = [row[0] for row in standings]
    reportMatch(tournament_id, 0, id1, id2)  # draw
    reportMatch(tournament_id, 1, id3, id4)  # id3 wins
    reportMatch(tournament_id, 2, id5, id6)  # id6 wins
    reportMatch(tournament_id, 3, id7, id7)  # bye -> id7
    pairings = swissPairings(tournament_id)
    if len(pairings) != 4:
        raise ValueError(
            "For seven players, swissPairings should return four pairs.")
    [(pid1, pname1, pid2, pname2),
     (pid3, pname3, pid4, pname4),
     (pid5, pname5, pid6, pname6),
     (pid7, pname7, pid8, pname8)] = pairings
    correct_pairs = set([
                        frozenset([id6, id7]),
                        frozenset([id3, id1]),
                        frozenset([id2, id4]),
                        frozenset([id5, id5])
                        ])
    actual_pairs = set([
                        frozenset([pid1, pid2]),
                        frozenset([pid3, pid4]),
                        frozenset([pid5, pid6]),
                        frozenset([pid7, pid8])
                        ])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with equal or nearly-equal number of "
            "points should be paired.")
    print "11. After one match, players with equal or nearly-equal number of "
    "points are paired."


if __name__ == '__main__':
    testDeleteAllData()
    testCountAllPlayers()
    testCreatePlayer()
    testCountTournaments()
    testCreateTournament()
    testCountRegisteredPlayers()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"
