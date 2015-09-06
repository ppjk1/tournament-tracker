-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

-- Connect to database (psql cli command)
\c tournament

CREATE TABLE players (
	id serial primary key,
	name text
);

CREATE TABLE matches (
    id serial primary key,
	winner integer references players(id),
	loser integer references players(id)
);

CREATE VIEW player_standings AS
	SELECT players.id, players.name, count(matches.winner) as wins,
		(SELECT count(*) FROM matches
		 WHERE matches.winner = players.id OR matches.loser = players.id
	 	 ) as match_num
	FROM players FULL OUTER JOIN matches
	ON players.id = matches.winner
	GROUP BY players.id
	ORDER BY wins DESC;
