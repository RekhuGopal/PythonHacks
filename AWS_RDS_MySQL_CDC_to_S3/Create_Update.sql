create table TestDemo.dspostgresqlcdc (
  industry_name_anzsic varchar(100)    not null,
  rme_size_grp     	   varchar(100)    not null,
  variables        	   varchar(100)    not null
)

INSERT INTO TestDemo.dspostgresqlcdc (industry_name_anzsic, rme_size_grp, variables)
VALUES ('value1', 'value2', 'value3');

INSERT INTO dspostgresqlcdc2 (industry_name_anzsic, rme_size_grp, variables)
VALUES ('value1', 'value2', 'value3');

INSERT INTO dspostgresqlcdc3 (industry_name_anzsic, rme_size_grp, variables)
VALUES ('value1', 'value2', 'value3');

CREATE TABLE EMPLOYEES (
    Id varchar(255),
    Name varchar(255),
    City varchar(255),
	Email varchar(255),
    Designation varchar(255),
	PhoneNumber varchar(255)
);

INSERT INTO EMPLOYEES (Id, Name, City, Email, Designation, PhoneNumber)
VALUES ('12414', 'Tyson', 'NewYark', 'testemail@gmail.com','PO','3432545645');

