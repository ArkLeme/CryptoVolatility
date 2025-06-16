variable "environment" {
  description = "Environment name (e.g., dev, prod)"
  type        = string
}

variable "step_functions_role_arn" {
  description = "ARN of the Step Functions IAM role"
  type        = string
}

variable "emr_application_id" {
  description = "ID of the EMR Serverless application"
  type        = string
}

variable "emr_serverless_role_arn" {
  description = "ARN of the EMR Serverless IAM role"
  type        = string
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
} 