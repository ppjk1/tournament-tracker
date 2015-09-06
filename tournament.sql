-- Table and view definitions for the tournament project.
-- SQL commands assume use of PostgreSQL.
--


CREATE DATABASE tournament;


-- Connect to database (psql cli command).
\c tournament


-- Store player names matched to unique incrementing IDs.
CREATE TABLE players (
	id serial primary key,
	name text
);


-- Assign matches unique IDs.
-- Reference winner/loser from players table by ID.
CREATE TABLE matches (
    id serial primary key,
	winner integer references players(id),
	loser integer references players(id)
);


-- Pulls player ids and names from players table.
-- Aggregates wins and total matches per player.
-- Results returned ordered by descending number of wins.
CREATE VIEW player_standings AS
	SELECT players.id, players.name, count(matches.winner) as wins,
		( SELECT count(*) FROM matches
		  WHERE matches.winner = players.id
		      OR matches.loser = players.id
	 	) as match_num
	FROM players FULL OUTER JOIN matches
	ON players.id = matches.winner
	GROUP BY players.id
	ORDER BY wins DESC;
