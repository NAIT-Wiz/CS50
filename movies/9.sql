--- SQL query to list the names of all people who starred in a movie released in 2004, ordered by birth year
SELECT DISTINCT p.name
FROM people p
JOIN stars s ON p.id = s.person_id
JOIN movies m ON s.movie_id = m.id
WHERE m.year = 2004
ORDER BY p.birth;


SELECT *
FROM interviews
WHERE (id = '162' OR name = '163' OR name = '161')
AND year = 2023
AND month = 7
AND day = 28;
