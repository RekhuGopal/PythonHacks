unload ('select * from dev.public.test')
to 's3://redshift-table-to-s3-bucket/'
iam_role 'arn:aws:iam::357171621133:role/ETLlambdaAccessRole';