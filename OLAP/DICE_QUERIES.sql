 --number of fatal cases for November and December in Peel(Mississauga) and Ottawa
select L.phu_name, D.month, count(*) as "Fatal Cases" 
from data_mart.fact_table F, data_mart.reported_date_dimension D, data_mart.phu_location_dimension L 
where F.reported_date_key=D.reported_date_key and F.phu_location_key=L.phu_location_key and F.is_fatal=true and D.month in ('November','December') and L.city in ('Mississauga','Ottawa') 
GROUP BY (L.phu_name,D.month);

 --number of unresolved cases for rainy and snowy days in Peel and York
select L.phu_name, count(W) as "Sunny", count(WR) as "Rainy", count(WSR) as "Rain and Snow", count(*) as "Total"
from data_mart.fact_table as F
INNER JOIN data_mart.phu_location_dimension as L ON L.phu_location_key=F.phu_location_key
FULL OUTER JOIN (select * from data_mart.weather_dimension W where W.snow_amount =0 and W.rain_amount=0) as W ON W.weather_key=F.weather_key
FULL OUTER JOIN (select * from data_mart.weather_dimension W where W.snow_amount =0 and W.rain_amount>0) as WR ON WR.weather_key=F.weather_key
FULL OUTER JOIN (select * from data_mart.weather_dimension W where W.snow_amount >0 and W.rain_amount>0) as WSR ON WSR.weather_key=F.weather_key
WHERE F.is_unresolved=true and L.city in ('Mississauga', 'Newmarket')
GROUP BY (L.phu_name);