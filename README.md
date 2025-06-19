# CryptoVolatility

CryptoVolatility is a modular, end-to-end platform for ingesting, processing, analyzing, and visualizing cryptocurrency volatility data, primarily sourced from Binance. The project leverages distributed data processing (Apache Spark), scalable cloud infrastructure (AWS EMR, S3, Glue, Step Functions), and a local Hadoop cluster for testing, to provide a robust environment for crypto data engineering and analytics.

## Project Structure

- **spark_apps/**: Python Spark applications for data ingestion and volatility computation.
  - `bin/ingest_binance.py`: Ingests raw kline (candlestick) data from Binance for specified symbols and dates.
  - `bin/process_volatility.py`: Processes ingested data to compute hourly volatility metrics.
  - Includes Makefile for local and cluster-based execution.

- **docker_cluster/**: Docker Compose setup for a local Hadoop/YARN cluster.
  - Services: NameNode, DataNode, ResourceManager, NodeManager, HistoryServer, Hive Metastore, HiveServer2, and PostgreSQL.
  - Enables local development and testing of Spark jobs in a distributed environment.

- **terraform/**: Infrastructure-as-Code for AWS deployment.
  - Modular Terraform scripts to provision S3 buckets, AWS Glue Data Catalog, EMR Serverless, IAM roles, and Step Functions for orchestration.
  - Supports scalable, production-grade cloud deployments.

## Quick Start

### Local Development

1. **Start the Hadoop Cluster**:
   ```sh
   cd docker_cluster
   docker-compose up -d --build
   ```
2. **Run Spark Applications**:
   ```sh
   cd spark_apps
   make install
   make run_ingest
   make run_volatility
   ```

### Cloud Deployment

On the root directory of the project, you can deploy the infrastructure and run Spark jobs on AWS EMR Serverless:
```sh
make all
```

## Documentation

- See `spark_apps/README.md`
- See `docker_cluster/README.md` for local cluster setup.
- See `terraform/README.md` for AWS infrastructure details.

## Requirements

- Docker, Docker Compose
- Python 3.8
- Java 8
- AWS CLI & credentials (for cloud deployment)
