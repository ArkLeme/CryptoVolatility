# Step Functions State Machine
resource "aws_sfn_state_machine" "crypto_volatility" {
  name     = "crypto-volatility-${var.environment}"
  role_arn = var.step_functions_role_arn

  definition = jsonencode({
    Comment = "Crypto Volatility Data Pipeline"
    StartAt = "IngestBinance"
    States = {
      IngestBinance= {
        Type     = "Task"
        Resource = "arn:aws:states:::emr-serverless:startJobRun.sync"
        Parameters = {
          ApplicationId    = var.emr_application_id
          ExecutionRoleArn = var.emr_serverless_role_arn
          JobDriver = {
            SparkSubmit = {
              EntryPoint = "s3://${var.s3_bucket_name}/code/ingest_binance.py"
              EntryPointArguments = [
                "--symbol", "BTCUSDT",
                "--catalog", "AwsDataCatalog",
                "--schema", "s3://${var.s3_bucket_name}/schema/binance_crypto_kline.yml"
              ]
            }
          }
          ConfigurationOverrides = {
            ApplicationConfiguration = [
              {
                Classification = "spark-defaults"
                Properties = {
                  "spark.app.name"                                = "Binance Ingestion"
                  "spark.sql.defaultCatalog" =  "AwsDataCatalog"
                  "spark.sql.catalog.AwsDataCatalog"              = "org.apache.iceberg.spark.SparkCatalog"
                  "spark.sql.catalog.AwsDataCatalog.catalog-impl" = "org.apache.iceberg.aws.glue.GlueCatalog"
                  "spark.sql.catalog.AwsDataCatalog.io-impl"      = "org.apache.iceberg.aws.s3.S3FileIO"
                  "spark.sql.catalog.AwsDataCatalog.warehouse"    = "s3://${var.s3_bucket_name}/warehouse/"
                  "spark.dynamicAllocation.enabled"                      = "true"
                  "spark.executor.instances"                             = "2"
                  "spark.dynamicAllocation.initialExecutors"             = "1"
                  "spark.dynamicAllocation.minExecutors"                 = "1"
                  "spark.dynamicAllocation.maxExecutors"                 = "4"
                  "spark.executor.cores"                                 = "2"
                  "spark.executor.memory"                                = "6g"
                  "spark.executor.memoryOverhead"                        = "1g"
                  "spark.driver.cores"                                   = "2"
                  "spark.driver.memory"                                  = "6g"
                  "spark.driver.memoryOverhead"                          = "1g"
                  "spark.memory.fraction"                                = "0.8"
                  "spark.memory.storageFraction"                         = "0.3"
                  "spark.archives"                                       = "s3://${var.s3_bucket_name}/deps/deps.zip#environment"
                  "spark.emr-serverless.driverEnv.PYSPARK_DRIVER_PYTHON" = "./environment/bin/python"
                  "spark.emr-serverless.driverEnv.PYSPARK_PYTHON"        = "./environment/bin/python"
                  "spark.executorEnv.PYSPARK_PYTHON"                     = "./environment/bin/python"
                  "spark.sql.catalog.AwsDataCatalog.glue.skip-name-validation" = "true"
                }
              }
            ]
            MonitoringConfiguration = {
              S3MonitoringConfiguration = {
                LogUri = "s3://${var.s3_bucket_name}/logs/"
              }
            }
          }
        }
        Next = "ProcessVolatility"
      },
      ProcessVolatility = {
        Type     = "Task"
        Resource = "arn:aws:states:::emr-serverless:startJobRun.sync"
        Parameters = {
          ApplicationId    = var.emr_application_id
          ExecutionRoleArn = var.emr_serverless_role_arn
          JobDriver = {
            SparkSubmit = {
              EntryPoint = "s3://${var.s3_bucket_name}/code/process_volatility.py"
              EntryPointArguments = [
                "--catalog", "AwsDataCatalog",
                "--schema_path", "s3://${var.s3_bucket_name}/schema/binance_crypto_hourly_volatility.yml",
                "--symbol", "BTCUSDT",
                "--source_table", "binance_crypto_kline",
                "--source_db", "crypto_binance",
              ]
            }
          }
          ConfigurationOverrides = {
            ApplicationConfiguration = [
              {
                Classification = "spark-defaults"
                Properties = {
                  "spark.app.name"                                = "Process Crypto Volatility"
                  "spark.sql.defaultCatalog" =  "AwsDataCatalog"
                  "spark.sql.catalog.AwsDataCatalog"              = "org.apache.iceberg.spark.SparkCatalog"
                  "spark.sql.catalog.AwsDataCatalog.catalog-impl" = "org.apache.iceberg.aws.glue.GlueCatalog"
                  "spark.sql.catalog.AwsDataCatalog.io-impl"      = "org.apache.iceberg.aws.s3.S3FileIO"
                  "spark.sql.catalog.AwsDataCatalog.warehouse"    = "s3://${var.s3_bucket_name}/warehouse/"
                  "spark.dynamicAllocation.enabled"                      = "true"
                  "spark.executor.instances"                             = "2"
                  "spark.dynamicAllocation.initialExecutors"             = "1"
                  "spark.dynamicAllocation.minExecutors"                 = "1"
                  "spark.dynamicAllocation.maxExecutors"                 = "4"
                  "spark.executor.cores"                                 = "2"
                  "spark.executor.memory"                                = "6g"
                  "spark.executor.memoryOverhead"                        = "1g"
                  "spark.driver.cores"                                   = "2"
                  "spark.driver.memory"                                  = "6g"
                  "spark.driver.memoryOverhead"                          = "1g"
                  "spark.memory.fraction"                                = "0.8"
                  "spark.memory.storageFraction"                         = "0.3"
                  "spark.archives"                                       = "s3://${var.s3_bucket_name}/deps/deps.zip#environment"
                  "spark.emr-serverless.driverEnv.PYSPARK_DRIVER_PYTHON" = "./environment/bin/python"
                  "spark.emr-serverless.driverEnv.PYSPARK_PYTHON"        = "./environment/bin/python"
                  "spark.executorEnv.PYSPARK_PYTHON"                     = "./environment/bin/python"
                  "spark.sql.catalog.AwsDataCatalog.glue.skip-name-validation" = "true"
                }
              }
            ]
            MonitoringConfiguration = {
              S3MonitoringConfiguration = {
                LogUri = "s3://${var.s3_bucket_name}/logs/"
              }
            }
          }
        }
        End = true
      }
    }
  })
} 