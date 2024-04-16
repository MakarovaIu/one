-- In 13.sql, write a SQL query to list the names of all people who starred in a movie
-- in which Kevin Bacon also starred.
-- Be sure to only select the Kevin Bacon born in 1958.
SELECT name
FROM people
WHERE name IS NOT "Kevin Bacon"
  AND id in
      (SELECT person_id
       FROM stars
       WHERE movie_id in (SELECT movie_id
                          FROM stars
                          WHERE person_id in (SELECT id
                                              FROM people
                                              WHERE name = "Kevin Bacon"
                                                AND birth = 1958)))
GROUP BY id;
-- 500 ms