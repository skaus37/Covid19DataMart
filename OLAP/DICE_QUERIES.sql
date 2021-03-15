 --number of fatal cases for November and December in Peel and Ottawa
 select L.phu_name, count(*) from data_mart.fact_table F, data_mart.patient_dimension P, data_mart.reported_date_dimension D, data_mart.phu_location_dimension L where F.reported_date_key=D.reported_date_key and F.patient_key=P.patient_key and F.phu_location_key=L.phu_location_key and F.is_fatal=true and D.month in ('November','December') and L.city in ('Mississauga','Ottawa') GROUP BY (L.phu_name);


 --