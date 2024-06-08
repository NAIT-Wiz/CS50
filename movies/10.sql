--write a SQL query to list the names of all people who have directed a movie that received a rating of at least 9.0
SELECT DISTINCT p.name
FROM directors d
JOIN movies m ON d.movie_id = m.id
JOIN ratings r ON m.id = r.movie_id
JOIN people p ON d.person_id = p.id
WHERE r.rating >= 9.0;
