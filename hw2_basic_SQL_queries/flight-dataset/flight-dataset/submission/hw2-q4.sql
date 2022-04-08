-- output row number is 12

SELECT DISTINCT C.name AS name

FROM FLIGHTS AS F, CARRIERS AS C
WHERE F.carrier_id = C.cid
GROUP BY F.month_id, F.day_of_month, C.name
HAVING COUNT(*) > 1000;