--Step 1 in the blog lands the data files in an Amazon S3 location
--Step 2 registers the data files as two different tables in the AWS Glue database, rs-dimension-blog

--Step 3. Create external schema in Redshift pointing to the Glue database, rs-dimension-blog
--Replace placeholders <account-id> and <redshift-spectrum-role-name> appropriately
create external schema spectrum_dim_blog
from data catalog 
database 'rs-dimension-blog' 
iam_role 'arn:aws:iam::<account-id>:role/<redshift-spectrum-role-name>';

--Step 4. Create table-views (1:1) to read latest version of records
--This is to check if you are able to access existing cataloged tables in S3
select * from spectrum_dim_blog.customer_master limit 10;
select * from spectrum_dim_blog.customer_address limit 10;

create schema rs_dim_blog;

--Create one view each on top of customer_master and customer_address to fetch the latest
--version of record for each customer_id using the row_number window function
--Create view to access latest records of customer_master
create or replace view rs_dim_blog.vw_cust_mstr_latest as
with rows_numbered as
(
  select customer_id, first_name, last_name, employer_name, row_audit_ts,
  row_number() over(partition by customer_id order by row_audit_ts desc) as rnum
  from spectrum_dim_blog.customer_master
)
select customer_id, first_name, last_name, employer_name, row_audit_ts, rnum
from rows_numbered
where rnum = 1
with no schema binding;

--Create view to access latest records of customer_address
create or replace view rs_dim_blog.vw_cust_addr_latest as
with rows_numbered as
(
  select customer_id, email_id, city, country, row_audit_ts,
  row_number() over(partition by customer_id order by row_audit_ts desc) as rnum
  from spectrum_dim_blog.customer_address
)
select customer_id, email_id, city, country, row_audit_ts, rnum
from rows_numbered
where rnum = 1
with no schema binding;

select * from rs_dim_blog.vw_cust_mstr_latest order by customer_id;
select * from rs_dim_blog.vw_cust_addr_latest order by customer_id;

--Step 5. Create target (dimension) table and dimension-specific views joining table-views from step#4; 
--Populate all data from dimension-specific-view to dimension table to complete initial load.

--drop if exists
drop table rs_dim_blog.dim_customer;

--create the target dim_customer table
CREATE TABLE rs_dim_blog.dim_customer (
    customer_sk bigint ENCODE az64,
    customer_id bigint ENCODE az64,
    first_name character varying(100) ENCODE lzo,
    last_name character varying(100) ENCODE lzo,
    employer_name character varying(100) ENCODE lzo,
    email_id character varying(100) ENCODE lzo,
    city character varying(100) ENCODE lzo,
    country character varying(100) ENCODE lzo,
    rec_eff_dt date ENCODE az64,
    rec_exp_dt date ENCODE az64
)
DISTSTYLE AUTO;	

--Step 6. Create view to extract columns to be included in dim_customer fetching them by joining 
--the latest source-table views that were created above.
create or replace view rs_dim_blog.vw_dim_customer_src as
select m.customer_id, m.first_name, m.last_name, m.employer_name, a.email_id, a.city, a.country
from rs_dim_blog.vw_cust_mstr_latest as m
left join rs_dim_blog.vw_cust_addr_latest as a on m.customer_id = a.customer_id
order by m.customer_id
with no schema binding;

--This query should list all customer_ids that were provided in the initial data files
select customer_id from rs_dim_blog.vw_dim_customer_src group by 1 having count(1)=1;

--This query should give zero rows as output as the initial data contains only one record per customer_id
select customer_id from rs_dim_blog.vw_dim_customer_src group by 1 having count(1)>1;

--Step 7. Populate dim_customer by querying vw_dim_customer_src
--For auto-generation of primary key column values (customer_sk) use row_number() window function
--This insert statement completes the initial data loading into dim_customer table
insert into rs_dim_blog.dim_customer
(customer_sk, customer_id, first_name, last_name, employer_name, email_id, city, country, rec_eff_dt, rec_exp_dt)
select row_number() over() as customer_sk,
customer_id, first_name, last_name, employer_name, email_id, city, country, cast('2022-07-01' as date) as rec_eff_dt, 
cast('9999-12-31' as date) as rec_exp_dt
from rs_dim_blog.vw_dim_customer_src;

select * from rs_dim_blog.dim_customer order by 1;

--Ensure dim_customer has been populated only with one record per customer_id
--Both counts of the below query should have an identical value
select count(1), count(distinct customer_id) from rs_dim_blog.dim_customer;

select count(1), count(distinct customer_id) from rs_dim_blog.vw_dim_customer_src;

--Step 8. Landing ongoing change data files in S3 location
--Now copy the incremental csv files to the respective directories (customer_master_with_ts_incr.csv, customer_address_with_ts_incr.csv)
--The result of placing the incremental files will be reflected in the below query output against vw_dim_customer_src
--The query against vw_dim_customer_src will show the latest version of records while the dim_customer query will show the initial version
select * from rs_dim_blog.dim_customer order by customer_id;

select * from rs_dim_blog.vw_dim_customer_src order by customer_id;

--Step 9. Create temporary table with same structure as dim_customer
CREATE TEMP TABLE temp_dim_customer (
    customer_sk bigint,
    customer_id bigint,
    first_name varchar(100),
    last_name varchar(100),
    employer_name varchar(100),
    email_id varchar(100),
    city varchar(100),
    country varchar(100),
    rec_eff_dt date,
    rec_exp_dt date,
    iud_operation character(1)
);

select count(1) from temp_dim_customer;

--Step 10. Since we are receiving incremental data from source we will receive only I's, U's
--In case D records are also received, it is expected that there will be a STATUS column with INACTIVE as value
--Which will be treated as U and existing latest record will be expired.
--In case of full refresh, the below query will also retrieve D type records against all PK values
--which are absent in the latest snapshot

--Populate all new inserts and updates to the temp_dim_customer table by using query below
insert into temp_dim_customer (
  customer_sk, customer_id, first_name, last_name, employer_name, email_id, city, country, rec_eff_dt, rec_exp_dt, iud_operation
  )
with 
newt as (
  	select customer_id, 
  			sha2(coalesce(first_name, '') || coalesce(last_name, '') || coalesce(employer_name, '') || coalesce(email_id, '') || coalesce(city, '') || coalesce(country, ''), 512) as hash_value,
  			first_name, last_name, employer_name, 
  			email_id, city, country, 
  		current_date rec_eff_dt, cast('9999-12-31' as date) rec_exp_dt
     from rs_dim_blog.vw_dim_customer_src
  ),
oldt as (
  	select customer_id, 
  			sha2(coalesce(first_name, '') || coalesce(last_name, '') || coalesce(employer_name, '') || coalesce(email_id, '') || coalesce(city, '') || coalesce(country, ''), 512) as hash_value,
  			first_name, last_name, employer_name, email_id, city, country
     from rs_dim_blog.dim_customer
     where rec_exp_dt = '9999-12-31'
  ),
maxsk as (select max(customer_sk) as maxval from rs_dim_blog.dim_customer),
allrecs as (select 
coalesce(oldt.customer_id, newt.customer_id) as customer_id,
case when oldt.customer_id is null then 'I'
when newt.customer_id is null then 'D'
when oldt.hash_value != newt.hash_value then 'U' 
else 'N' end as iud_op, 
newt.first_name, newt.last_name, newt.employer_name, 
newt.email_id, newt.city, newt.country, newt.rec_eff_dt, newt.rec_exp_dt
from oldt full outer join newt
on oldt.customer_id = newt.customer_id)
select (maxval+(row_number() over())) as customer_sk, customer_id, first_name, last_name, employer_name, 
email_id, city, country, rec_eff_dt, rec_exp_dt, iud_op
from allrecs, maxsk
where iud_op != 'N';

select count(1) from temp_dim_customer;

--Step 11. Expire records that have been updated as per the incremental data files
update rs_dim_blog.dim_customer
set rec_exp_dt = current_date-1
where customer_id in (
  select customer_id from temp_dim_customer as t
  where iud_operation in ('U', 'D')
  )
  and rec_exp_dt = '9999-12-31';
  
--Step 12. Insert all records tagged as I and U from temp_dim_customer to the target dim_customer table
insert into rs_dim_blog.dim_customer (
  customer_sk, customer_id, first_name, last_name, employer_name, 
email_id, city, country, rec_eff_dt, rec_exp_dt)
select customer_sk, customer_id, first_name, last_name, employer_name, 
email_id, city, country, rec_eff_dt, rec_exp_dt from temp_dim_customer where iud_operation in ('I', 'U');

commit;

--Check final output by firing below query to see that dim_customer contains initial load as well as incremental load records
select * from rs_dim_blog.dim_customer order by customer_id, customer_sk;
