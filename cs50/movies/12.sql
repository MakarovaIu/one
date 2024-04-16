-- In 12.sql, write a SQL query to list the titles of all movies
-- in which both Johnny Depp and Helena Bonham Carter starred.
SELECT title
FROM movies
WHERE id in (SELECT movie_id
             FROM stars
             WHERE person_id in (SELECT id
                                 FROM people
                                 WHERE name = "Johnny Depp"))
  AND id in
      (SELECT movie_id
       FROM stars
       WHERE person_id in (SELECT id
                           FROM people
                           WHERE name = "Helena Bonham Carter"))
GROUP BY title;
-- 500 ms