## Create Table
create table demo (
  faceId varchar(100)    not null,
  email  varchar(100)    not null,
  name   varchar(100)    not null,
  phone  varchar(100)    not null,
  title  varchar(100)    not null,
  amount INT             not null
)

## Insert Values
INSERT INTO demo (faceId, email, name, phone, title, amount) VALUES ('face123', 'example@example.com', 'John Doe', '1234567890', 'Manager', 1000)