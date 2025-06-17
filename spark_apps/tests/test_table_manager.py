from unittest.mock import MagicMock, patch
from pyspark.sql.types import StructType, StructField, StringType
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../crypto_volatility')))
import table_manager

def test_database_exists():
    spark = MagicMock()
    spark.catalog.databaseExists.return_value = True
    assert table_manager.database_exists(spark, 'test_db') is True
    spark.catalog.databaseExists.assert_called_with('test_db')

def test_table_exists():
    spark = MagicMock()
    spark.catalog.tableExists.return_value = True
    assert table_manager.table_exists(spark, 'test_table', 'test_db') is True
    spark.catalog.tableExists.assert_called_with('test_db.test_table')

def test_create_database():
    spark = MagicMock()
    table_manager.create_database(spark, 'test_db')
    spark.sql.assert_called_with('CREATE DATABASE IF NOT EXISTS test_db')

def test_create_table():
    spark = MagicMock()
    schema = StructType([StructField('id', StringType())])
    partition_columns = [{'name': 'date', 'type': 'date'}]
    table_manager.create_table(spark, 'test_table', 'test_db', 'hive', schema, partition_columns, location=None)
    assert spark.sql.called

def test_insert_into_table():
    spark = MagicMock()
    df = MagicMock()
    schema = StructType([StructField('id', StringType())])
    partition_columns = [{'name': 'date', 'type': 'date'}]
    with patch('table_manager.database_exists', return_value=False), \
         patch('table_manager.create_database') as mock_create_db, \
         patch('table_manager.table_exists', return_value=False), \
         patch('table_manager.create_table') as mock_create_table:
        table_manager.insert_into_table(spark, df, 'test_table', 'test_db', 'hive', schema, partition_columns)
        mock_create_db.assert_called_once()
        mock_create_table.assert_called_once()
    assert df.write.format().insertInto.called or df.write.format.return_value.insertInto.called 