drop table if exists transaction_shred;
create table transaction_shred (
  c_custkey bigint,
  c_phone varchar(20),
  c_acctbal decimal(18,2),
  c_orders super  
);

COPY transaction_shred
FROM 's3://redshift-downloads/semistructured/tpch-nested/data/json/customer_orders_lineitem/customer_order_lineitem.json'
IAM_ROLE 'arn:aws:iam::357171621133:role/ETLlambdaAccessRole'
REGION 'us-east-1'
JSON 'auto ignorecase';


SELECT c_custkey, c_phone, c_acctbal, o.o_orderstatus::varchar, l.l_shipmode::varchar, l.l_extendedprice::decimal(18,2)
from transaction_shred t, t.c_orders o, o.o_lineitems l;

INSERT INTO transaction_shred VALUES
  (1234,
   '800-867-5309',
   441989.88,
   JSON_PARSE(  
    '[{
      "o_orderstatus":"F",
      "o_clerk":"Clerk#0000001991",
      "o_lineitems":[
         {
            "l_returnflag":"R",
            "l_receiptdate":"2017-07-23",
            "l_tax":0.03,
            "l_shipmode":"TRUCK",
            "l_suppkey":4799,
            "l_shipdate":"2014-06-24",
            "l_commitdate":"2014-06-05",
            "l_partkey":54798,
            "l_quantity":4,
            "l_linestatus":"F",
            "l_comment":"Net new order for new customer",
            "l_extendedprice":28007.64,
            "l_linenumber":1,
            "l_discount":0.02,
            "l_shipinstruct":"TAKE BACK RETURN"
         }
      ],
      "o_orderdate":"2014-06-01",
      "o_shippriority":0,
      "o_totalprice":28308.25,
      "o_orderkey":1953697,
      "o_comment":"wing for 997.1 gt3",
      "o_orderpriority":"5-LOW"
    }],'));

INSERT INTO transaction_shred VALUES
  (1234,
   '800-867-5309',
   441989.88,
   JSON_PARSE(  '[{
      "o_orderstatus":"F",
      "o_clerk":"Clerk#0000001991",
      "o_lineitems":[
         {
            "l_returnflag":"R",
            "l_receiptdate":"2017-07-23",
            "l_tax":0.03,
            "l_shipmode":"TRUCK",
            "l_suppkey":4799,
            "l_shipdate":"2014-06-24",
            "l_commitdate":"2014-06-05",
            "l_partkey":54798,
            "l_quantity":4,
            "l_linestatus":"F",
            "l_comment":"Net new order for new customer",
            "l_extendedprice":28007.64,
            "l_linenumber":1,
            "l_discount":0.02,
            "l_shipinstruct":"TAKE BACK RETURN"
         }
      ],
      "o_orderdate":"2014-06-01",
      "o_shippriority":0,
      "o_totalprice":28308.25,
      "o_orderkey":1953697,
      "o_comment":"wing for 997.1 gt3",
      "o_orderpriority":"5-LOW"
   }]'));


update transaction_shred
set c_orders =  
   JSON_PARSE(  '[{
      "o_orderstatus":"F",
      "o_clerk":"Clerk#0000001991",
      "o_lineitems":[
         {
            "l_returnflag":"R",
            "l_receiptdate":"2017-07-23",
            "l_tax":0.03,
            "l_shipmode":"TRUCK",
            "l_suppkey":4799,
            "l_shipdate":"2014-06-24",
            "l_commitdate":"2014-06-05",
            "l_partkey":54798,
            "l_quantity":4,
            "l_linestatus":"F",
            "l_comment":"Net new order for new customer",
            "l_extendedprice":28007.64,
            "l_linenumber":1,
            "l_discount":0.02,
            "l_shipinstruct":"TAKE BACK RETURN"
         },
         {
            "l_returnflag":"R",
            "l_receiptdate":"2017-07-23",
            "l_tax":0.03,
            "l_shipmode":"TRUCK",
            "l_suppkey":4799,
            "l_shipdate":"2014-06-24",
            "l_commitdate":"2014-06-05",
            "l_partkey":54798,
            "l_quantity":4,
            "l_linestatus":"F",
            "l_comment":"Net new order2 for new customer",
            "l_extendedprice":28007.64,
            "l_linenumber":2,
            "l_discount":0.02,
            "l_shipinstruct":"TAKE BACK RETURN"
         }
      ],
      "o_orderdate":"2014-06-01",
      "o_shippriority":0,
      "o_totalprice":28308.25,
      "o_orderkey":1953697,
      "o_comment":"wing for 997.1 gt3",
      "o_orderpriority":"5-LOW"
   }]')
   where c_custkey = 1234;

SELECT c_custkey, c_phone, c_acctbal, o.o_orderstatus::varchar, l.l_shipmode::varchar, l.l_extendedprice::decimal(18,2), l.l_linenumber::int
FROM transaction_shred t, t.c_orders o, o.o_lineitems l
order by c_custkey;