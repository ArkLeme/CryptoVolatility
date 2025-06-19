# CryptoVolatility Spark applications

This directory contains the Python Spark applications.

There is two spark applications:

- `bin/ingest_binance.py`: Ingests Binance for a specific symbol, date range, and interval.
- `bin/process_binance.py`: Processes the ingested data for a specific symbol and date, and computes hourly volatility.

## Prerequisites

- Java 8
- uv
- Python 3.8
- Docker and Docker Compose (for YARN cluster setup)

## Setup

To set up the environment, you can use the provided `Makefile` to install the necessary dependencies.

```bash
make install
```

## Running the Applications

To run the applications, you can use the provided `Makefile` or submit them manually to a YARN cluster.
Be sure that the YARN cluster is running and accessible.

### Using the Makefile

You can use the `Makefile` to submit the applications:

```bash
# Run the ingest application
make run_ingest 
# Run the process application
make run_volatility
```



