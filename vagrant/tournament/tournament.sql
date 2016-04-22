-- Table definitions for the tournament project.

CREATE DATABASE tournament;

\CONNECT tournament;

DROP TABLE IF EXISTS Players CASCADE;

CREATE TABLE Players (id serial PRIMARY KEY, playername varchar NOT NULL);

DROP TABLE IF EXISTS Matches;

CREATE TABLE Matches (id serial PRIMARY KEY,
                      winner int REFERENCES Players (id),
                      loser int REFERENCES Players (id)
                    );

CREATE OR REPLACE VIEW standings AS
SELECT P.id AS id,
       P.playername AS name,

    (SELECT COALESCE(COUNT(M.winner),0)
     FROM Matches M
     WHERE M.winner = P.Id) AS wins,

    (SELECT COALESCE(COUNT(M.Id),0)
     FROM Matches M
     WHERE M.Winner = P.Id
         OR M.loser = P.Id) AS matches
FROM Players P;
