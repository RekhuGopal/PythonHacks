DROP TABLE if exists transaction;
CREATE TABLE transaction (
	data_json super
);

COPY transaction
FROM 's3://redshift-downloads/semistructured/tpch-nested/data/json/customer_orders_lineitem/customer_order_lineitem.json'
IAM_ROLE 'arn:aws:iam::357171621133:role/ETLlambdaAccessRole'
REGION 'us-east-1'
JSON 'noshred';

SELECT * FROM transaction limit 1;

SELECT count(1) from transaction;

SELECT data_json.c_custkey, data_json.c_phone, data_json.c_acctbal FROM transaction;

SELECT data_json.c_custkey::int, data_json.c_phone::varchar, data_json.c_acctbal::decimal(18,2) FROM transaction;

SELECT COUNT(1) FROM transaction t, t.data_json.c_orders o;

SELECT COUNT(1) FROM transaction t, t.data_json.c_orders o, o.o_lineitems l;

SELECT data_json.c_custkey::int, data_json.c_phone::varchar, data_json.c_acctbal::decimal(18,2), o.o_orderstatus::varchar, l.l_shipmode::varchar, l.l_extendedprice::decimal(18,2)
FROM transaction t, t.data_json.c_orders o, o.o_lineitems l;