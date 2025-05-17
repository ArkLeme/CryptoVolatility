import yaml
from typing import List, Tuple
from pyspark.sql.types import (
    DataType,
    StructType,
    StructField,
    StringType,
    IntegerType,
    LongType,
    DoubleType,
    BooleanType,
    TimestampType,
    DateType,
)


def get_data_type(type_str: str) -> DataType:
    mapping = {
        "string": StringType(),
        "int": IntegerType(),
        "long": LongType(),
        "double": DoubleType(),
        "bool": BooleanType(),
        "timestamp": TimestampType(),
        "date": DateType(),
    }
    type_str = type_str.strip().lower()
    if type_str not in mapping:
        raise ValueError(f"Unsupported type: {type_str}")
    return mapping[type_str]


def load_schema(path: str) -> Tuple[str, str, StructType, List[dict]]:
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    table_name = data["name"]
    db = data["db"]
    fields = data["schema"]
    partition_columns = data.get("partition_columns", [])

    struct_fields = [StructField(f["name"], get_data_type(f["type"])) for f in fields]

    return db, table_name, StructType(struct_fields), partition_columns
