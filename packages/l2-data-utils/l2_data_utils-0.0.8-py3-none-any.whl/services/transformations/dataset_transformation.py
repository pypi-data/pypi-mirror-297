from pyspark.sql.functions import col, when, greatest, datediff, expr
from pyspark.sql.types import TimestampType, DateType
from pyspark.sql import SparkSession, DataFrame

def update_cdc_timestamp(df, time_diff_threshold: int):
    timestamp_cols = [col.name for col in df.schema.fields if isinstance(col.dataType, (TimestampType, DateType)) and col.name != 'cdc_timestamp']
    if timestamp_cols:
        max_timestamp_per_row = None
        if len(timestamp_cols) > 1:
            max_timestamp_per_row = greatest(*[col(col_name) for col_name in timestamp_cols])
        else:
            max_timestamp_per_row = col(timestamp_cols[0])
            
        df = df.withColumn(
            'cdc_timestamp',
                when(
                    (col('cdc_timestamp').isNull()) | 
                    (datediff(col('cdc_timestamp'), max_timestamp_per_row) > time_diff_threshold), 
                    max_timestamp_per_row
                ).otherwise(col('cdc_timestamp'))
            )
        
    return df


def get_filtered_df_greater_equal_than(df, threshold: str, col_name: str):
    df_filtered = df.filter(col(col_name) >= threshold)
    return df_filtered


def set_cdc_timestamp_partition_month(df, alias_col_name: str):
    return df.withColumn(alias_col_name, expr("date_format(cdc_timestamp, 'yyyy-MM')"))