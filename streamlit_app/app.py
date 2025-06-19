import streamlit as st
import pandas as pd
from pyspark.sql import SparkSession
import os


def create_spark_session(use_aws = False) -> SparkSession:
    """Create Spark session based on the selected data source."""
    builder = (SparkSession.builder
              .appName("CryptoVolatilityStreamlit")
              )

    if use_aws:
        # AWS Glue configuration
        builder = (builder
                #   .config("spark.sql.warehouse.dir",
                #          f"s3a://{st.secrets['S3_BUCKET']}/warehouse")
                 .config("spark.sql.defaultCatalog", "AwsDataCatalog")
                  .config("spark.hadoop.fs.s3a.access.key", st.secrets['AWS_ACCESS_KEY_ID'])
                  .config("spark.hadoop.fs.s3a.secret.key", st.secrets['AWS_SECRET_ACCESS_KEY'])
                  .config("spark.hadoop.fs.s3a.endpoint", f"s3.{st.secrets['AWS_REGION']}.amazonaws.com")
                  .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
                  .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain")
                .config("spark.sql.catalog.AwsDataCatalog", "org.apache.iceberg.spark.SparkCatalog")
                .config("spark.sql.catalog.AwsDataCatalog.catalog-impl", "org.apache.iceberg.aws.glue.GlueCatalog")
                .config("spark.sql.catalog.AwsDataCatalog.warehouse", f"s3a://{st.secrets['S3_BUCKET']}/warehouse")
                .config("spark.sql.catalog.AwsDataCatalog.io-impl", "org.apache.iceberg.aws.s3.S3FileIO")
                .config("spark.sql.catalog.AwsDataCatalog.glue.skip-name-validation", "true")
                    .config("spark.jars.packages",
            ",".join([
                "org.apache.iceberg:iceberg-spark-runtime-3.3_2.12:1.3.0",
                "org.apache.iceberg:iceberg-aws:1.3.0",
                # "com.amazonaws:aws-java-sdk-bundle:1.12.262",
                "org.apache.hadoop:hadoop-aws:3.3.6",
                "software.amazon.awssdk:glue:2.20.155",
                "software.amazon.awssdk:auth:2.20.155",
                "software.amazon.awssdk:regions:2.20.155",
                "software.amazon.awssdk:sts:2.20.155",
                "software.amazon.awssdk:s3:2.20.155",
                "software.amazon.awssdk:kms:2.20.155",
                "software.amazon.awssdk:dynamodb:2.20.155",
            ])))
                #   .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.2.2,com.amazonaws:aws-java-sdk-bundle:1.12.262")
    # .config("spark.sql.catalog.default", "AwsDataCatalog")
                #   .enableHiveSupport())
    else:
        # Local Hive configuration
        builder = (builder
                .enableHiveSupport()
                
                  .config("spark.sql.warehouse.dir", '/user/hive/warehouse')
                  .config("spark.hadoop.hive.metastore.uris",'thrift://localhost:9083'))

    return builder.getOrCreate()

def get_available_symbols(spark: SparkSession):
    """Get list of available symbols from the bronze table."""
    try:
        symbols_df = spark.sql("""
            SELECT DISTINCT symbol
            FROM crypto_volatility.crypto_bronze
            ORDER BY symbol
        """)
        return [row.symbol for row in symbols_df.collect()]
    except Exception as e:
        st.error(f"Error getting available symbols: {str(e)}")
        return []

def read_bronze_data(spark: SparkSession, symbol: str, limit: int = 1000) -> pd.DataFrame:
    """Read bronze data for a specific symbol."""
    try:
        df = spark.sql(f"""
            SELECT *
            FROM crypto_volatility.crypto_bronze
            WHERE symbol = '{symbol}'
            ORDER BY date DESC
            LIMIT {limit}
        """)
        print(df.schema)
        df = df.withColumn("open_time", df["open_time"].cast("string")) \
        .withColumn("close_time", df["close_time"].cast("string")) \
                     .withColumn("ingestion_time", df["ingestion_time"].cast("string")) \
                        .withColumn("date", df["date"].cast("string"))
        print(df.toPandas().head())
        return df.toPandas()
    except Exception as e:
        st.error(f"Error reading data for {symbol}: {str(e)}")
        return pd.DataFrame()

def main():
    st.set_page_config(page_title="Crypto Bronze Data Viewer", layout="wide")
    
    st.title("Crypto Bronze Data Viewer")
    
    # Data source selection
    use_aws = st.sidebar.radio(
        "Select Data Source",
        ["AWS Glue", "Local Hive"],
        index=0
    )
    
    # Create Spark session
    if not "spark_session" in st.session_state:
        st.session_state.spark_session = create_spark_session(use_aws == "AWS Glue")
    else:
        st.session_state.spark_session.stop()
        st.session_state.spark_session = create_spark_session(use_aws == "AWS Glue")

    spark = st.session_state.spark_session
    # print(spark.catalog.listCatalogs())
    # print(spark.catalog.listDatabases())
    # spark.sql("SHOW TABLES IN AwsDataCatalog.default").show()

    # schema = """CREATE TABLE crypto_volatility.crypto_bronze (
    #         symbol string,
    #         open_time timestamp,
    #         open_price double,
    #         high_price double,
    #         low_price double,
    #         close_price double,
    #         volume double,
    #         close_time timestamp,
    #         quote_asset_volume double,
    #         number_of_trades int,
    #         taker_buy_base_asset_volume double,
    #         taker_buy_quote_asset_volume double,
    #         ignore string,
    #         ingestion_time timestamp,
    #         date date)
    #     USING iceberg
    #     PARTITIONED BY (date);
    #     """
    # spark.sql(schema)

    # spark.sql("CREATE DATABASE IF NOT EXISTS test_db")
    # spark.sql("USE test_db")
    # spark.sql("""
    #     CREATE TABLE IF NOT EXISTS crypto_bronze_test (
    #         symbol STRING,
    #         open_time TIMESTAMP,
    #         open_price DOUBLE,
    #         high_price DOUBLE,
    #         low_price DOUBLE,
    #         close_price DOUBLE,
    #         volume DOUBLE,
    #         close_time TIMESTAMP,
    #         quote_asset_volume DOUBLE,
    #         number_of_trades INT,
    #         taker_buy_base_asset_volume DOUBLE,
    #         taker_buy_quote_asset_volume DOUBLE,
    #         ignore STRING,
    #         ingestion_time TIMESTAMP
    #     )
    #     PARTITIONED BY (date STRING)
    #     STORED AS PARQUET
    # """)

    # df = pd.DataFrame({
    #     'symbol': ['BTCUSDT', 'ETHUSDT'],
    #     'open_time': pd.to_datetime(['2023-10-01', '2023-10-01']),
    #     'open_price': [50000.0, 3500.0],
    #     'high_price': [51000.0, 3600.0],
    #     'low_price': [49000.0, 3400.0],
    #     'close_price': [50500.0, 3550.0],
    #     'volume': [1000.0, 500.0],
    #     'close_time': pd.to_datetime(['2023-10-02', '2023-10-02']),
    #     'quote_asset_volume': [50000000.0, 1750000.0],
    #     'number_of_trades': [100, 50],
    #     'taker_buy_base_asset_volume': [600.0, 300.0],
    #     'taker_buy_quote_asset_volume': [30000000.0, 1050000.0],
    #     'ignore': ['ignore1', 'ignore2'],
    #     'ingestion_time': pd.to_datetime(['2023-10-03', '2023-10-03']),
    #     'date': ['2023-10-01', '2023-10-01']
    # })

    # df_spark = spark.createDataFrame(df)
    # df_spark.write.mode("overwrite").insertInto("test_db.crypto_bronze_test")

    # print(spark.catalog.listTables("default"))
    try:
        # Get available symbols
        symbols = get_available_symbols(spark)
        
        if not symbols:
            st.error("No data available in the bronze table.")
            return
        
        # Sidebar controls
        st.sidebar.header("Data Selection")
        selected_symbol = st.sidebar.selectbox("Select Cryptocurrency", symbols)
        row_limit = st.sidebar.number_input("Number of rows to display", 
                                          min_value=100, 
                                          max_value=10000, 
                                          value=1000, 
                                          step=100)
        
        # Read and display data
        df = read_bronze_data(spark, selected_symbol, row_limit)
        
        if df.empty:
            st.warning(f"No data available for {selected_symbol}")
            return
        
        # Display data
        st.subheader(f"Raw Data for {selected_symbol}")
        st.dataframe(df)
        
        # Display basic statistics
        st.subheader("Basic Statistics")
        st.write(df.describe())
    
    finally:
        # Stop Spark session
        spark.stop()

if __name__ == "__main__":
    main() 