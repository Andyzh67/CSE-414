
SELECT DISTINCT C.name AS carrier

FROM CARRIERS AS C, (SELECT DISTINCT carrier_id
                     FROM FLIGHTS
                     WHERE origin_city = 'Seattle WA' AND
                           dest_city = 'San Francisco CA') AS F
WHERE C.cid = F.carrier_id
ORDER BY carrier;

/*

query returns 4 rows of output

the query takes about 6s


first 20 rows of the result:

carrier
Alaska Airlines Inc.
SkyWest Airlines Inc.
United Air Lines Inc.
Virgin America

*/