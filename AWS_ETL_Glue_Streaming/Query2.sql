SELECT *
FROM "tickettransactiondatabase"."parquet_tickettransactionstreamingdata" 
WHERE ingest_year='2023'
AND cast(ingest_year as bigint)=year(now())
AND cast(ingest_month as bigint)=month(now())
AND cast(ingest_day as bigint)=day_of_month(now())
AND cast(ingest_hour as bigint)=hour(now())
AND sourceip='221.233.116.256'
limit 100;
