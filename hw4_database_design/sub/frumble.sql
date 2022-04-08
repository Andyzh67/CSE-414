/*
1. Create a table in the database and load the data from the provided file into that table;
use SQLite or any other relational DBMS of your choosing.
Turn in your create-table statement. The data import statements are optional (you don't
need to include these).
*/

CREATE TABLE FrumbleData (
    name VARCHAR(10),
    discount VARCHAR(3),
    month VARCHAR(3),
    price INT
);

-- .import mrFrumbleData.txt FrumbleData
-- 426 rows






/*
2. Find all non-trivial functional dependencies in the database. This is a reverse
engineering task, so expect to proceed in a trial and error fashion. Search first for the
simple dependencies, say name → discount then try the more complex ones, like name,
discount → month, as needed. To check each functional dependency you have to write a
SQL query.
*/

-- Check name → discount, fails
-- this functional dependency doesn't exist
SELECT *
FROM FrumbleData F1, FrumbleData F2
WHERE F1.name = F2.name AND
      F1.discount <> F2.discount;


-- Check name → price, holds
SELECT *
FROM FrumbleData F1, FrumbleData F2
WHERE F1.name = F2.name AND
      F1.price <> F2.price;

-- name → month also fails, so name + = {name, price}


/*
Then check functional dependency of discount,
result in discount has trivial closure
*/

/*
The same result for price (trivial closure)
*/

/*
Check functional dependency of month,
result in month+ = {month, discount}
*/
SELECT *
FROM FrumbleData F1, FrumbleData F2
WHERE F1.month = F2.month AND
      F1.discount <> F2.discount;


/*
Thus the functional dependencies are:
name → price
month → discount
{name, month} → {price, discount}
*/





/* 
3. Decompose the table into Boyce-Codd Normal Form (BCNF), and create SQL tables for
the decomposed schema. Create keys and foreign keys where appropriate.
For this question turn in the SQL commands for creating the tables.

Suppose we have R(name, discount, month, price).
Since name → price, we break R into R1(name, price), R2(name, discount, month).
R1 is in BCNF.
Since month → discount, we break R2 into R3(month, discount), R4(month, name).
Then R3 and R4 are both in BCNF.
Thus the decomposition gives us R1(name, price), R3(month, discount), R4(month, name).

name is the (super)key in R1, month is the (super)key in R3, the combination of month and
name is the (super)key in R4.
*/

CREATE TABLE R1(
    name VARCHAR(10) PRIMARY KEY,
    price INT
);

CREATE TABLE R3(
    month VARCHAR(3) PRIMARY KEY,
    discount VARCHAR(3)
);

CREATE TABLE R4(
    name VARCHAR(10) REFERENCES R1(name),
    month VARCHAR(3) REFERENCES R3(month),
    PRIMARY KEY (name, month)
);




/*
4. Here, turn in the SQL queries that load the new tables, and count the size of the tables
after loading them (obtained by running SELECT COUNT(*) FROM Table).
*/

INSERT INTO R1
SELECT DISTINCT name, price
FROM FrumbleData;

-- R1 has 36 rows
SELECT COUNT(*)
FROM R1;



INSERT INTO R3
SELECT DISTINCT month, discount
FROM FrumbleData;

-- R3 has 12 rows
SELECT COUNT(*)
FROM R3;



INSERT INTO R4
SELECT DISTINCT name, month
FROM FrumbleData;

-- R4 has 426 rows
SELECT COUNT(*)
FROM R4;

