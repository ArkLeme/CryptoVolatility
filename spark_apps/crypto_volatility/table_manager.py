from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from typing import List, Dict


def database_exists(
    spark: SparkSession,
    db: str,
) -> bool:
    """
    Check if a database exists in Spark.
    
    Args:
        spark (SparkSession): Spark session.
        db (str): Database name.
    Returns:
        bool: True if the database exists, False otherwise.
    """
    return spark.catalog.databaseExists(db)


def table_exists(
    spark: SparkSession,
    table_name: str,
    db: str,
) -> bool:
    """
    Check if a table exists in a specific database.
    
    Args:
        spark (SparkSession): Spark session.
        table_name (str): Table name.
        db (str): Database name.

    Returns:
        bool: True if the table exists, False otherwise.
    """
    return spark.catalog.tableExists(f"{db}.{table_name}")


def create_database(
    spark: SparkSession,
    db: str,
):
    """
    Create a database in Spark if it does not exist.
    
    Args:
        spark (SparkSession): Spark session.
        db (str): Database name.
    """
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {db}")
    print(f"Database created: {db}")


def create_table(
    spark: SparkSession,
    table_name: str,
    db: str,
    catalog: str,
    schema: StructType,
    partition_columns: List[Dict] = None,
    location: str = None,
):
    """
    Create a table in Spark with the specified schema and partitioning.
    
    Args:
        spark (SparkSession): Spark session.
        table_name (str): Table name.
        db (str): Database name.
        catalog (str): Catalog name ( AwsDataCatalog' or 'hive').
        schema (StructType): Schema of the table.
        partition_columns (List[Dict], optional): List of partition columns with their names and types.
        location (str, optional): Location for the table data.
    """

    full_table_name = f"{db}.{table_name}"
    partition_columns_str = ", ".join(
        [f"{p['name']} {p['type']}" for p in partition_columns]
    )
    if catalog == "AwsDataCatalog":
        spark.sql(
            f"""
            CREATE TABLE IF NOT EXISTS {full_table_name} (
                {', '.join([f"{field.name} {field.dataType.simpleString()}" for field in schema.fields])},
                {partition_columns_str}
            )
            USING iceberg
            PARTITIONED BY ({', '.join([p['name'] for p in partition_columns])})
            {f"LOCATION '{location}'" if location else ""}
            """
        )
    else:
        partition_columns_str = (
            f"PARTITIONED BY ({partition_columns_str})" if partition_columns else ""
        )
        spark.sql(
            f"""
            CREATE TABLE IF NOT EXISTS {full_table_name} (
                {', '.join([f"{field.name} {field.dataType.simpleString()}" for field in schema.fields if field.name not in  [p['name'] for p in partition_columns]])}
            )
            {partition_columns_str}
            STORED AS PARQUET
            {f"LOCATION '{location}'" if location else ""}
            """
        )

    print(f"Table created: {full_table_name}")


def insert_into_table(
    spark: SparkSession,
    df,
    table_name: str,
    db: str,
    catalog: str,
    schema: StructType,
    partition_columns: List[Dict] = None,
):
    """
    Insert a DataFrame into a specified table in Spark, creating the database and table if they do not exist.

    Args:
        spark (SparkSession): Spark session.
        df: DataFrame to insert.
        table_name (str): Table name.
        db (str): Database name.
        catalog (str): Catalog name (AwsDataCatalog' or 'hive').
        schema (StructType): Schema of the table.
        partition_columns (List[Dict], optional): List of partition columns with their names and types.
    """

    if not database_exists(spark, db):
        create_database(spark, db)

    if not table_exists(spark, table_name, db):
        create_table(
            spark=spark,
            table_name=table_name,
            db=db,
            catalog=catalog,
            schema=schema,
            partition_columns=partition_columns,
        )
    df.write.format("parquet").insertInto(f"{db}.{table_name}", overwrite=True)
