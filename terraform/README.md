# Terraform for Crypto Volatility Project

This directory contains the Terraform configuration for the Crypto Volatility project infrastructure, organized into modular services.

## Structure

The infrastructure is organized into the following service modules:

### s3/
- **Purpose**: S3 bucket for data storage
- **Resources**: S3 bucket with proper tagging
- **Files**: `main.tf`, `variables.tf`

### glue/
- **Purpose**: AWS Glue Data Catalog
- **Resources**: Glue catalog database
- **Files**: `main.tf`

### emr/
- **Purpose**: EMR Serverless application with networking
- **Resources**: 
  - VPC with public subnet
  - Internet Gateway
  - Route tables and associations
  - Security groups
  - EMR Serverless application
- **Files**: `main.tf`, `variables.tf`

### iam/
- **Purpose**: IAM roles and policies for all services
- **Resources**:
  - EMR Serverless execution role and policy
  - Step Functions execution role and policy
- **Files**: `main.tf`, `variables.tf`

### step-functions/
- **Purpose**: Step Functions state machine for orchestration
- **Resources**: State machine with EMR job execution
- **Files**: `main.tf`, `variables.tf`

## Root Files

- `main.tf`: Main configuration that references all modules
- `variables.tf`: Global variables

## Usage

```bash
terraform init
terraform plan
terraform apply
```

### Variables

The following variables can be configured:

- `aws_region`: AWS region (default: "eu-west-3")
- `environment`: Environment name (default: "prod")

## Dependencies

The modules have the following dependencies:

1. **S3** - No dependencies
2. **Glue** - No dependencies  
3. **EMR** - No dependencies
4. **IAM** - Depends on S3, Glue, and EMR outputs
5. **Step Functions** - Depends on IAM, EMR, and S3 outputs