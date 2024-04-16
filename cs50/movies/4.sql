-- In 4.sql, write a SQL query to determine the number of movies with an IMDb rating of 10.0.
SELECT count(id)
FROM movies
WHERE id in (
    SELECT movie_id
    FROM ratings
    WHERE rating = 10
    )