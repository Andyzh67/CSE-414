-- output row number is 1

SELECT SUM(F.capacity) AS capacity

FROM FLIGHTS AS F, MONTHS as M
WHERE F.month_id = M.mid AND
    M.month = 'July' AND
    F.day_of_month = 10 AND
    ((F.origin_city = 'Seattle WA' AND F.dest_city = 'San Francisco CA') OR 
    (F.origin_city = 'San Francisco CA' AND F.dest_city = 'Seattle WA'));