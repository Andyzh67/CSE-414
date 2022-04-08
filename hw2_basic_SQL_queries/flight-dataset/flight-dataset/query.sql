CREATE EXTERNAL DATA SOURCE cse414blob
WITH (TYPE = BLOB_STORAGE, 
LOCATION = 'https://cse344.blob.core.windows.net/cse344-22wi'
);



-- create carrier table
CREATE TABLE CARRIERS (cid varchar(7) PRIMARY KEY,
    name varchar(83)
);


-- create month table
CREATE TABLE MONTHS (mid int PRIMARY KEY,
    month varchar(9)
);


-- create weekday table
CREATE TABLE WEEKDAYS (did int PRIMARY KEY,
    day_of_week varchar(9)
);

CREATE TABLE FLIGHTS (fid int PRIMARY KEY,
    month_id int REFERENCES MONTHS(mid), -- 1-12
    day_of_month int, -- 1-31
    day_of_week_id int REFERENCES WEEKDAYS(did), -- 1-7, 1 = Monday, 2 = Tuesday, etc
    carrier_id varchar(7) REFERENCES CARRIERS(cid),
    flight_num int,
    origin_city varchar(34),
    origin_state varchar(47),
    dest_city varchar(34),
    dest_state varchar(46),
    departure_delay int, -- in mins
    taxi_out int, -- in mins
    arrival_delay int, -- in mins
    canceled int, -- 1 means canceled
    actual_time int, -- in mins
    distance int, -- in miles
    capacity int,
    price int -- in $
);

bulk insert Carriers from 'carriers.csv'
with (ROWTERMINATOR = '0x0a',
DATA_SOURCE = 'cse414blob', FORMAT='CSV', CODEPAGE = 65001, --UTF-8 encoding
FIRSTROW=1,TABLOCK);

bulk insert Months from 'months.csv'
with (ROWTERMINATOR = '0x0a',
DATA_SOURCE = 'cse414blob', FORMAT='CSV', CODEPAGE = 65001, --UTF-8 encoding
FIRSTROW=1,TABLOCK);

bulk insert Weekdays from 'weekdays.csv'
with (ROWTERMINATOR = '0x0a',
DATA_SOURCE = 'cse414blob', FORMAT='CSV', CODEPAGE = 65001, --UTF-8 encoding
FIRSTROW=1,TABLOCK);

-- Import for the large Flights table
-- This last import might take a little under 10 minutes on the provided server settings

bulk insert Flights from 'flights-small.csv'
with (ROWTERMINATOR = '0x0a',
DATA_SOURCE = 'cse414blob', FORMAT='CSV', CODEPAGE = 65001, --UTF-8 encoding
FIRSTROW=1,TABLOCK);

-- Indexes to make your query run faster (optional, but recommended)
-- This will take about 3-4 minutes

create index Flights_idx1 on Flights(origin_city,dest_city,actual_time);
create index Flights_idx2 on Flights(actual_time);
create index Flights_idx3 on Flights(dest_city,origin_city,actual_time);
