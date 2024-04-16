-- In 9.sql, write a SQL query to list the names of all people who starred in a movie released in 2004,
-- ordered by birth year.
SELECT name
FROM people
WHERE id in (SELECT s.person_id
             FROM stars s
             WHERE movie_id in (SELECT id
                                FROM movies
                                WHERE year = 2004))
GROUP BY id
ORDER BY birth;
