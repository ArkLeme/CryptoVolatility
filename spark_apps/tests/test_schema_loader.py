import pytest
from unittest.mock import patch
from pyspark.sql.types import StringType, IntegerType, DoubleType, BooleanType, TimestampType, DateType, StructType, StructField
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../crypto_volatility')))
from schema_loader import get_data_type, load_schema

def test_get_data_type_valid():
    assert isinstance(get_data_type('string'), StringType)
    assert isinstance(get_data_type('int'), IntegerType)
    assert isinstance(get_data_type('double'), DoubleType)
    assert isinstance(get_data_type('bool'), BooleanType)
    assert isinstance(get_data_type('timestamp'), TimestampType)
    assert isinstance(get_data_type('date'), DateType)

def test_get_data_type_invalid():
    with pytest.raises(ValueError):
        get_data_type('unknown')

def test_load_schema_local_real_file():
    schema_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../schema/binance_crypto_hourly_volatility.yml'))
    db, table_name, schema, partition_columns = load_schema(schema_path)
    assert db == 'crypto_binance'
    assert table_name == 'binance_crypto_hourly_volatility'
    assert isinstance(schema, StructType)
    field_names = [f.name for f in schema.fields]
    assert 'hour' in field_names
    assert 'volatility' in field_names
    assert 'volatility_percent' in field_names
    fields_types = [f.dataType for f in schema.fields]
    assert isinstance(fields_types[0], StringType)
    assert isinstance(fields_types[1], DoubleType)
    assert isinstance(fields_types[2], DoubleType)
    assert partition_columns[0]['name'] == 'date'
    assert partition_columns[0]['type'] == 'string'
    assert partition_columns[1]['name'] == 'symbol' 