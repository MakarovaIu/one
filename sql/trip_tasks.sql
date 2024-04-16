-- Вывести из таблицы trip информацию о командировках тех сотрудников, фамилия которых заканчивается на букву «а»,
-- в отсортированном по убыванию даты последнего дня командировки виде.
-- В результат включить столбцы name, city, per_diem, date_first, date_last.
select name, city, per_diem, date_first, date_last
from trip
where name like "%а %.%"
order by date_last desc;

-- Вывести в алфавитном порядке фамилии и инициалы тех сотрудников, которые были в командировке в Москве.
select distinct name
from trip
where city = "Москва"
order by name;

-- Для каждого города посчитать, сколько раз сотрудники в нем были.
-- Информацию вывести в отсортированном в алфавитном порядке по названию городов.
-- Вычисляемый столбец назвать Количество.
select city, count(*) as 'Количество'
from trip
group by city
order by city;

-- Вывести два города, в которых чаще всего были в командировках сотрудники. Вычисляемый столбец назвать Количество.
select city, count(*) as 'Количество'
from trip
group by city
order by Количество desc
limit 2;

-- Вывести информацию о командировках во все города кроме Москвы и Санкт-Петербурга (фамилии и инициалы сотрудников,
-- город, длительность командировки в днях, при этом первый и последний день относится к периоду командировки).
-- Последний столбец назвать Длительность. Информацию вывести в упорядоченном по убыванию длительности поездки,
-- а потом по убыванию названий городов (в обратном алфавитном порядке).
select name, city, cast(julianday(date_last)-julianday(date_first) as integer)+1 as Длительность
from trip
where city not in ('Москва', 'Санкт-Петербург')
order by Длительность desc, city desc;
-- MySQL version
-- select name, city, datediff(date_last, date_first)+1 as Длительность
-- from trip
-- where city not in ('Москва', 'Санкт-Петербург')
-- order by Длительность desc, city desc;

-- Вывести информацию о командировках сотрудника(ов), которые были самыми короткими по времени.
-- В результат включить столбцы name, city, date_first, date_last.
select name, city, date_first, date_last
from trip
where cast(julianday(date_last)-julianday(date_first) as integer) in (
    select min(cast(julianday(date_last)-julianday(date_first) as integer))
    from trip
);
-- MySQL version
-- select name, city, date_first, date_last
-- from trip
-- where datediff(date_last, date_first) in (
--     select min(datediff(date_last, date_first)) from trip);


-- Вывести информацию о командировках, начало и конец которых относятся к одному месяцу (год может быть любой).
-- В результат включить столбцы name, city, date_first, date_last. Строки отсортировать сначала
-- в алфавитном порядке по названию города, а затем по фамилии сотрудника.
select name, city, date_first, date_last
from trip
where strftime('%m', date_last) = strftime('%m', date_first)
order by city, name;
-- MySQL version
-- select name, city, date_first, date_last
-- from trip
-- where month(date_last) = month(date_first)
-- order by city, name;

-- Вывести название месяца и количество командировок для каждого месяца.
-- Считаем, что командировка относится к некоторому месяцу, если она началась в этом месяце.
-- Информацию вывести сначала в отсортированном по убыванию количества,
-- а потом в алфавитном порядке по названию месяца виде. Название столбцов – Месяц и Количество.
select case strftime('%m', date_first) when '01' then 'January'
    when '02' then 'February' when '03' then 'March' when '04' then 'April' when '05' then 'May' when '06' then 'June'
    when '07' then 'July' when '08' then 'August' when '09' then 'September' when '10' then 'October'
    when '11' then 'November' when '12' then 'December' else '' end
    as month, count(*) as amount
from trip
group by month
order by amount desc, month;
-- MySQL version
-- select MONTHNAME(date_first) as Месяц, count(*) as Количество
-- from trip
-- group by Месяц
-- order by Количество desc, Месяц;

-- Вывести сумму суточных (произведение количества дней командировки и размера суточных) для командировок,
-- первый день которых пришелся на февраль или март 2020 года. Значение суточных для каждой командировки занесено
-- в столбец per_diem. Вывести фамилию и инициалы сотрудника, город, первый день командировки и сумму суточных.
-- Последний столбец назвать Сумма. Информацию отсортировать сначала  в алфавитном порядке по фамилиям сотрудников,
-- а затем по убыванию суммы суточных.
select name, city, date_first, per_diem * (cast(julianday(date_last)-julianday(date_first) as integer)+1) as Сумма
from trip
where date_first BETWEEN '2020-02-01' AND '2020-03-31'
order by name, Сумма desc;
-- MySQL version
-- select name, city, date_first, per_diem * (datediff(date_last, date_first)+1) as Сумма
-- from trip
-- where date_first BETWEEN '2020-02-01' AND '2020-03-31'
-- order by name, Сумма desc;

-- Вывести фамилию с инициалами и общую сумму суточных, полученных за все командировки для тех сотрудников, которые были
-- в командировках больше чем 3 раза, в отсортированном по убыванию сумм суточных виде. Последний столбец назвать Сумма.
select name, sum(per_diem * (cast(julianday(date_last)-julianday(date_first) as integer)+1)) as Сумма
from trip
group by name
having count(*) > 3
order by Сумма desc;
-- MySQL version
-- select name, sum(per_diem * (datediff(date_last, date_first)+1)) as Сумма
-- from trip
-- group by name
-- having count(*) > 3
-- order by Сумма desc;