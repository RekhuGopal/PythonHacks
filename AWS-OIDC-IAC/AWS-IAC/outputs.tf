output "bucket_name" {
  value       = aws_s3_bucket.this.bucket
  description = "Name of the created S3 bucket"
}

output "bucket_arn" {
  value       = aws_s3_bucket.this.arn
  description = "ARN of the S3 bucket"
}
