#!/usr/bin/env python
# coding=utf-8
########################################################################
#
# Copyright (C) Baidu Ltd. All rights reserved. 
#
########################################################################

"""
Author: chenxiaoyan07@baidu.com
Date: 2024-09-12 17:00:01
LastEditTime: 2024-09-12 17:11:06
LastEditors: chenxiaoyan07@baidu.com
Description: 
FilePath: /festar-sdk/src/festar/framework/data_source.py
"""

import logging
from typing import List, Optional, Union, Dict, Callable, Any
from google.protobuf.struct_pb2 import Struct
from google.protobuf.json_format import MessageToDict, ParseDict
from pyspark.sql import SparkSession

from festar.core.conf import festar_config
from festar.framework.base_festar_object import BaseFestarObject, ObjectSource
from festar.proto.resource import custom_resource_pb2
from festar.proto.spec import batch_data_source_pb2
from festar.proto.common import field_pb2, data_format_pb2, value_type_pb2
from festar.proto.spec import transformation_pb2, user_defined_function_pb2
from festar.proto.spec.batch_data_source_pb2 import BatchSourceType
from festar.framework.transformation import TransformationMode, Transformation
from festar.framework.configs import IcebergConfig, AfsConfig, ValueType
from festar.framework.data_frame import FestarDataFrame
from festar.festar_context import FestarContext


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DataSource(BaseFestarObject):
    """
    Abstract base class for all objects managed by Festar."""
    def __init__(
        self, 
        name: str, 
        owner: str, 
        workspace: str, 
        description: str, 
        id: Optional[str] = None, 
        source: ObjectSource = ObjectSource.LOCAL
    ):
        """
            Initializes a new instance of the `Object` class.
        
        Args:
            name (str): The name of the object.
            owner (str): The owner of the object.
            workspace (str): The workspace of the object.
            description (str): A brief description of the object.
            id (Optional[str], optional): An optional unique identifier for the object. Defaults to None.
            source (ObjectSource, optional): The source of the object. Defaults to ObjectSource.LOCAL.
        
        Raises:
            ValueError: If the `id` is not a valid UUID.
        """
        super().__init__(name, owner, workspace, description, id, source)

    def to_proto(self):
        """
            Converts the object into its protobuf representation.
        
        Raises:
            NotImplementedError: Always raised, as this is an abstract method and should be implemented by subclasses.
        
        Returns:
            NoneType: Always returns None, as there is no return value for this method.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @classmethod
    def from_proto(cls, proto):
        """
            Creates a new instance of this class from a protocol buffer message.
        
        Args:
            proto (google.protobuf.message.Message): A protocol buffer message representing the
                class to be instantiated.
        
        Raises:
            NotImplementedError: This method is not implemented in the base class and should be
                overridden by subclasses.
        
        Returns:
            BaseModel: An instance of the subclass that was created from the protocol buffer message.
        """
        raise NotImplementedError("Subclasses must implement this method")
    

class BatchDataSource(DataSource):
    """
    BatchDataSource represents a batch data source in Festar framework. 
    It contains information about the data source such as its name, type, configuration, schema, etc.
    """
    def __init__(
        self,
        name: str,
        type: int,
        config: Union['IcebergConfig', 'AfsConfig'],
        schema: List['Field'],
        owner: str = "",
        workspace: str = "default",
        description: Optional[str] = None,
        id: Optional[str] = None,
        post_processor: Optional[Callable] = None,
        mode: int = TransformationMode.PYTHON,
        timestamp_field: Optional[str] = None,
        timestamp_format: Optional[str] = None,
        source: ObjectSource = ObjectSource.LOCAL
    ):
        """
            Initializes a Table object with the given parameters.
        
        Args:
            name (str): The name of the table.
            type (int): The type of the table, which can be one of the following values:
                        1 - Iceberg table; 2 - AFS table.
            config (Union['IcebergConfig', 'AfsConfig']): The configuration for the table, which can be either an
                instance of IcebergConfig or AfsConfig.
            schema (List['Field']): The list of fields in the table schema. Each field is represented by an instance
                of Field.
            owner (str, optional): The owner of the table. Defaults to "".
            workspace (str, optional): The workspace where the table resides. Defaults to "default".
            description (Optional[str], optional): The description of the table. Defaults to None.
            id (Optional[str], optional): The unique identifier of the table. Defaults to None.
            post_processor (Optional[Callable], optional): A function that will be applied to the data after it has
                been transformed. Defaults to None.
            mode (int, optional): The transformation mode, which can be one of the following values:
                                  0 - No transformation; 1 - Python transformation; 2 - Spark transformation.
                                  Defaults to TransformationMode.PYTHON.
            timestamp_field (Optional[str], optional): The name of the timestamp field. Defaults to None.
            timestamp_format (Optional[str], optional): The format of the timestamp field. Defaults to None.
            source (ObjectSource, optional): The source of the object, which can be one of the following values:
                                             1 - Local file system; 2 - HDFS; 3 - S3; 4 - Azure Blob Storage;
                                             5 - Google Cloud Storage. Defaults to ObjectSource.LOCAL.
        
        Raises:
            ValueError: If the type is not one of the allowed values.
        """
        super().__init__(name, owner, workspace, description, id, source)
        self.type = type
        self.config = config
        self.schema = schema
        self.post_processor = post_processor
        self.mode = mode
        self.timestamp_field = timestamp_field
        self.timestamp_format = timestamp_format

    def to_proto(self) -> custom_resource_pb2.CustomResource:
        """
            将 CustomResource 对象转换为 protobuf 格式的 CustomResource 消息。
        
        Args:
            None
        
        Returns:
            custom_resource_pb2.CustomResource (protobuf): 包含自定义资源信息的 CustomResource 消息。
            - api_version (str): 自定义资源 API 版本，默认值为 festar_config['api_version']。
            - kind (str): 自定义资源类型，通过 get_kind() 方法获取。
            - metadata (custom_resource_pb2.ObjectMeta): 自定义资源元数据，由 info 属性转换得到。
            - spec (dict): 自定义资源规格，由 _spec_to_proto() 方法转换得到。
        
        Raises:
            None
        """
        return custom_resource_pb2.CustomResource(
            api_version=festar_config.get('api_version'),
            kind=self.get_kind(),
            metadata=self.info.to_proto(),
            spec=self._spec_to_proto()
        )

    @classmethod
    def from_proto(cls, proto: custom_resource_pb2.CustomResource, source: ObjectSource) -> 'BatchDataSource':
        """
            Creates a BatchDataSource instance from a CustomResource protobuf message.
        
        Args:
            proto (custom_resource_pb2.CustomResource): The CustomResource protobuf message.
            source (ObjectSource): The source of the object.
        
        Returns:
            BatchDataSource (Union[None, BatchDataSource]): An instance of BatchDataSource or None if the
                CustomResource is not a BatchDataSource.
        
        Raises:
            None
        """
        spec_dict = cls._spec_from_proto(proto.spec)
        metadata = proto.metadata
        
        post_processor = None
        mode = TransformationMode.PYTHON
        if 'post_processor' in spec_dict:
            try:
                post_processor = Transformation.from_proto(spec_dict['post_processor'])
                mode = spec_dict['post_processor'].transformation_mode
                Transformation.test_execution(post_processor, mode)
            except RuntimeError as e:
                logger.warning(f"Failed to create post_processor: {str(e)}. Proceeding without post-processor.")

        return cls(
            name=metadata.name,
            owner=metadata.labels.owner,
            workspace=metadata.labels.workspace,
            description=metadata.labels.description,
            id=metadata.labels.id,
            type=spec_dict['type'],
            config=cls._create_config_from_spec(spec_dict['config']),
            schema=[Field.from_proto(field) for field in spec_dict['schema']],
            post_processor=post_processor,
            mode=mode,
            timestamp_field=spec_dict.get('timestamp_field'),
            timestamp_format=spec_dict.get('timestamp_format'),
            source=source
        )

    def get_kind(self) -> str:
        """
            获取数据源类型，总是返回"BatchDataSource"。
        
        Args:
            None
            
        Returns:
            str (str): 返回一个字符串，固定为"BatchDataSource"。
            
        Raises:
            None
        """
        return "BatchDataSource"

    def _spec_to_proto(self) -> Struct:
        """
            将 BatchDataSource 的规格信息转换为 protobuf 的 Struct，返回该 Struct。
        包括数据源类型、配置、模式、字段列表、时间戳字段、时间戳格式以及后处理器和运行模式等信息。
        
        Args:
            None
        
        Returns:
            Struct (google.protobuf.struct_pb2.Struct):
                包含 BatchDataSource 规格信息的 Struct，包括：
                - type (str): 数据源类型，例如 "csv"、"parquet" 等。
                - config (google.protobuf.struct_pb2.Struct): 数据源配置，包括文件路径、分隔符等信息。
                - schema (List[Field]): 数据源中的字段列表，每个字段是一个 Field 对象。
                - timestamp_field (str, optional): 时间戳字段名称，默认为 None。
                - timestamp_format (str, optional): 时间戳格式，默认为 None。
                - post_processor (Transformation, optional): 后处理器，默认为 None。
                - mode (str, optional): 运行模式，默认为 None。
        
        Raises:
            None
        """
        batch_source_spec = batch_data_source_pb2.BatchDataSourceSpec(
            type=self.type,
            config=self._config_to_proto(),
            schema=[field.to_proto() for field in self.schema],
            timestamp_field=self.timestamp_field,
            timestamp_format=self.timestamp_format
        )

        if self.post_processor:
            transformation = Transformation(self.post_processor, self.mode)
            batch_source_spec.post_processor.CopyFrom(transformation.to_proto())
        # 将 BatchDataSourceSpec 转换为字典
        spec_dict = MessageToDict(batch_source_spec, preserving_proto_field_name=True)

        # 创建 Struct 并更新它
        result = Struct()
        result.update(spec_dict)
        return result

    @classmethod
    def _spec_from_proto(cls, spec: Struct) -> Dict[str, Any]:
        """
            将 protobuf 格式的 BatchDataSourceSpec 转换为字典形式。
        该方法主要用于从 protobuf 中解析出 BatchDataSourceSpec，并将其转换成 Python 字典。
        
        Args:
            spec (Struct, required): protobuf 格式的 BatchDataSourceSpec，包含了数据源的类型、配置、模式、时间戳字段等信息。
        
        Returns:
            Dict[str, Any]: 返回一个字典，包含以下键值对：
                    - type (str): 数据源的类型，如 "file"、"kafka" 等。
                    - config (Dict[str, Any]): 数据源的配置信息，如文件路径或 Kafka 地址等。
                    - schema (List[str]): 数据源的模式，表示每条记录的结构。
                    - timestamp_field (str, optional): 数据源的时间戳字段，如果存在则指定此字段。默认为 None。
                    - timestamp_format (str, optional): 数据源的时间戳格式，如果存在则指定此格式。默认为 None。
                    - post_processor (str, optional): 数据处理器的名称，如果存在则指定此处理器。默认为 None。
        """
        batch_source_spec = ParseDict(spec, batch_data_source_pb2.BatchDataSourceSpec())
        spec_dict = {
            'type': batch_source_spec.type,
            'config': batch_source_spec.config,
            'schema': list(batch_source_spec.schema),
            'timestamp_field': batch_source_spec.timestamp_field,
            'timestamp_format': batch_source_spec.timestamp_format
        }
        if batch_source_spec.HasField('post_processor'):
            spec_dict['post_processor'] = batch_source_spec.post_processor
        return spec_dict

    def _config_to_proto(self) -> batch_data_source_pb2.BatchSourceConfig:
        """
            将当前配置转换为Protobuf格式的BatchSourceConfig对象，返回该对象。
        如果当前配置是IcebergConfig类型，则将其转换为batch_data_source_pb2.IcebergConfig；
        如果当前配置是AfsConfig类型，则将其转换为batch_data_source_pb2.AfsConfig。
        
        Args:
            None
        
        Returns:
            batch_data_source_pb2.BatchSourceConfig (protobuf message): Protobuf格式的BatchSourceConfig对象，包含了当前配置信息。
        """
        config_proto = batch_data_source_pb2.BatchSourceConfig()
        if isinstance(self.config, IcebergConfig):
            config_proto.iceberg_config.CopyFrom(self.config.to_proto())
        elif isinstance(self.config, AfsConfig):
            config_proto.afs_config.CopyFrom(self.config.to_proto())
        return config_proto
    
    def get_dataframe(self, **kwargs: Any) -> FestarDataFrame:
        """
        使用 Spark 读取数据源并返回 DataFrame。

        :param kwargs: 额外的参数，可用于过滤或其他操作
        :return: Spark DataFrame
        """
        context = FestarContext.get_instance()
        spark = context._get_spark()
        if isinstance(self.config, IcebergConfig):
            return self._get_iceberg_dataframe(spark, **kwargs)
        elif isinstance(self.config, AfsConfig):  # AFS 路径
            return self._get_afs_dataframe(spark, **kwargs)
    
    def _get_iceberg_dataframe(self, spark: SparkSession, **kwargs: Any) -> FestarDataFrame:
        """
        使用 Iceberg 读取数据源并返回 DataFrame。
        """
        table = f"iceberg_ns.{self.config.database}.{self.config.table}"
        df = spark.read.table(table)
        return df
    
    def _get_afs_dataframe(self, spark: SparkSession, **kwargs: Any) -> FestarDataFrame:
        """
        使用 AFS 读取数据源并返回 DataFrame。
        """
        sc = spark.sparkContext
        sc._jsc.hadoopConfiguration().set("hadoop.job.ugi", self.config.ugi)
        df = spark.read.format(self.config.file_format).load(self.config.uri)
        return df

class Field:
    """
    Field类，用于描述数据源中的一个字段。
    """
    def __init__(self, name: str, value_type: ValueType):
        """
            初始化函数，用于设置变量名和值类型。
        
        Args:
            name (str): 变量的名称。
            value_type (ValueType): 变量的值类型，可以是ValueType枚举中的任意一种。
        
        Returns:
            None; 无返回值。
        """
        self.name = name
        self.value_type = value_type

    def to_proto(self) -> field_pb2.Field:
        """
            将当前对象转换为 protobuf 格式的 Field 对象。
        
        Args:
            无参数，不需要传入任何参数。
        
        Returns:
            field_pb2.Field (google.cloud.bigquery.migration.v2alpha.types.field_pb2):
                返回一个 protobuf 格式的 Field 对象，包含当前对象的名称和类型信息。
                - name (str): 字段的名称。
                - value_type (int): 字段的值类型，取值范围为 FieldValueType 枚举常量。
        
        返回值是 protobuf 格式的 Field 对象，可以直接用于 BigQuery API 的请求中。
        """
        return field_pb2.Field(
            name=self.name,
            value_type=self.value_type.value
        )

    @classmethod
    def from_proto(cls, proto: field_pb2.Field):
        """
            从 Field protobuf 对象创建 Field 实例。
        
        Args:
            proto (field_pb2.Field): Field protobuf 对象，包含字段名称和值类型等信息。
        
                - name (str): 字段名称。
                - value_type (ValueType): 字段的值类型，可以是 ValueType.INT、ValueType.STRING 等枚举值之一。
        
        Returns:
            Field: Field 实例，包含字段名称和值类型等信息。
        """
        return cls(
            name=proto.name,
            value_type=ValueType(proto.value_type)
        )
