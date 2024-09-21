#!/usr/bin/env python
# coding=utf-8
########################################################################
#
# Copyright (C) Baidu Ltd. All rights reserved. 
#
########################################################################

"""
Author: chenxiaoyan07@baidu.com
Date: 2024-09-10 01:38:00
LastEditTime: 2024-09-12 17:35:20
LastEditors: chenxiaoyan07@baidu.com
Description: 
FilePath: /festar-sdk/src/festar/framework/configs.py
"""
from enum import Enum
from typing import List, Optional, Union, Dict, Callable, Any

from festar.proto.spec import batch_data_source_pb2
from festar.proto.common import data_format_pb2


class FileFormatType(Enum):
    """
    FileFormatType枚举类型，用于表示文件格式类型"""
    UNKNOWN = 0
    CSV = 1
    PARQUET = 2
    SEQUENCE = 3
    
class ValueType(Enum):
    """
    ValueType枚举类型，用于表示值的类型"""
    INVALID = 0
    BYTES = 1
    STRING = 2
    INT32 = 3
    INT64 = 4
    DOUBLE = 5
    FLOAT = 6
    BOOL = 7
    UNIX_TIMESTAMP = 8
    BYTES_LIST = 11
    STRING_LIST = 12
    INT32_LIST = 13
    INT64_LIST = 14
    DOUBLE_LIST = 15
    FLOAT_LIST = 16
    BOOL_LIST = 17
    UNIX_TIMESTAMP_LIST = 18
    NULL = 19


class FileFormatConfig:
    """
    FileFormatConfig类，用于存储文件格式配置"""
    def __init__(self, config: Union['ParquetFormat', 'CsvFormat', 'SequenceFormat']):
        """
            Initializes the ParquetFormat, CsvFormat or SequenceFormat object.
        
        Args:
            config (Union['ParquetFormat', 'CsvFormat', 'SequenceFormat']): The configuration for the format. Can be a
                ParquetFormat, CsvFormat or SequenceFormat object.
        """
        self.config = config

    def to_proto(self) -> data_format_pb2.FileFormatConfig:
        """
            将当前对象转换为ProtoBuf格式的数据格式配置，返回一个data_format_pb2.FileFormatConfig类型的对象。
        如果当前对象是ParquetFormat实例，则将其转换为ProtoBuf中的parquet_config字段；
        如果当前对象是CsvFormat实例，则将其转换为ProtoBuf中的csv_config字段；
        如果当前对象是SequenceFormat实例，则将其转换为ProtoBuf中的sequence_config字段。
        
        Args:
            None
        
        Returns:
            data_format_pb2.FileFormatConfig (protobuf) - ProtoBuf格式的数据格式配置，包含了当前对象的相关信息。
        """
        proto = data_format_pb2.FileFormatConfig()
        if isinstance(self.config, ParquetFormat):
            proto.parquet_config.CopyFrom(self.config.to_proto())
        elif isinstance(self.config, CsvFormat):
            proto.csv_config.CopyFrom(self.config.to_proto())
        elif isinstance(self.config, SequenceFormat):
            proto.sequence_config.CopyFrom(self.config.to_proto())
        return proto

    @classmethod
    def from_proto(cls, proto: data_format_pb2.FileFormatConfig):
        """
            从 FileFormatConfig Protobuf 对象中创建一个 FileFormatConfig 实例。
        如果 proto 没有指定任何配置，则会引发 ValueError。
        
        Args:
            proto (data_format_pb2.FileFormatConfig): Protobuf 格式的 FileFormatConfig 对象。
        
        Raises:
            ValueError: 如果 proto 没有指定任何配置。
        
        Returns:
            FileFormatConfig: 包含 proto 中指定配置的 FileFormatConfig 实例。
        """
        if proto.HasField('parquet_config'):
            config = ParquetFormat.from_proto(proto.parquet_config)
        elif proto.HasField('csv_config'):
            config = CsvFormat.from_proto(proto.csv_config)
        elif proto.HasField('sequence_config'):
            config = SequenceFormat.from_proto(proto.sequence_config)
        else:
            raise ValueError("Unknown file format config type")
        return cls(config)

class ParquetFormat:
    """
    ParquetFormat类，用于存储Parquet格式配置"""
    def to_proto(self) -> data_format_pb2.FileFormatConfig.ParquetFormat:
        """
            将当前对象转换为 protobuf 格式的 ParquetFormat 类型，用于序列化和网络传输。
        
        Returns:
            data_format_pb2.FileFormatConfig.ParquetFormat (Protobuf): Protobuf 格式的 ParquetFormat 类型。
            包含所有可能需要的配置信息。
        """
        return data_format_pb2.FileFormatConfig.ParquetFormat()

    @classmethod
    def from_proto(cls, proto: data_format_pb2.FileFormatConfig.ParquetFormat):
        """
            从 Protobuf 格式的 ParquetFormat 对象中构建一个 FileFormatConfig.ParquetFormat 实例。
        
        Args:
            proto (data_format_pb2.FileFormatConfig.ParquetFormat): Protobuf 格式的 ParquetFormat 对象。
        
        Returns:
            FileFormatConfig.ParquetFormat: 一个 FileFormatConfig.ParquetFormat 实例，包含了从 proto 中解析出来的数据。
        
        Raises:
            无。
        """
        return cls()

class CsvFormat:
    """
    CsvFormat类，用于存储CSV格式配置"""
    def __init__(self, csv_options: Dict[str, str]):
        """
            初始化函数，用于设置CSV选项。
        
        Args:
            csv_options (Dict[str, str]): CSV选项字典，包含以下键值对：
                - delimiter (str, optional): CSV文件的分隔符，默认为','。
                - quotechar (str, optional): CSV文件中引号的字符，默认为'"'。
                - quoting (int, optional): 指定如何处理引号，可能的值有0（不使用引号）、1（所有字段都使用引号）和3（只有非空字段使用引号），默认为1。
                - doublequote (bool, optional): 指定是否将两个连续的引号解释为一个引号，默认为True。
                - escapechar (str, optional): CSV文件中转义字符，默认为None。
                - skipinitialspace (bool, optional): 指定是否跳过每行开头的任意空格，默认为False。
                - lineterminator (str, optional): 指定换行符，默认为'\n'。
                - dialect (str, optional): 指定CSV文件的语言方言，默认为'excel'。
        
        Returns:
            None.
        
        Raises:
            无.
        """
        self.csv_options = csv_options

    def to_proto(self) -> data_format_pb2.FileFormatConfig.CsvFormat:
        """
            将当前对象转换为 protobuf 格式的 CsvFormat 类型。
        
        Returns:
            data_format_pb2.FileFormatConfig.CsvFormat (protobuf): 包含当前 CSV 格式配置的 protobuf 对象。
            其中包括 csv_options，表示 CSV 文件的选项。
        """
        return data_format_pb2.FileFormatConfig.CsvFormat(
            csv_options=self.csv_options
        )

    @classmethod
    def from_proto(cls, proto: data_format_pb2.FileFormatConfig.CsvFormat):
        """
            从 protobuf 格式的 CSV 配置对象转换为当前类实例。
        
        Args:
            proto (data_format_pb2.FileFormatConfig.CsvFormat): protobuf 格式的 CSV 配置对象。
        
                - csv_options (Dict[str, Any]): CSV 文件的选项，包括以下字段：
                  - delimiter (str, optional): 用于分隔列的字符串，默认为 ','。
                  - quote (str, optional): 用于引用字符串中包含分隔符或行结束符的字符串，默认为 '"'。
                  - escape (str, optional): 用于转义引用字符串中的引用字符的字符串，默认为 None。
                  - header (bool, optional): 指示是否有一个标题行，默认为 False。
                  - null_values (List[str], optional): 表示空值的字符串列表，默认为 ['', 'NA']。
                  - skip_rows (int, optional): 跳过开头的行数，默认为 0。
                  - skip_columns (int, optional): 跳过开头的列数，默认为 0。
                  - comment (str, optional): 注释字符串，默认为 '#'。
                  - encoding (str, optional): 编码方式，默认为 'utf-8'。
        
        Returns:
            CsvFormat (CsvFormat): 当前类实例，包含从 protobuf 格式的 CSV 配置对象中解析出来的所有信息。
        """
        return cls(dict(proto.csv_options))

class SequenceFormat:
    """
    SequenceFormat类，用于存储序列格式配置"""
    def to_proto(self) -> data_format_pb2.FileFormatConfig.SequenceFormat:
        """
            将当前对象转换为 protobuf 格式的字节数组。
        
        Returns:
            data_format_pb2.FileFormatConfig.SequenceFormat: protobuf 格式的字节数组，表示当前对象。
        """
        return data_format_pb2.FileFormatConfig.SequenceFormat()

    @classmethod
    def from_proto(cls, proto: data_format_pb2.FileFormatConfig.SequenceFormat):
        """
            从 Protobuf 对象中创建 SequenceFormat 实例。
        
        Args:
            proto (data_format_pb2.FileFormatConfig.SequenceFormat): Protobuf 对象，包含序列格式的配置信息。
        
        Returns:
            SequenceFormat: 返回一个 SequenceFormat 实例，其中包含了从 proto 中解析出来的序列格式相关的配置信息。
        """
        return cls()

class IcebergConfig:
    """
    IcebergConfig类，用于存储Iceberg格式配置"""
    def __init__(self, table_name: str, partition_field: str, partition_value: str, snapshot_id: str):
        """
            Initializes a Partition object with the given parameters.
        
        Args:
            table_name (str): The name of the table that the partition belongs to.
            partition_field (str): The field in the table that is used for partitioning.
            partition_value (str): The value of the partition field for this partition.
            snapshot_id (str): The ID of the snapshot that created this partition.
        
        Raises:
            None.
        
        Returns:
            None. (Initialization method)
        """
        self.table_name = table_name
        self.partition_field = partition_field
        self.partition_value = partition_value
        self.snapshot_id = snapshot_id

    def to_proto(self) -> batch_data_source_pb2.BatchSourceConfig.IcebergConfig:
        """
            将当前对象转换为 protobuf 格式的 BatchSourceConfig.IcebergConfig 类型，用于序列化和网络传输。
        
        Returns:
            batch_data_source_pb2.BatchSourceConfig.IcebergConfig (protobuf) – 包含以下字段：
                - table_name (str) – Iceberg 表名称；
                - partition_field (str, optional) – Iceberg 分区字段，默认值为 None；
                - partition_value (str, optional) – Iceberg 分区值，默认值为 None；
                - snapshot_id (int, optional) – Iceberg 快照 ID，默认值为 None。
        
        Raises:
            无。
        """
        return batch_data_source_pb2.BatchSourceConfig.IcebergConfig(
            table_name=self.table_name,
            partition_field=self.partition_field,
            partition_value=self.partition_value,
            snapshot_id=self.snapshot_id
        )

    @classmethod
    def from_proto(cls, proto: batch_data_source_pb2.BatchSourceConfig.IcebergConfig):
        """
            从 protobuf 格式的 IcebergConfig 对象中创建 BatchIcebergConfig 实例。
        
        Args:
            proto (batch_data_source_pb2.BatchSourceConfig.IcebergConfig):
                一个包含 IcebergConfig 信息的 protobuf 对象。
        
                - table_name (str, optional): Iceberg 表名称，默认为 None。
                - partition_field (str, optional): Iceberg 分区字段，默认为 None。
                - partition_value (str, optional): Iceberg 分区值，默认为 None。
                - snapshot_id (int, optional): Iceberg 快照 ID，默认为 None。
        
        Returns:
            BatchIcebergConfig (BatchDataSources.BatchIcebergConfig):
                一个包含 IcebergConfig 信息的 BatchIcebergConfig 实例。
        """
        return cls(
            table_name=proto.table_name,
            partition_field=proto.partition_field,
            partition_value=proto.partition_value,
            snapshot_id=proto.snapshot_id
        )

class AfsConfig:
    """
    AfsConfig类，用于存储AFS格式配置"""
    def __init__(self, uri: str, ugi: str, file_format: FileFormatType, file_format_config: 'FileFormatConfig'):
        """
            Initializes the class with the given parameters.
        
        Args:
            uri (str): The URI of the data source.
            ugi (str): The UGI of the user who is accessing the data source.
            file_format (FileFormatType): The format of the data source.
            file_format_config (FileFormatConfig): The configuration for the file format.
        
        Returns:
            None.
        """
        self.uri = uri
        self.ugi = ugi
        self.file_format = file_format
        self.file_format_config = file_format_config

    def to_proto(self) -> batch_data_source_pb2.BatchSourceConfig.AfsConfig:
        """
            将当前对象转换为 protobuf 格式的 BatchSourceConfig.AfsConfig 类型。
        
        Returns:
            batch_data_source_pb2.BatchSourceConfig.AfsConfig (Protobuf): 包含当前对象所有属性的 protobuf 对象。
            其中包括 uri（str）、ugi（str）、file_format（FileFormat）和 file_format_config（FileFormatConfig）等属性。
        """
        return batch_data_source_pb2.BatchSourceConfig.AfsConfig(
            uri=self.uri,
            ugi=self.ugi,
            file_format=self.file_format.value,
            file_format_config=self.file_format_config.to_proto()
        )

    @classmethod
    def from_proto(cls, proto: batch_data_source_pb2.BatchSourceConfig.AfsConfig):
        """
            从 protobuf 对象创建一个 BatchAfsConfig 实例。
        
        Args:
            proto (batch_data_source_pb2.BatchSourceConfig.AfsConfig):
                来自 protobuf 的 BatchAfsConfig 对象。
        
                - uri (str): AFS URI，包括文件名。
                - ugi (str, optional): Hadoop 用户组信息，默认为 None。
                - file_format (FileFormatType, optional): 数据格式类型，默认为 None。
                - file_format_config (FileFormatConfig, optional): FileFormatConfig 对象，默认为 None。
        
        Returns:
            BatchAfsConfig (object): BatchAfsConfig 实例。
        """
        return cls(
            uri=proto.uri,
            ugi=proto.ugi,
            file_format=FileFormatType(proto.file_format),
            file_format_config=FileFormatConfig.from_proto(proto.file_format_config)
        )
        

class RetryConfig:
    """
    RetryConfig类，用于存储重试策略"""
    def __init__(self, retry_times: int, timeoutSeconds: int):
        """
            初始化RetryPolicy类，设置重试次数和超时时间。
        
        Args:
            retry_times (int): 重试的次数，默认为3次。
            timeoutSeconds (int, optional): 每次请求的超时时间，单位为秒，默认为10秒。
        
        Returns:
            None
        """
        self.retry_times = retry_times
        self.timeoutSeconds = timeoutSeconds