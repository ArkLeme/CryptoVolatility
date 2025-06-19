import argparse
from datetime import datetime, timezone, timedelta
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

from crypto_volatility.binance import get_klines_by_date
from crypto_volatility.schema_loader import load_schema
from crypto_volatility.table_manager import insert_into_table


def create_spark_session() -> SparkSession:
    """
    Create Spark session
    """
    builder = SparkSession.builder.appName("CryptoVolatility Ingest Binance")
    return builder.getOrCreate()


def parse_args():
    """
    Set up command line argument parser
    """

    parser = argparse.ArgumentParser(description="Ingest Binance data")

    parser.add_argument(
        "--schema_path", type=str, required=True, help="Path to the schema file"
    )

    parser.add_argument(
        "--catalog",
        type=str,
        default="hive",
        help="Catalog to use for the Spark session (default: hive)",
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
        default=(datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d"),
        help="Date for which to process data (format: YYYY-MM-DD) (default: yesterday)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    db, table_name, schema, partition_columns = load_schema(args.schema_path)

    # Get binance data for the specified date and symbol
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

    #  Create DataFrame from the klines data and match the schema
    df = spark.createDataFrame(klines)
    df = df.withColumn("date", lit(args.date))
    df = df.withColumn("symbol", lit(args.symbol))
    partition_columns_names = [p["name"] for p in partition_columns]
    df = df.select(schema.fieldNames() + partition_columns_names)

    # Insert the DataFrame into the specified table
    insert_into_table(
        spark=spark,
        df=df,
        table_name=table_name,
        db=db,
        catalog=args.catalog,
        schema=schema,
        partition_columns=partition_columns,
    )

    print(f"Data ingested into {db}.{table_name} successfully: {len(klines)} records.")
    spark.stop()


if __name__ == "__main__":
    main()
