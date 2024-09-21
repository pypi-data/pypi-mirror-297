
from datetime import timedelta, datetime
from datetime import datetime
from pyspark.sql import Window
from pyspark.sql import functions as f
from pyspark.sql.types import *
import pandas as pd
import sys

__version__ = '0.0.7'
class spark_functions():
    def __init__(self, spark=None, health_table_name = None) -> None:
        self.spark = spark
        self.health_table_name = health_table_name
    def sample_function(self):
        print("Sample is working")
        pass

    def get_top_duplicates(self,df,col='customer_hash',n=2):
        return (df.groupBy(col)
                .agg(f.count(col).alias('count'))
                .orderBy(f.col('count').desc_nulls_last())
                .limit(n))

    def sdf_to_dwh(self,sdf,table_address,mode,mergeSchema = "true"):
        (sdf.write.mode(mode)
            .option("mergeSchema", mergeSchema)
            .saveAsTable(table_address))

    def sdf_fillDown(self,sdf,groupCol,orderCol,cols_to_fill):   
        window_spec = Window.partitionBy(groupCol).orderBy(orderCol)
        
        for column in cols_to_fill:
            # sdf = sdf.withColumn(column, f.last(f.col(column),ignorenulls=True).over(window))
            sdf = (sdf
                .withColumn(column,
                            f.last(column, ignorenulls=True).over(window_spec))
                )
        return sdf
    
    def sdf_fillUp(self,sdf,groupCol,orderCol,cols_to_fill):
        window_spec = Window.partitionBy(groupCol).orderBy(f.col(orderCol).desc_nulls_last())
        
        for column in cols_to_fill:
            # sdf = sdf.withColumn(column, f.last(f.col(column),ignorenulls=True).over(window))
            sdf = (sdf
                .withColumn(column,
                            f.last(column, ignorenulls=True).over(window_spec))
                )
        return sdf
    
    def sdf_fill_gaps(self,sdf,groupCol,orderCol,cols_to_fill,direction='both'):
        if direction == 'up':
            sdf = self.sdf_fillUp(sdf,groupCol,orderCol,cols_to_fill)
        elif direction == 'down':
            sdf = self.sdf_fillDown(sdf,groupCol,orderCol,cols_to_fill)
        else:
            sdf = self.sdf_fillDown(sdf,groupCol,orderCol,cols_to_fill)
            sdf = self.sdf_fillUp(sdf,groupCol,orderCol,cols_to_fill)
        return sdf
    
    def single_value_expr(partition_col, order_col, value_col, ascending=False):
        windowSpec = Window.partitionBy(partition_col).orderBy(order_col)
        if ascending:
            return f.first(f.when(f.col(order_col) == f.min(order_col).over(windowSpec), f.col(value_col)), True)
        else:
            return f.first(f.when(f.col(order_col) == f.max(order_col).over(windowSpec), f.col(value_col)), True)

    def read_dwh_table(self,table_name, last_update_column=None, save_health=True):
        sdf = self.spark.table(table_name)
        if save_health:
            try:
                last_update = sdf\
                                .filter(
                                f.col(last_update_column).cast('timestamp') < \
                                    (datetime.today()+timedelta(days=1)).strftime('%Y-%m-%d'))\
                                .select(f.max(f.col(last_update_column).cast('timestamp')).alias('last_update'))\
                                .collect()[0]['last_update']
                health_data = {'table_name': [table_name], 'last_update': [last_update]}
                health_sdf =  self.spark.createDataFrame(pd.DataFrame(data=health_data))
                self.sdf_to_dwh(health_sdf,self.health_table_name,'append')
            except: 
                pass
        return (sdf)

    def remove_duplicates_keep_latest(self,sdf, partition_col: str, order_col: str):
        """
        Removes duplicate rows based on the partition_col, keeping only the row with the highest value in order_col.

        Parameters:
        - df (DataFrame): The Spark DataFrame to process.
        - partition_col (str): The name of the column to partition the data (e.g., 'customer_hash').
        - order_col (str): The name of the column to order data within each partition (e.g., 'created_at').

        Returns:
        - DataFrame: A new DataFrame with duplicates removed based on partition_col, keeping only the latest record based on order_col.
        """
        # Define the window specification
        windowSpec = Window.partitionBy(partition_col).orderBy(f.col(order_col).desc_nulls_last())

        # Rank rows within each partition and filter to keep only the top-ranked row
        filtered_df = sdf.withColumn("row_number", f.row_number().over(windowSpec)) \
                        .filter(f.col("row_number") == 1) \
                        .drop("row_number")

        return filtered_df
    def remove_duplicates(self,sdf, partition_col: str, order_col: str, ascending = False):
        """
        Removes duplicate rows based on the partition_col, keeping only the row with the single value in order_col. 
        Ordering will beased on ascending variable.

        Parameters:
        - df (DataFrame): The Spark DataFrame to process.
        - partition_col (str): The name of the column to partition the data (e.g., 'customer_hash').
        - order_col (str): The name of the column to order data within each partition (e.g., 'created_at').
        - ascending (int): 1 means ascending order, 0 means descending order

        Returns:
        - DataFrame: A new DataFrame with duplicates removed based on partition_col, keeping only the latest record based on order_col.
        """
        # Define the window specification
        if ascending:
            windowSpec = Window.partitionBy(partition_col).orderBy(f.col(order_col).asc_nulls_last())
        else:
            windowSpec = Window.partitionBy(partition_col).orderBy(f.col(order_col).desc_nulls_last())

        # Rank rows within each partition and filter to keep only the top-ranked row
        filtered_df = sdf.withColumn("row_number", f.row_number().over(windowSpec)) \
                        .filter(f.col("row_number") == 1) \
                        .drop("row_number")

        return filtered_df
