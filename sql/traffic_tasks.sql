show databases;
use traffic;
show tables;

-- In order not to change the initial table we can create a view
drop view if exists traffic.temp_fine;
create view temp_fine as select * from fine;
select * from temp_fine;
drop view temp_fine;

-- to roll back to initial table
truncate table fine;
INSERT INTO fine(name, number_plate, violation, sum_fine, date_violation, date_payment)
VALUES ('Баранов П.Е.', 'Р523ВТ', 'Превышение скорости(от 40 до 60)', 500.00, '2020-01-12', '2020-01-17'),
       ('Абрамова К.А.', 'О111АВ', 'Проезд на запрещающий сигнал', 1000.00, '2020-01-14', '2020-02-27'),
       ('Яковлев Г.Р.', 'Т330ТТ', 'Превышение скорости(от 20 до 40)', 500.00, '2020-01-23', '2020-02-23'),
       ('Яковлев Г.Р.', 'М701АА', 'Превышение скорости(от 20 до 40)', NULL, '2020-01-12', NULL),
       ('Колесов С.П.', 'К892АХ', 'Превышение скорости(от 20 до 40)', NULL, '2020-02-01', NULL),
       ('Баранов П.Е.', 'Р523ВТ', 'Превышение скорости(от 40 до 60)', NULL, '2020-02-14', NULL),
       ('Абрамова К.А.', 'О111АВ', 'Проезд на запрещающий сигнал', NULL, '2020-02-23', NULL),
       ('Яковлев Г.Р.', 'Т330ТТ', 'Проезд на запрещающий сигнал', NULL, '2020-03-03', NULL);
select * from fine;

create table if not exists payment
(
    payment_id	int primary key auto_increment,
    name varchar(30),
    number_plate varchar(6),
    violation varchar(50),
    date_violation date,
    date_payment date
);

insert into payment(name, number_plate, violation, date_violation, date_payment)
values ('Яковлев Г.Р.',	'М701АА', 'Превышение скорости(от 20 до 40)', '2020-01-12', '2020-01-22'),
       ('Баранов П.Е.', 'Р523ВТ', 'Превышение скорости(от 40 до 60)', '2020-02-14', '2020-03-06'),
       ('Яковлев Г.Р.',	'Т330ТТ', 'Проезд на запрещающий сигнал', '2020-03-03', '2020-03-23');
select * from payment;

-- Для тех, кто уже оплатил штраф, вывести информацию о том, изменялась ли стандартная сумма штрафа.
SELECT  f.name, f.number_plate, f.violation,
   if(
    f.sum_fine = tv.sum_fine, "Стандартная сумма штрафа",
    if(
      f.sum_fine < tv.sum_fine, "Уменьшенная сумма штрафа", "Увеличенная сумма штрафа"
    )
  ) AS description
FROM  fine f, traffic_violation tv
WHERE tv.violation = f.violation and f.sum_fine IS NOT Null;

-- Занести в таблицу fine суммы штрафов, которые должен оплатить водитель, в соответствии с данными
-- из таблицы traffic_violation. При этом суммы заносить только в пустые поля столбца sum_fine.
update fine f, traffic_violation v
set f.sum_fine = v.sum_fine
where f.violation = v.violation and f.sum_fine is null;

-- Вывести фамилию, номер машины и нарушение только для тех водителей, которые на одной машине нарушили одно
-- и то же правило два и более раз. При этом учитывать все нарушения, независимо от того оплачены они или нет.
-- Информацию отсортировать в алфавитном порядке, сначала по фамилии водителя, потом по номеру машины и по нарушению.
select name, number_plate, violation
from fine
group by name, number_plate, violation
having count(*) >= 2
order by name, number_plate, violation;

-- В таблице fine увеличить в два раза сумму неоплаченных штрафов для отобранных на предыдущем шаге записей.
update fine f, (select name, number_plate, violation
    from fine
    group by name, number_plate, violation
    having count(*) >= 2) v
set sum_fine = sum_fine * 2
where date_payment is null and f.name=v.name and f.number_plate=v.number_plate and f.violation=v.violation;
select * from fine;

-- Водители оплачивают свои штрафы. В таблице payment занесены даты их оплаты. Необходимо в таблицу fine занести
-- дату оплаты соответствующего штрафа из таблицы payment; уменьшить начисленный штраф в таблице fine в два раза
-- (только для тех штрафов, информация о которых занесена в таблицу payment),
-- если оплата произведена не позднее 20 дней со дня нарушения.
update fine f, payment p
set f.sum_fine = if(datediff(p.date_payment, p.date_violation) <= 20,
    f.sum_fine / 2, f.sum_fine),
    f.date_payment = p.date_payment
where f.date_payment IS NULL and
      (f.name, f.number_plate, f.violation, f.date_violation) = (p.name, p.number_plate, p.violation, p.date_violation);

-- Создать новую таблицу back_payment, куда внести информацию о неоплаченных штрафах
-- (Фамилию и инициалы водителя, номер машины, нарушение, сумму штрафа  и  дату нарушения) из таблицы fine.
create table if not exists back_payment as
    select name, number_plate, violation, sum_fine, date_violation
        from fine
        where date_payment is null;
select * from back_payment;

-- Удалить из таблицы fine информацию о нарушениях, совершенных раньше 1 февраля 2020 года.
delete from temp_fine
where date_violation < '2020-02-01';
select * from temp_fine;
drop view temp_fine;

select *
from fine, payment;