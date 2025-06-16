terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# S3 Module
module "s3" {
  source = "./s3"
  
  environment = var.environment
}

# Glue Module
module "glue" {
  source = "./glue"
}

# EMR Module
module "emr" {
  source = "./emr"
  
  aws_region  = var.aws_region
  environment = var.environment
}

# IAM Module
module "iam" {
  source = "./iam"
  
  aws_region           = var.aws_region
  s3_bucket_arn        = module.s3.bucket_arn
  glue_database_arn    = module.glue.database_arn
  emr_application_arn  = module.emr.application_arn
}

# Step Functions Module
module "step_functions" {
  source = "./step-functions"
  
  environment              = var.environment
  step_functions_role_arn  = module.iam.step_functions_role_arn
  emr_application_id       = module.emr.application_id
  emr_serverless_role_arn  = module.iam.emr_serverless_role_arn
  s3_bucket_name           = module.s3.bucket_name
}