import re
from typing import Optional

from pyspark.sql import DataFrame, SparkSession


def get_active_session() -> SparkSession:
    return SparkSession.getActiveSession()


def detect_delimiter(path: str) -> str:
    spark = get_active_session()
    # Read a small portion of the file to detect the delimiter
    sample = spark.read.text(path).limit(10).collect()
    lines: list[str] = [row[0] for row in sample]
    #
    possible_delimiters = ["|", ";", ","]
    delimiter_counts = {delimiter: 0 for delimiter in possible_delimiters}

    for line in lines:
        for delimiter in possible_delimiters:
            delimiter_counts[delimiter] += line.count(delimiter)

    # Choose the delimiter with the highest count
    detected_delimiter = max(delimiter_counts, key=delimiter_counts.get)
    return detected_delimiter


def load_file(path: str) -> DataFrame:
    spark = get_active_session()
    file_extension = path.split(".")[-1]

    if file_extension == "csv":
        df = spark.read.option("sep", detect_delimiter(path)).csv(
            path, header=True, inferSchema=True
        )
    elif file_extension == "json":
        df = spark.read.json(path, inferSchema=True)
    elif file_extension == "parquet":
        df = spark.read.parquet(path, inferSchema=True)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

    return df


def clean_column_name(df: DataFrame, column_name: Optional[str] = None) -> DataFrame:
    def clean_name(col_name) -> str:
        # Replace invalid characters with underscores
        return re.sub(r"[^a-zA-Z0-9_]", "_", col_name)

    if column_name:
        # Clean the specified column name
        new_col_name = clean_name(column_name)
        df = df.withColumnRenamed(column_name, new_col_name)
    else:
        # Clean all column names in the DataFrame
        for col_name in df.columns:
            new_col_name = clean_name(col_name)
            df = df.withColumnRenamed(col_name, new_col_name)

    return df
