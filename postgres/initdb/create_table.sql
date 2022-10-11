create table logs
(
  id integer,
  name varchar(10),
  status varchar(10), 
  money integer, 
  time TIMESTAMP,
);

create table total
(
  id integer,
  name varchar(10),
  all_money integer,
);