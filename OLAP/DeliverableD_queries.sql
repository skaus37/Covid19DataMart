-- Part 1: Standard OLAP operations
--Drill down and roll up 
--total number of positive cases in the data mart; drill down to a month (--December 2020), and drill down to a specific day (15th).
select count(*), D.month, D.day
from data_mart.fact_table as F, data_mart.onset_date_dimension as D
where F.onset_date_key = D.onset_date_key
and D.month = 'December'
and D.day = 15
group by (D.month,  D.day);

--ii.  all resolved cases for individual days, roll up to months, roll up to all
select D.day, D.month, count (*)
from data_mart.fact_table as F, data_mart.onset_date_dimension as D
where D.onset_date_key = F.onset_date_key
and F.is_resolved = true
group by rollup (d.day, d.month)
order by D.month, D.day;

--Slice
--The number of cases in a specific PHU (Peel)
SELECT SUM(count_res) FROM (SELECT count(*) as count_res, F.is_resolved, P.phu_name
from data_mart.fact_table as F, data_mart.phu_location_dimension as P
where F.phu_location_key = P.phu_location_key
and P.phu_name = 'Peel Public Health'
group by (P.phu_name,F.is_resolved) )as goo;


--The mobility levels in Ottawa
select M.subregion, avg(M.retail_and_recreation_percentage), 
avg(M.grocery_and_pharmacy_percentage), avg(M.parks_percentage), 
avg(M.transit_stations_percentage), avg(M.workplaces_percentage), 
avg(M.residential_percentage)
from  data_mart.mobility_dimension as M
where M.subregion = 'Ottawa Division' and M.retail_and_recreation_percentage IS NOT NULL 
and M.grocery_and_pharmacy_percentage IS NOT NULL and M.parks_percentage IS NOT NULL 
and M.transit_stations_percentage IS NOT NULL and M.workplaces_percentage IS NOT NULL
and M.residential_percentage IS NOT NULL
group by (M.subregion);
--Dice 
--number of fatal cases for November and December in Mississauga and Ottawa
select L.phu_name, D.month, count(*) as "Fatal Cases" 
from data_mart.fact_table F, data_mart.reported_date_dimension D, data_mart.phu_location_dimension L 
where F.reported_date_key=D.reported_date_key and F.phu_location_key=L.phu_location_key and F.is_fatal=true and D.month in ('November','December') and L.city in ('Mississauga','Ottawa') 
GROUP BY (L.phu_name,D.month);

--number of fatal cases when contrasting two mobility locations, e.g., parks and transit, in mississauga and ottawa
Select L.city, avg(M.parks_percentage) as parks, avg(M.grocery_and_pharmacy_percentage) as grocery, D.month, count(F.is_fatal) as "Fatal Cases"
From data_mart.fact_table F, data_mart.mobility_dimension M, data_mart.reported_date_dimension D, data_mart.phu_location_dimension L
Where F.is_fatal=true and F.reported_date_key=D.reported_date_key and F.phu_location_key=L.phu_location_key and F.mobility_key=M.mobility_key and ((M.grocery_and_pharmacy_percentage>0)or(M.parks_percentage > 0)) and L.city in ('Mississauga','Newmarket')
GROUP BY  D.month, L.city;

--Combining OLAP operations 
--Number of cases when certain measures are in place (peel and control)
SELECT SUM(count_res) FROM (SELECT count(*) as count_res, F.is_resolved, P.phu_name
from data_mart.fact_table as F, data_mart.phu_location_dimension as P, data_mart.special_measures_dimension as S
where F.phu_location_key = P.phu_location_key and F.special_measures_key = S.special_measures_key 
and P.phu_name = 'Peel Public Health' and S.status = 'Control' and S.region = 'peel'
group by (P.phu_name,F.is_resolved) )as goo;

--number of resolved cases i) during different periods of the year, by phu city --drill down for each day
SELECT D.day, D.month, L.city, count(F.is_resolved)
FROM data_mart.fact_table F, data_mart.reported_date_dimension D, data_mart.phu_location_dimension L 
WHERE F.reported_date_key=D.reported_date_key and F.phu_location_key=L.phu_location_key and F.is_resolved=true 
GROUP BY (F.is_resolved,L.city,D.month,D.day,D.number_of_month)
ORDER BY (D.number_of_month,D.day) asc;

--number of resolved cases for each city comparing sunny vs rainy days 
select PHU.city, count(case when W.rain_amount < 1 then 1 else null end) as Sunny,
count(case when W.rain_amount > 1 then 1 else null end) as Rainy
from data_mart.fact_table as F, data_mart.weather_dimension as W, data_mart.phu_location_dimension as PHU
where F.weather_key = W.weather_key
and F.phu_location_key = PHU.phu_location_key
and F.is_resolved = true
group by (PHU.city);




--Part 2. Explorative operation – 3 queries 
--ICEBERG
--find the five days with the highest numbers of resolved outcomes
SELECT D.month,D.day, COUNT(F.is_resolved)
FROM data_mart.fact_table F, data_mart.reported_date_dimension D
WHERE F.reported_date_key=D.reported_date_key
GROUP BY (D.month,D.day)
ORDER BY COUNT(F.is_resolved) desc
LIMIT 5;

--Windowing Query
--ranking of the PHUs in terms of the number of cases per month
SELECT P.phu_name, D.month, count(*),
rank() OVER (partition by D.month order by count(*))
from data_mart.fact_table as F, data_mart.onset_date_dimension as D, data_mart.phu_location_dimension as P
where F.onset_date_key = D.onset_date_key
and F.phu_location_key = P.phu_location_key			   
group by (P.phu_name, D.month)
order by count(*) desc;

--iii. Using Window clause
SELECT P.phu_name, R.month, AVG(COUNT(*)) OVER W AS countofcases
FROM data_mart.fact_table AS F, data_mart.phu_location_dimension AS P,
data_mart.reported_date_dimension AS R
WHERE F.reported_date_key = R.reported_date_key
AND P.phu_name = 'Ottawa Public Health'
AND F.phu_location_key = '6'
GROUP BY (F.is_resolved,P.phu_name, R.month)
WINDOW W AS (PARTITION BY P.phu_name
                                    ORDER BY TO_DATE(R.month,'MONTH')
                                    RANGE BETWEEN INTERVAL '1' MONTH PRECEDING
                                    AND INTERVAL '1' MONTH FOLLOWING);
