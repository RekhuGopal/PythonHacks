import boto3
import json
import random
import calendar
import time
from datetime import datetime
import psycopg2
from psycopg2.extras import LogicalReplicationConnection

#my_stream_name = 'Foo'
#kinesis_client = boto3.client('kinesis', region_name='us-east-1')
my_connection  = psycopg2.connect(
                   "dbname='postgres' host='cloudquicklabsdb.clg2kzrollbh.ap-south-1.rds.amazonaws.com' user='postgres' password='PosTgeSqL2321'" ,
                   connection_factory = LogicalReplicationConnection)
cur = my_connection.cursor()
cur.drop_replication_slot('wal2json_test_slot')
cur.create_replication_slot('wal2json_test_slot', output_plugin = 'wal2json')
cur.start_replication(slot_name = 'wal2json_test_slot', options = {'pretty-print' : 1}, decode= True)

def consume(msg):
    #kinesis_client.put_record(StreamName=my_stream_name, Data=json.dumps(msg.payload), PartitionKey="default")
    print (msg.payload)

cur.consume_stream(consume)