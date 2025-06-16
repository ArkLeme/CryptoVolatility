variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
}

variable "s3_bucket_arn" {
  description = "ARN of the S3 bucket"
  type        = string
}

variable "glue_database_arn" {
  description = "ARN of the Glue catalog database"
  type        = string
}

variable "emr_application_arn" {
  description = "ARN of the EMR Serverless application"
  type        = string
} 