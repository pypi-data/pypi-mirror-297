#!/usr/bin/env python
# coding=utf-8
########################################################################
#
# Copyright (C) Baidu Ltd. All rights reserved. 
#
########################################################################

"""
Author: chenxiaoyan07@baidu.com
Date: 2024-09-10 00:28:35
LastEditTime: 2024-09-11 15:02:45
LastEditors: chenxiaoyan07@baidu.com
Description: 
FilePath: /festar-sdk/src/festar/festar_context.py
"""
import logging
import pyspark
from pyspark.sql import SparkSession
from contextlib import contextmanager
from typing import Dict, Any, Optional
from festar.core.conf import festar_config

from festar._internal.sdk_decorators import sdk_public_method
from festar.core.materialization.spark.spark_utils import get_or_create_spark_session


logger = logging.getLogger(__name__)

@contextmanager
def festar_context(**kwargs):
    """
    一个上下文管理器，用于在执行代码块时修改festar配置。
    该函数接受任意数量的键值对参数，其中每个键是一个字符串，表示要修改的festar配置项，
    而每个值是一个可以转换为str类型的对象，表示新的配置值。
    当代码块被执行后，将会自动还原所有修改过的festar配置项到原始状态。
    
    Args:
        **kwargs (dict, optional): 键值对参数，默认为{}. 其中每个键是一个字符串，表示要修改的festar配置项，
            而每个值是一个可以转换为str类型的对象，表示新的配置值。默认为{}.
    
    Yields:
        None: 无返回值，直接进入代码块执行。
    
    Raises:
        None: 不会引发任何异常。
    
    Returns:
        None: 无返回值，直接进入代码块执行。
    """
    original_values = {}
    for key, value in kwargs.items():
        original_values[key] = festar_config.get(key)
        festar_config.set(key, value)
    try:
        yield
    finally:
        for key, value in original_values.items():
            festar_config.set(key, value)
            

class FestarContext:
    """
    Execute Spark SQL queries; access various utils.
    """

    _current_context_instance: Optional["FestarContext"] = None
    _config: Dict[str, Any] = {}

    def __init__(self, spark: SparkSession):
        """
            Args:
            spark (SparkSession): Spark session instance.
        """
        self._spark = spark

    @classmethod
    def _set_config(cls, custom_spark_options=None):
        """
        Sets the configs for FestarContext instance.
        To take effect it must be called before any calls to FestarContext.get_instance().

        :param custom_spark_options: If spark session gets created by FestarContext, custom spark options/
        """
        cls._config = {"custom_spark_options": custom_spark_options}

    @classmethod
    @sdk_public_method
    def get_instance(cls) -> "FestarContext":
        """
        Get the singleton instance of FestarContext.
        """
        # If the instance doesn't exist, creates a new FestarContext from
        # an existing Spark context. Alternatively, creates a new Spark context on the fly.
        if cls._current_context_instance is not None:
            return cls._current_context_instance
        else:
            return cls._generate_and_set_new_instance()

    @classmethod
    def set_global_instance(cls, instance: Optional["FestarContext"]):
        """
        Create the singleton instance of FestarContext from the provided spark session.
        """
        cls._current_context_instance = instance

    @classmethod
    def _generate_and_set_new_instance(cls) -> "FestarContext":
        """
            生成一个新的Spark会话，并将其设置为当前上下文实例。如果已经存在一个实例，则返回该实例。
        如果没有配置文件，则使用默认配置。
        
        Args:
            None
        
        Returns:
            "FestarContext": 当前上下文实例，如果已经存在一个实例，则返回该实例。
        
        Raises:
            None
        """
        logger.debug("Generating new Spark session")
        spark = get_or_create_spark_session(
            cls._config.get("custom_spark_options"),
        )
        cls._current_context_instance = cls(spark)
        return cls._current_context_instance

    def get_spark_session(self) -> SparkSession:
        """
            获取SparkSession实例，如果不存在则创建一个新的。
        
        Args:
            None
        
        Returns:
            SparkSession (SparkSession): SparkSession实例。
        
        Raises:
            None
        """
        return self._spark


@sdk_public_method
def set_festar_spark_session(spark: SparkSession):
    """
    Configure Festar to use the provided SparkSession instead of its default.
    """
    FestarContext.set_global_instance(FestarContext(spark))
