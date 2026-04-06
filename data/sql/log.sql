\connect nasa_neo

CREATE TABLE etl_log(
run_id INT
,step varchar(40)
,status varchar(20)
,row_processed INT
,message varchar
,logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
,primary key(run_id, step)
);