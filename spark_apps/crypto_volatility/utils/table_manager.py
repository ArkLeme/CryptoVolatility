from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from typing import List, Dict


def database_exists(
    spark: SparkSession,
    db: str,
) -> bool:
    return spark.catalog.databaseExists(db)


def table_exists(
    spark: SparkSession,
    table_name: str,
    db: str,
) -> bool:
    return spark.catalog.tableExists(f"{db}.{table_name}")


def create_database(
    spark: SparkSession,
    db: str,
):
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {db}")
    print(f"Database created: {db}")


def create_table(
    spark: SparkSession,
    table_name: str,
    db: str,
    schema: StructType,
    partition_columns: List[Dict] = None,
    location: str = None,
):
    full_table_name = f"{db}.{table_name}"

    partition_columns_str = ", ".join(
        [f"{p['name']} {p['type']}" for p in partition_columns]
    )
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
    schema: StructType,
    partition_columns: List[Dict] = None,
):
    if not database_exists(spark, db):
        create_database(spark, db)

    if not table_exists(spark, table_name, db):
        create_table(
            spark=spark,
            table_name=table_name,
            db=db,
            schema=schema,
            partition_columns=partition_columns,
        )
    df.write.format("parquet").insertInto(f"{db}.{table_name}", overwrite=True)
