# IAM Role for EMR Serverless
resource "aws_iam_role" "emr_serverless_role" {
  name = "crypto_volatility_emr_serverless_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "emr-serverless.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy for EMR Serverless
resource "aws_iam_role_policy" "emr_serverless_policy" {
  name = "crypto_volatility_emr_serverless_policy"
  role = aws_iam_role.emr_serverless_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket",
          "s3:DeleteObject"
        ]
        Resource = [
          var.s3_bucket_arn,
          "${var.s3_bucket_arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "glue:GetDatabase",
          "glue:GetDatabases",
          "glue:GetTable",
          "glue:GetTables",
          "glue:GetPartition",
          "glue:GetPartitions",
          "glue:CreateTable",
          "glue:CreateDatabase",
          "glue:UpdateTable",
          "glue:BatchCreatePartition",
          "glue:BatchUpdatePartition",
          "glue:GetCatalog",
          "glue:GetDataCatalogEncryptionSettings",
          "glue:GetUserDefinedFunction",
          "glue:GetUserDefinedFunctions"
        ]
        Resource = [
          var.glue_database_arn,
          "${var.glue_database_arn}/*",
          "arn:aws:glue:${var.aws_region}:*:catalog",
          "arn:aws:glue:${var.aws_region}:*:database/*",
          "arn:aws:glue:${var.aws_region}:*:table/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams",
          "logs:GetLogEvents",
          "logs:PutRetentionPolicy"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# IAM Role for Step Functions
resource "aws_iam_role" "step_functions_role" {
  name = "crypto_volatility_step_functions_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "states.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy for Step Functions
resource "aws_iam_role_policy" "step_functions_policy" {
  name = "crypto_volatility_step_functions_policy"
  role = aws_iam_role.step_functions_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "emr-serverless:StartJobRun",
          "emr-serverless:GetJobRun",
          "emr-serverless:CancelJobRun",
          "emr-serverless:ListJobRuns"
        ]
        Resource = [var.emr_application_arn, "${var.emr_application_arn}/*"]
      },
      {
        Effect = "Allow"
        Action = [
          "iam:PassRole"
        ]
        Resource = aws_iam_role.emr_serverless_role.arn
      },
      {
        Effect = "Allow"
        Action = [
          "states:CreateStateMachine",
          "states:DeleteStateMachine",
          "states:DescribeStateMachine",
          "states:ListStateMachines",
          "states:StartExecution",
          "states:StopExecution",
          "states:TagResource",
          "states:UntagResource",
          "states:UpdateStateMachine"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "events:PutRule",
          "events:DeleteRule",
          "events:DescribeRule",
          "events:DisableRule",
          "events:EnableRule",
          "events:PutTargets",
          "events:RemoveTargets",
          "events:ListTargetsByRule"
        ]
        Resource = "*"
      }
    ]
  })
} 