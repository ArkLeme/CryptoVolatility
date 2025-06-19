import argparse
from datetime import datetime, timedelta, timezone
from pyspark.sql import DataFrame as pyspark_df
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, hour, log, stddev, lit, concat

from crypto_volatility.schema_loader import load_schema
from crypto_volatility.table_manager import (
    database_exists,
    table_exists,
    insert_into_table,
)


def create_spark_session() -> SparkSession:
    """
    Create Spark session
    """
    builder = SparkSession.builder.appName("CryptoVolatility Processor")
    return builder.getOrCreate()


def parse_args():
    """
    Set up command line argument parser
    """
    parser = argparse.ArgumentParser(
        description="Process crypto volatility from Binance data"
    )

    parser.add_argument(
        "--catalog",
        type=str,
        default="hive",
        help="Catalog to use for the Spark session (default: hive)",
    )

    parser.add_argument(
        "--schema_path", type=str, required=True, help="Path to the schema file"
    )

    parser.add_argument(
        "--date",
        type=str,
        default=(datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d"),
        help="Date for which to process data (format: YYYY-MM-DD)",
    )
    parser.add_argument(
        "--symbol",
        type=str,
        default="BTCUSDT",
        help="Crypto symbol (default: BTCUSDT)",
    )

    parser.add_argument(
        "--source_table",
        type=str,
        default="binance_crypto_kline",
        help="Source table name for Binance kline data (default: binance_crypto_kline)",
    )
    parser.add_argument(
        "--source_db",
        type=str,
        default="crypto_binance",
        help="Source database name (default: crypto_binance)",
    )

    return parser.parse_args()


def compute_volatility(df: pyspark_df) -> pyspark_df:
    """
    Compute hourly volatility from kline data.
    
    Args:
        df (pyspark_df): DataFrame containing kline data

    Returns:
        pyspark_df: DataFrame with computed volatility
    """

    first_open_price = df.select("open_price").first()[0]

    df_log_return = df.withColumn(
        "log_return", log(col("close_price") / lit(first_open_price))
    ).withColumn("hour", hour(col("open_time")))

    df_volatility = df_log_return.groupBy("symbol", "hour").agg(
        stddev("log_return").alias("volatility")
    )

    df_volatility = df_volatility.orderBy("hour").withColumn(
        "hour", concat(col("hour"), lit(":00:00"))
    )

    df_volatility = df_volatility.withColumn(
        "volatility_percent", col("volatility") * 100
    )

    return df_volatility


def main():
    args = parse_args()

    db, table_name, schema, partition_columns = load_schema(args.schema_path)

    spark = create_spark_session()

    if not database_exists(spark, args.source_db):
        raise ValueError(f"Database {args.source_db} does not exist.")
    if not table_exists(spark, args.source_table, args.source_db):
        raise ValueError(
            f"Table {args.source_table} does not exist in database {args.source_db}."
        )

    # Load kline data for the specified symbol and date
    df_klines = spark.sql(
        f"""
        SELECT * FROM {args.source_db}.{args.source_table}
        WHERE symbol = '{args.symbol}'
        AND date = '{args.date}'
        ORDER BY open_time
    """
    )
    if df_klines.isEmpty():
        raise ValueError(f"No data found for symbol {args.symbol} on date {args.date}.")

    # Compute volatility
    df_volatility = compute_volatility(df_klines)

    date = datetime.strptime(args.date, "%Y-%m-%d")
    next_date = (date + timedelta(days=1)).strftime("%Y-%m-%d")

    partition_columns_names = [p["name"] for p in partition_columns]
    df_final = df_volatility.withColumn("date", lit(next_date)).select(
        schema.fieldNames() + partition_columns_names
    )

    # Insert the DataFrame into the specified table
    insert_into_table(
        spark=spark,
        df=df_final,
        table_name=table_name,
        db=db,
        catalog=args.catalog,
        schema=schema,
        partition_columns=partition_columns,
    )

    print(f"Volatility data processed and stored in {db}.{table_name} successfully.")
    spark.stop()


if __name__ == "__main__":
    main()
