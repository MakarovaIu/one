-- In 8.sql, write a SQL query to list the names of all people who starred in Toy Story.
SELECT name
FROM people
WHERE id in (SELECT s.person_id
             FROM stars as s
             WHERE s.movie_id in (SELECT id
                                  FROM movies
                                  WHERE title = "Toy Story"));
-- 300 ms