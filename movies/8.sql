-- SQL query to list the names of all people who starred in Toy Story.
SELECT p.name
FROM stars s
JOIN people p ON s.person_id = p.id
JOIN movies m ON s.movie_id = m.id
WHERE m.title = 'Toy Story';
