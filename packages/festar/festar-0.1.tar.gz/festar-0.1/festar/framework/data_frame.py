"""
FestarDataFrame Definition
"""
from pyspark.sql import DataFrame as SparkDataFrame
import pandas as pd
from typing import Optional, Union
from abc import ABC
import attrs

@attrs.define(repr=False)
class FestarDataFrame(object):
    """
    A FestarDataFrame is a wrapper around either a pandas DataFrame or Spark
    """
    _pandas_df: Optional[pd.DataFrame] = None
    _spark_df: Optional[SparkDataFrame] = None

    @classmethod
    def _create(cls, df: Union[pd.DataFrame, SparkDataFrame]):
        """
        Create a FestarDataFrame from either a pandas DataFrame or Spark DataFrame
        """
        if isinstance(df, pd.DataFrame):
            return cls(pandas_df=df)
        elif isinstance(df, SparkDataFrame):
            return cls(spark_df=df)

        raise ValueError("df must be a pandas DataFrame or Spark DataFrame")
        
    def __getattr__(self, name):
        """
        Delegate to the underlying pandas DataFrame or Spark DataFrame
        """
        if self._pandas_df is not None:
            return getattr(self._pandas_df, name)
        elif self._spark_df is not None:
            return getattr(self._spark_df, name)
        return None

    def to_pandas(self) -> pd.DataFrame:
        """
        Convert the FestarDataFrame to a pandas DataFrame
        """
        if self._pandas_df is not None:
            return self._pandas_df
        elif self._spark_df is not None:
            return self._spark_df.toPandas()
        
        raise ValueError("No data to convert")