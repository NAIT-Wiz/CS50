--SQL query to determine the average rating of all movies released in 2012
SELECT AVG(r.rating) AS average_rating
FROM movies m
JOIN ratings r ON m.id = r.movie_id
WHERE m.year = 2012;
