PostgreSQL Notes 
1. What is PostgreSQL?

PostgreSQL is an open-source relational database management system (RDBMS) used to store, manage, and retrieve data efficiently.

In simple words, it is a place where applications store structured data so it can be accessed later.

Examples of data stored in PostgreSQL:

user accounts
product information
job applications
transaction records

Many large companies use PostgreSQL because it is reliable, scalable, and secure.

2. Database Concepts

Before using PostgreSQL, it helps to understand a few basic terms.

Database
A container that holds multiple tables.

Table
A structure that stores data in rows and columns.

Example:

| id | name | email |
|----|------|-------|
|1|Niveditha|nive@email.com|

Row (Record)
Each individual entry in the table.

Column (Field)
The type of information stored.

3. Creating a Database

To create a database:

CREATE DATABASE internship_db;


Now all tables will be created inside this database.

4. Creating Tables

Tables define the structure of stored data.

Example:

CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    score INT
);

Explanation:

SERIAL → auto-increment ID
PRIMARY KEY → unique identifier
VARCHAR → text data
INT → integer numbers

5. Inserting Data

To add records into a table:

INSERT INTO candidates (name, email, score)
VALUES ('Niveditha', 'nive@email.com', 85);

Insert multiple records:

INSERT INTO candidates (name, email, score)
VALUES
('Rahul','rahul@email.com',78),
('Priya','priya@email.com',92);

6. Retrieving Data (SELECT)

To view data:

SELECT * FROM candidates;

Select specific columns:

SELECT name, score FROM candidates;

Filtering data:

SELECT * FROM candidates
WHERE score > 80;

Sorting results:

SELECT * FROM candidates
ORDER BY score DESC;

7. Updating Data

Modify existing data:

UPDATE candidates
SET score = 88
WHERE name = 'Rahul';
8. Deleting Data

Remove records:

DELETE FROM candidates
WHERE name = 'Priya';

9. Relationships Between Tables

In real applications, data is stored across multiple tables.

Example:

Candidates Table

|id|    |name|
|----||-------|
|1|	  |Niveditha|

Results Table

candidate_id	status
1	            Selected

These tables are connected using foreign keys.

10. JOIN Operations

JOIN combines data from multiple tables.

Example:

SELECT candidates.name, results.status
FROM candidates
JOIN results
ON candidates.id = results.candidate_id;

Result:

name	status
Niveditha	Selected
11. Aggregate Functions

Used to perform calculations.

Count records:

SELECT COUNT(*) FROM candidates;

Average score:

SELECT AVG(score) FROM candidates;

Maximum score:

SELECT MAX(score) FROM candidates;
12. Indexing (Performance Optimization)

Indexes help databases retrieve data faster.

Example:

CREATE INDEX idx_candidate_email
ON candidates(email);

This speeds up searches using the email column.

13. Transactions

Transactions ensure data consistency.

Example:

BEGIN;

UPDATE accounts
SET balance = balance - 100
WHERE id = 1;

UPDATE accounts
SET balance = balance + 100
WHERE id = 2;

COMMIT;

If something fails:

ROLLBACK;