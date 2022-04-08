
SELECT DISTINCT C.name AS carrier

FROM CARRIERS AS C, FLIGHTS AS F
WHERE F.origin_city = 'Seattle WA' AND
      F.dest_city = 'San Francisco CA' AND
      C.cid = F.carrier_id
ORDER BY carrier;

/*

query returns 4 rows of output

the query takes about 4s


first 20 rows of the result:

carrier
Alaska Airlines Inc.
SkyWest Airlines Inc.
United Air Lines Inc.
Virgin America

*/