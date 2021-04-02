create table completed_log (
	id serial primary key, 
	time float, 
	jobname varchar, 
	last_updated float, 
	len int, 
	status varchar, 
	name varchar, 
	size int, 
	processed boolean, 
	processed_time float
); 

create table current_fleet (
	id serial primary key, 
	bike_id varchar, 
	company_name varchar, 
	start_time float, 
	start_lat float, 
	start_lon float, 
	start_is_reserved boolean, 
	start_is_disabled boolean, 
	start_battery_level float, 
	lat float, 
	lon float, 
	is_reserved boolean, 
	is_disabled boolean, 
	battery_level float, 
	jobname varchar, 
	new boolean, 
	last_updated float
); 

create table removed (
	id serial primary key, 
	bike_id varchar, 
	company_name varchar, 
	start_time float, 
	start_lat float, 
	start_lon float, 
	start_is_reserved boolean, 
	start_is_disabled boolean, 
	start_battery_level float, 
	lat float, 
	lon float, 
	is_reserved boolean, 
	is_disabled boolean, 
	battery_level float, 
	jobname varchar, 
	new boolean, 
	last_updated float
);

