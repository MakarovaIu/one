-- The TASK
-- The CS50 Duck has been stolen! The town of Fiftyville has called upon you to solve the mystery of the stolen duck.
-- Authorities believe that the thief stole the duck and then, shortly afterwards, took a flight out of town
-- with the help of an accomplice. Your goal is to identify:
-- Who the thief is,
-- What city the thief escaped to, and
-- Who the thief’s accomplice is who helped them escape
-- All you know is that the theft took place on July 28, 2021 and that it took place on Humphrey Street.

-- Keep a log of any SQL queries you execute as you solve the mystery.
select description
from crime_scene_reports
where street = "Humphrey Street"
  and year = 2021
  and month = 7
  and day = 28;
-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
-- Interviews were conducted today with three witnesses who were present at the time –
-- each of their interview transcripts mentions the bakery.

select name, transcript
from interviews
where year = 2021
  and month = 7
  and day = 28;
-- Ruth:
-- Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
-- If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot
-- in that time frame.
-- Eugene:
-- I don't know the thief's name, but it was someone I recognized.
-- Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street
-- and saw the thief there withdrawing some money.
-- Raymond:
-- As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
-- In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
-- The thief then asked the person on the other end of the phone to purchase the flight ticket.


-- following Ruth
select name
from people
where license_plate in (select license_plate
                        from bakery_security_logs
                        where activity = "exit"
                          and year = 2021
                          and month = 7
                          and day = 28
                          and hour = 10
                          and minute between 15 and 26)
order by name;
-- list of suspects:
-- Barry, Bruce, Diana, Iman, Kelsey, Luca, Sofia, Vanessa
-- license plates:
-- '5P2BI95', '94KL13X', '6P58WS2', '4328GD8', 'G412CB7', 'L93JTIZ', '322W7JE', '0NTHK55'


-- following Eugene
select activity, hour, minute
from bakery_security_logs
where license_plate in (select license_plate
                        from people
                        where name = "Eugene")
  and year = 2021
  and month = 7
  and day = 28;
-- no record of Eugene arriving to the bakery the day of the crime.

-- all suspect who withdrew money the day of the crime on Leggett Street
select p.name, ba.account_number
from people p
         join bank_accounts ba on p.id = ba.person_id
where ba.account_number in (select account_number
                            from atm_transactions
                            where atm_location = "Leggett Street"
                              and transaction_type = "withdraw"
                              and month = 7
                              and day = 28)
order by name;
-- List of suspects:
-- Benista, Brooke, Bruce, Diana, Iman, Kenny, Luca, Taylor
-- account numbers:
-- 28500762, 28296815, 76054385, 49610011, 16153065, 25506511, 81061156, 26013199

-- people who withdrew money on crime day on Leggett street and people who left bakery parking in the morning
select name
from people
where id in (select person_id
             from bank_accounts
             where account_number in (select account_number
                                      from atm_transactions
                                      where atm_location = "Leggett Street"
                                        and transaction_type = "withdraw"
                                        and month = 7
                                        and day = 28)
             intersect
             select id
             from people
             where license_plate in
                   (select license_plate
                    from bakery_security_logs
                    where activity = "exit"
                      and year = 2021
                      and month = 7
                      and day = 28
                      and hour = 10
                      and minute between 15 and 26))
order by name;
-- List of suspects:
-- Bruce, Diana, Iman, Luca
-- list of suspects, id:
-- 396669, 449774, 467400, 514354, 686048


-- following Raymond
-- find all people who:
-- made made a call the day of the crime, 7.28
-- withdrew money on Leggett Street on 7.28
-- left the bakery between 10:15am and 10:26am
select name
from people
where id in (select id
             from people
             where phone_number in (select caller
                                    from phone_calls
                                    where month = 7
                                      and day = 28)
               and id in (select person_id
                          from bank_accounts
                          where account_number in (select account_number
                                                   from atm_transactions
                                                   where atm_location = "Leggett Street"
                                                     and transaction_type = "withdraw"
                                                     and month = 7
                                                     and day = 28)
                          intersect
                          select id
                          from people
                          where license_plate in
                                (select license_plate
                                 from bakery_security_logs
                                 where activity = "exit"
                                   and year = 2021
                                   and month = 7
                                   and day = 28
                                   and hour = 10
                                   and minute between 15 and 26)))
order by name;
-- List of suspects:
-- Bruce, Diana
-- 514354, 686048


-- suspects who took a flight on a first flight from fiftyville on 7.29
select name
from people
where passport_number in (select passport_number
                          from passengers
                          where flight_id in (select id
                                              from flights
                                              where day = 29
                                                and origin_airport_id in (select id from airports where city = "Fiftyville")
                                              order by hour
                                              limit 1)
                            and passport_number in
                                (select passport_number from people where name in ("Bruce", "Diana")));
-- Bruce

-- where the thief escaped to
select city
from airports
where id in (select destination_airport_id
             from flights
             where day = 29
               and origin_airport_id in (select id from airports where city = "Fiftyville")
             order by hour
             limit 1);
-- New York City

-- the accomplice
select name
from people
where phone_number in (select receiver
                       from phone_calls
                       where caller in (select phone_number from people where name = "Bruce")
                         and day = 28
                         and duration < 60);
-- Robin