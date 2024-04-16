-- In 7.sql, write a SQL query to list all movies released in 2010 and their ratings, in descending order by rating.
-- For movies with the same rating, order them alphabetically by title.
-- Movies that do not have ratings should not be included in the result.
SELECT m.title, r.rating
FROM movies as m
         JOIN ratings as r on m.id = r.movie_id
WHERE year = 2010
ORDER BY rating DESC, title;