
SELECT DISTINCT F.dest_city AS city

FROM FLIGHTS AS F, FLIGHTS AS F1
WHERE F1.origin_city = 'Seattle WA' AND
      F1.dest_city = F.origin_city AND
      F.dest_city <> 'Seattle WA' AND
      F.dest_city NOT IN (SELECT DISTINCT F2.dest_city
                          FROM FLIGHTS AS F2
                          WHERE F2.origin_city = 'Seattle WA')
ORDER BY city;

/*

query returns 256 rows of output

the query takes about 4s


first 20 rows of the result:

city
Aberdeen SD
Abilene TX
Adak Island AK
Aguadilla PR
Akron OH
Albany GA
Albany NY
Alexandria LA
Allentown/Bethlehem/Easton PA
Alpena MI
Amarillo TX
Appleton WI
Arcata/Eureka CA
Asheville NC
Ashland WV
Aspen CO
Atlantic City NJ
Augusta GA
Bakersfield CA
Bangor ME

*/