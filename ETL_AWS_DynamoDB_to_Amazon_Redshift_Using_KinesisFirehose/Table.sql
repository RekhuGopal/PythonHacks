CREATE TABLE Order (
    order_id varchar(255),
    product_id varchar(255),
    customer_id varchar(255),
	product varchar(255),
    state_name varchar(255),
	amount varchar,
	currency varchar(255),
	timestamp  varchar(255),
	transaction_date varchar(255)
);


 CREATE TABLE Person(
  PersonID int,
  LastName varchar(255),
  FirstName varchar(255),
  Address varchar(255),
  City varchar(255) 
);

INSERT INTO [dbo].[Persons] (PersonID, LastName, FirstName, Address_a, City)
VALUES ('1001', 'Erichsen', 'Skagen', '4006,Church Street', 'NY');