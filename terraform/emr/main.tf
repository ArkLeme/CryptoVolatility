# VPC for EMR Serverless
resource "aws_vpc" "emr_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "emr-serverless-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "emr_igw" {
  vpc_id = aws_vpc.emr_vpc.id

  tags = {
    Name = "emr-serverless-igw"
  }
}

# Public Subnet
resource "aws_subnet" "emr_public" {
  vpc_id                  = aws_vpc.emr_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name = "emr-serverless-public-subnet"
  }
}

# Route Table
resource "aws_route_table" "emr_public" {
  vpc_id = aws_vpc.emr_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.emr_igw.id
  }

  tags = {
    Name = "emr-serverless-public-rt"
  }
}

# Route Table Association
resource "aws_route_table_association" "emr_public" {
  subnet_id      = aws_subnet.emr_public.id
  route_table_id = aws_route_table.emr_public.id
}

# Security Group for EMR Serverless
resource "aws_security_group" "emr_serverless" {
  name        = "emr-serverless-sg"
  description = "Security group for EMR Serverless"
  vpc_id      = aws_vpc.emr_vpc.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "emr-serverless-sg"
  }
}

# EMR Serverless Application
resource "aws_emrserverless_application" "crypto_volatility" {
  name          = "crypto-volatility-${var.environment}"
  release_label = "emr-6.15.0"
  type          = "SPARK"

  initial_capacity {
    initial_capacity_type = "DRIVER"
    initial_capacity_config {
      worker_count = 1
      worker_configuration {
        cpu    = "2vCPU"
        memory = "8GB"
      }
    }
  }

  initial_capacity {
    initial_capacity_type = "EXECUTOR"
    initial_capacity_config {
      worker_count = 2
      worker_configuration {
        cpu    = "2vCPU"
        memory = "8GB"
      }
    }
  }

  maximum_capacity {
    cpu    = "8vCPU"
    memory = "32GB"
  }

  auto_stop_configuration {
    enabled              = true
    idle_timeout_minutes = 5
  }

  network_configuration {
    subnet_ids         = [aws_subnet.emr_public.id]
    security_group_ids = [aws_security_group.emr_serverless.id]
  }
} 