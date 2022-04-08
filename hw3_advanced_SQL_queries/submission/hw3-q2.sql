
SELECT DISTINCT origin_city AS city

FROM FLIGHTS

WHERE canceled = 0
GROUP BY origin_city
HAVING MAX(actual_time) < 180
ORDER BY city;

/*

query returns 109 rows of output

the query takes about 13s


first 20 rows of the result:

city
Aberdeen SD
Abilene TX
Alpena MI
Ashland WV
Augusta GA
Barrow AK
Beaumont/Port Arthur TX
Bemidji MN
Bethel AK
Binghamton NY
Brainerd MN
Bristol/Johnson City/Kingsport TN
Butte MT
Carlsbad CA
Casper WY
Cedar City UT
Chico CA
College Station/Bryan TX
Columbia MO
Columbus GA

*/
