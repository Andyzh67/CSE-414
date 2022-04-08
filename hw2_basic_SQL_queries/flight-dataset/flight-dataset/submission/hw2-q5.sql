-- output row number is 6

SELECT C.name AS name, AVG(F.canceled) * 100 AS percentage

FROM FLIGHTS AS F, CARRIERS AS C
WHERE F.carrier_id = C.cid AND
    F.origin_city = 'Seattle WA'
GROUP BY C.name
HAVING percentage > 0.5
ORDER BY percentage;