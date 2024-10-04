-- 2020-10-01 1575353
-- 2020-11-01 1409851
-- 2020-12-01 1362454
SELECT DATE_TRUNC('month', pickup_datetime) "Period", 
       COUNT(*) "Total Records"
FROM   serverlessanalytics_357171621133_transformed
GROUP BY DATE_TRUNC('month', pickup_datetime)
ORDER BY 1;