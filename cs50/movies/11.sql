-- In 11.sql, write a SQL query to list the titles of the five highest rated movies (in order)
-- that Chadwick Boseman starred in, starting with the highest rated.
SELECT m.title
FROM movies m
         JOIN ratings r on m.id = r.movie_id
WHERE m.id in (SELECT movie_id
               FROM stars
               WHERE person_id in (SELECT id
                                   FROM people
                                   WHERE name = "Chadwick Boseman"))
ORDER BY r.rating DESC
LIMIT 5;
-- 400 ms