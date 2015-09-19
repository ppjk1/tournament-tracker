-- Table and view definitions for the tournament project.
-- SQL commands assume use of PostgreSQL.
--


DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;


-- Connect to database (psql cli command).
\c tournament


--
-- TABLES
--


-- Assign tournaments unique IDs.
CREATE TABLE tournament (
	tournament_id serial PRIMARY KEY
	,tournament_name varchar(100)
);


-- Assign players unique IDs.
CREATE TABLE player (
	player_id serial PRIMARY KEY
	,player_name varchar(100)
);


-- Composite primary key prevents rematches between two players in a given
-- tournament.
-- Match outcome may hold the following values:
--		0: Draw
--		1: Player1 wins
--		2: Player 2 wins
--		3: Player1 received a bye
CREATE TABLE match (
	player1 integer references player(player_id)
	,player2 integer references player(player_id)
	,outcome smallint
	,tournament_id integer references tournament(tournament_id)
	,PRIMARY KEY (player1, player2, tournament_id)
);


-- Allocates points by tournament for a single player.
--		match win 	= 3 points
--		bye			= 3 points
--		draw		= 1 point
-- Player allowed one "bye" per tournament, so we use a Boolean to flag.
CREATE TABLE player_points (
	player_id integer references player(player_id)
	,tournament_id integer references tournament(tournament_id)
	,points integer
	,bye boolean
	,PRIMARY KEY (player_id, tournament_id)
);


-- Matches players to tournaments.
-- Use to determine which players are registered for a given tournament.
CREATE TABLE player_tournaments (
	player_id integer references player(player_id)
	,tournament_id integer references tournament(tournament_id)
	,PRIMARY KEY (player_id, tournament_id)
);


--
-- FUNCTIONS
--


-- Deletes all data in the database.
CREATE FUNCTION clean_data() RETURNS void AS
	$body$
		TRUNCATE
			match
			,player
			,player_points
			,player_tournaments
			,tournament;
 	$body$
	LANGUAGE sql;


-- Pulls player ids, names, points, byes, and number of matches for a
-- given tournament.
CREATE FUNCTION player_standings(_tournament_id integer)
RETURNS TABLE (
	player_id integer
	,player_name text
	,points integer
	,bye boolean
	,matches_played bigint
	) AS
	$body$
		SELECT
			player_tournaments.player_id
			,player.player_name,
			( SELECT points FROM player_points
			  WHERE player.player_id = player_points.player_id
			  AND tournament_id = _tournament_id
		    ) AS points
			,( SELECT bye FROM player_points
		  	  WHERE player.player_id = player_points.player_id
			  AND tournament_id = _tournament_id
		  	) AS bye
		  	,( SELECT count(*) FROM match
			  WHERE match.tournament_id = _tournament_id
			    AND player.player_id = match.player1
				 OR player.player_id = match.player2
		  	) AS matches_played
		FROM player_tournaments
		JOIN player ON player_tournaments.player_id = player.player_id
		WHERE player_tournaments.tournament_id = _tournament_id
		ORDER BY points DESC;
	$body$
	LANGUAGE sql;
