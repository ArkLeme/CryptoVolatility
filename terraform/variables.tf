variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "eu-west-3"
}

variable "environment" {
  description = "Environment name (e.g., dev, prod)"
  type        = string
  default     = "prod"
}