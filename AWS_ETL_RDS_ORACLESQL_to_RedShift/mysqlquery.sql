CREATE TABLE employees (
    id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    hire_date DATE NOT NULL,
    salary DECIMAL(10, 2) NOT NULL
);


INSERT INTO employees (id, first_name, last_name, email, hire_date, salary) 
VALUES (1, 'John', 'Doe', 'john.doe@example.com', TO_DATE('2023-01-15', 'YYYY-MM-DD'), 60000.00);

INSERT INTO employees (id, first_name, last_name, email, hire_date, salary) 
VALUES (2, 'Joh', 'Don', 'john.doe1@example.com', TO_DATE('2023-01-15', 'YYYY-MM-DD'), 90000.00);

