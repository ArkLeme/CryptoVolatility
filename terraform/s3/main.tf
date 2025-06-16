# S3 bucket
resource "aws_s3_bucket" "crypto_volatility" {
  bucket = "crypto-volatility-${var.environment}"

  tags = {
    Environment = var.environment
    Project     = "crypto-volatility"
  }
} 