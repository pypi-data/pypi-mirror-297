#!/usr/bin/env python
# coding=utf-8
########################################################################
#
# Copyright (C) Baidu Ltd. All rights reserved. 
#
########################################################################

"""
Author: chenxiaoyan07@baidu.com
Date: 2024-09-10 01:49:59
LastEditTime: 2024-09-12 17:07:44
LastEditors: chenxiaoyan07@baidu.com
Description: 
FilePath: /festar-sdk/src/festar/framework/transformation.py
"""
import logging
from enum import Enum
from typing import Callable, Dict, Any, Optional
from festar.proto.spec import transformation_pb2
from festar.proto.spec.transformation_pb2 import TransformationMode
from festar.proto.spec import user_defined_function_pb2
from festar._internal.function_serialization import serialize_function, deserialize_function
from types import FunctionType, ModuleType
from dill.detect import globalvars, freevars

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class UserDefinedFunction:
    """
    UserDefinedFunction类表示一个用户自定义的函数，它由一个名称和一个主体组成。"""
    def __init__(self, name: str, body: str):
        """
            初始化函数，用于设置名称和体。
        
        Args:
            name (str): 函数的名称。
            body (str): 函数的主体。
        
        Returns:
            None; 无返回值。
        """
        self.name = name
        self.body = body

    def to_proto(self) -> user_defined_function_pb2.UserDefinedFunction:
        """
            将当前对象转换为 protobuf 格式的 UserDefinedFunction 类型。
        返回值 (user_defined_function_pb2.UserDefinedFunction):
            - name (str, required): 用户定义函数的名称。
            - body (str, required): 用户定义函数的主体，必须是一个有效的 JavaScript 表达式或字符串。
        """
        return user_defined_function_pb2.UserDefinedFunction(
            name=self.name,
            body=self.body
        )

    @classmethod
    def from_proto(cls, proto: user_defined_function_pb2.UserDefinedFunction) -> 'UserDefinedFunction':
        """
            从Protobuf格式的用户定义函数对象创建一个新的UserDefinedFunction实例。
        
        Args:
            proto (user_defined_function_pb2.UserDefinedFunction): Protobuf格式的用户定义函数对象。
        
                - name (str): 函数名称。
                - body (str): 函数体，可以是任何有效的SQL语句。
        
        Returns:
            UserDefinedFunction (str): 包含函数名称和函数体的UserDefinedFunction实例。
        """
        return cls(
            name=proto.name,
            body=proto.body
        )

    @classmethod
    def from_callable(cls, func: Callable) -> 'UserDefinedFunction':
        """
            从可调用对象创建一个 UserDefinedFunction 实例。
        
        Args:
            func (Callable): 可调用的函数，将被转换为 UserDefinedFunction。
        
        Returns:
            UserDefinedFunction: 新创建的 UserDefinedFunction 实例。
        
        Raises:
            None.
        """
        name = func.__name__
        body = serialize_function(func)
        return cls(name, body)
    

class Transformation:
    """
    A class representing a transformation that can be applied to data using Festar's SDK."""
    def __init__(self, function: Callable, mode: int = TransformationMode.PYTHON):
        """
            Initializes a new instance of the `Function` class.
        
        Args:
            function (Callable): The Python function to be serialized.
            mode (int, optional): The transformation mode. Defaults to TransformationMode.PYTHON.
                Can be either TransformationMode.PYTHON or TransformationMode.CSHARP.
        
        Raises:
            TypeError: If the provided function is not callable.
        """
        self.function = function
        self.mode = mode
        self.name = function.__name__
        self.body = serialize_function(function)

    def to_proto(self) -> transformation_pb2.TransformationSpec:
        """
            将当前对象转换为 protobuf 格式的 TransformationSpec。
        
        Returns:
            transformation_pb2.TransformationSpec (protobuf): 包含当前对象信息的 TransformationSpec 类型对象。
            - transformation_mode (str): 当前对象的转换模式，取值为 "USER_DEFINED_FUNCTION"。
            - user_function (user_defined_function_pb2.UserDefinedFunction): 用户自定义函数的相关信息，包括：
                - name (str): 函数名称。
                - body (str): 函数体（Python 代码）。
        
        Raises:
            无。
        
        Returns:
            无返回值，直接修改传入的 protobuf 对象。
        """
        return transformation_pb2.TransformationSpec(
            transformation_mode=self.mode,
            user_function=user_defined_function_pb2.UserDefinedFunction(
                name=self.name,
                body=self.body
            )
        )

    @classmethod
    def from_proto(cls, proto: transformation_pb2.TransformationSpec) -> Callable:
        """
            将 protobuf 格式的 TransformationSpec 转换为 Python 中的函数。
        该函数从 proto 中提取用户定义的函数并进行反序列化，然后返回一个可执行的函数。
        
        Args:
            proto (transformation_pb2.TransformationSpec): protobuf 格式的 TransformationSpec。
                包含用户定义的函数信息。
        
        Returns:
            Callable: 一个可执行的函数，它接收一个 pandas DataFrame 作为输入参数，并返回一个 pandas DataFrame 作为结果。
        
        Raises:
            None.
        """
        function = deserialize_function(
            proto.user_function.body,
            proto.user_function.name
        )
        # 我们不再返回 Transformation 对象，而是直接返回可执行的函数
        return function

    @classmethod
    def from_callable(cls, func: Callable, transformation_mode: TransformationMode) -> 'Transformation':
        """
            从可调用对象创建一个转换。
        
        Args:
            func (Callable): 可调用的函数，将会被应用于每个输入元素。
            transformation_mode (TransformationMode): 指定转换模式，有两种选择：'permissive'或'strict'。
                如果是'permissive'，则允许任何类型的输入，并且不会引发错误；如果是'strict'，则只接受特定类型的输入，否则会引发错误。
        
        Returns:
            Transformation (str): 返回一个新的Transformation实例。
        
        Raises:
            无。
        """
        user_function = UserDefinedFunction.from_callable(func)
        return cls(transformation_mode, user_function)
    
    @staticmethod
    def test_execution(function: Callable, mode: int):
        """
            测试函数的执行是否成功。如果失败，则引发RuntimeError异常。
        参数：
            function (Callable) - 要测试的函数
            mode (int) - 测试模式（0或1），用于确定要使用的输入值
        返回值：
            无返回值，但会在测试成功时记录一条信息日志，并在测试失败时引发RuntimeError异常
        """
        try:
            test_input = Transformation._create_test_input(mode)
            _ = function(test_input)
            logger.info(f"Successfully tested execution of {function.__name__}")
        except Exception as e:
            logger.error(f"Failed to execute {function.__name__}: {str(e)}")
            raise RuntimeError(f"Post-processor function {function.__name__} failed execution test") from e

    @staticmethod
    def _create_test_input(mode: int) -> Any:
        """
            创建测试输入，支持PySpark、pandas和python三种模式。
        如果mode为TransformationMode.PYSPARK，则返回一个pyspark.sql.DataFrame；
        如果mode为TransformationMode.PANDAS，则返回一个pandas.DataFrame；
        如果mode为TransformationMode.PYTHON，则返回一个list。
        其他情况下返回None。
        
        Args:
            mode (int): 转换模式，可选值包括：
                - TransformationMode.PYSPARK（0）：使用PySpark；
                - TransformationMode.PANDAS（1）：使用pandas；
                - TransformationMode.PYTHON（2）：使用Python原生数据类型。
        
        Returns:
            Any: 返回一个对象，可能是pyspark.sql.DataFrame、pandas.DataFrame或list，取决于mode的值。如果mode不在支持范围内，则返回None。
        """
        if mode == TransformationMode.PYSPARK:
            from pyspark.sql import SparkSession
            spark = SparkSession.builder.getOrCreate()
            return spark.createDataFrame([(1,)], ["id"])
        elif mode == TransformationMode.PANDAS:
            import pandas as pd
            return pd.DataFrame({"id": [1]})
        elif mode == TransformationMode.PYTHON:
            return [{"id": 1}]
        else:
            return None