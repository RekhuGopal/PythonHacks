create table workerslist (
  ID varchar(100) not null,
  Name  varchar(100) not null,
  Description varchar(100) not null,
  Email  varchar(100) not null,
  Phone  varchar(100) not null,
  Amount varchar(100) not null,
  colo varchar(100) not null,
  col1  varchar(100) not null,
  col2 varchar(100) not null,
  col3  varchar(100) not null,
  col4  varchar(100) not null,
  col5 varchar(100) not null
)


SELECT *
FROM DataSource2
LEFT JOIN DataSource1 ON  DataSource1.col0 = DataSource2.id

