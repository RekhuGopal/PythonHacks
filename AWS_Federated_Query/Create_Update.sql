CREATE TABLE EMPLOYEES (
    Id BigINT NOT NULL,
    Name varchar(255),
    City varchar(255),
	  Email varchar(255),
    Designation varchar(255),
	PhoneNumber varchar(255)
);

INSERT INTO EMPLOYEES (Id, Name, City, Email, Designation, PhoneNumber)
VALUES ('10001', 'Tyson', 'NewYark', 'testemail@gmail.com','PO','3432545645');

INSERT INTO EMPLOYEES (Id, Name, City, Email, Designation, PhoneNumber)
VALUES ('10002', 'Tyson2', 'NewYark2', 'testemail2@gmail.com','PO2','3432545642');

INSERT INTO EMPLOYEES (Id, Name, City, Email, Designation, PhoneNumber)
VALUES ('10003', 'Tyson3', 'NewYark3', 'testemail3@gmail.com','PO3','3432545643');

INSERT INTO EMPLOYEES (Id, Name, City, Email, Designation, PhoneNumber)
VALUES ('10004', 'Tyson4', 'NewYark4', 'testemail4@gmail.com','PO4','3432545644');

INSERT INTO EMPLOYEES (Id, Name, City, Email, Designation, PhoneNumber)
VALUES ('10005', 'Tyson5', 'NewYark5', 'testemail5@gmail.com','PO5','3432545645');

INSERT INTO EMPLOYEES (Id, Name, City, Email, Designation, PhoneNumber)
VALUES ('10006', 'Tyson6', 'NewYark6', 'testemail6@gmail.com','PO6','343254566');

INSERT INTO EMPLOYEES (Id, Name, City, Email, Designation, PhoneNumber)
VALUES ('10007', 'Tyson7', 'NewYark7', 'testemail7@gmail.com','PO7','343254567');

SELECT 
    *
FROM 
    "public"."employees"
LEFT JOIN 
     "AwsDataCatalog"."s3database"."s3_databucketsourceside" ON "public"."employees".id = "AwsDataCatalog"."s3database"."s3_databucketsourceside".industryid;
