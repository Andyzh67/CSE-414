
SELECT DISTINCT F.dest_city AS city

FROM FLIGHTS AS F

WHERE F.dest_city NOT IN (SELECT DISTINCT dest_city
                          FROM FLIGHTS
                          WHERE origin_city = 'Seattle WA') AND
      F.dest_city NOT IN (SELECT DISTINCT F2.dest_city
                          FROM FLIGHTS AS F1, FLIGHTS AS F2
                          WHERE F1.origin_city = 'Seattle WA' AND
                          F1.dest_city = F2.origin_city)
ORDER BY city;

/*

query returns 3 rows of output

the query takes about 15s


first 20 rows of the result:

city
Devils Lake ND
Hattiesburg/Laurel MS
St. Augustine FL

*/