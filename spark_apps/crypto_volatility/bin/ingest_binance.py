import argparse
import pandas as pd
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

from utils.binance import get_klines_by_date
from utils.schema_loader import load_schema
from utils.table_manager import insert_into_table


def create_spark_session() -> SparkSession:
    builder = SparkSession.builder.appName("CryptoVolatility Ingest Binance")
    return builder.getOrCreate()


def parse_args():
    parser = argparse.ArgumentParser(description="Ingest Binance data")

    parser.add_argument(
        "--schema_path", type=str, required=True, help="Path to the schema file"
    )

    binance_group = parser.add_argument_group(
        "binance",
        "Binance API parameters",
    )
    binance_group.add_argument(
        "--symbol",
        type=str,
        default="BTCUSDT",
        help="Crypto symbol (default: BTCUSDT)",
    )
    binance_group.add_argument(
        "--date",
        type=str,
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Date for which to process data (format: YYYY-MM-DD)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if not os.path.exists(args.schema_path):
        raise FileNotFoundError(f"Schema file not found: {args.schema_path}")

    db, table_name, schema, partition_columns = load_schema(args.schema_path)

    klines = get_klines_by_date(
        symbol=args.symbol,
        date=args.date,
    )

    if klines.empty:
        print(
            f"No data found for symbol {args.symbol} from {args.start_time} to {args.end_time}."
        )
        return
    spark = create_spark_session()

    df = spark.createDataFrame(klines)
    df = df.withColumn("date", lit(args.date))
    df = df.withColumn("symbol", lit(args.symbol))
    partition_columns_names = [p["name"] for p in partition_columns]
    df = df.select(schema.fieldNames() + partition_columns_names)

    insert_into_table(
        spark=spark,
        df=df,
        table_name=table_name,
        db=db,
        schema=schema,
        partition_columns=partition_columns,
    )

    print(f"Data ingested into {db}.{table_name} successfully: {len(klines)} records.")
    spark.stop()


if __name__ == "__main__":
    main()
