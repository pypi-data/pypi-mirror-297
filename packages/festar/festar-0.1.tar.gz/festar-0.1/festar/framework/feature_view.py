#!/usr/bin/env python
# coding=utf-8
########################################################################
#
# Copyright (C) Baidu Ltd. All rights reserved. 
#
########################################################################

"""
Author: chenxiaoyan07@baidu.com
Date: 2024-09-10 20:25:59
LastEditTime: 2024-09-12 17:37:34
LastEditors: chenxiaoyan07@baidu.com
Description: 
FilePath: /festar-sdk/src/festar/framework/feature_view.py
"""
from pandas import DataFrame
from typing import List, Dict, Any, Optional, Callable
from google.protobuf.struct_pb2 import Struct
from google.protobuf.json_format import MessageToDict, ParseDict
from google.protobuf.duration_pb2 import Duration
from pyspark.sql import SparkSession

from festar.core.conf import festar_config
from festar.festar_context import FestarContext
from festar.framework.entity import Entity
from festar.framework.configs import 
from festar.framework.transformation import Transformation, TransformationMode
from festar.framework.base_festar_object import BaseFestarObject, ObjectSource
from festar.framework.data_source import BatchDataSource

from festar.proto.resource import custom_resource_pb2
from festar.proto.spec import batch_feature_view_pb2
from festar.proto.common.field_pb2 import Field
from festar.proto.spec.trigger_pb2 import TriggerType



class Metrics:
    """
    A class used to represent metrics information for a batch feature view."""
    def __init__(
        self,
        name,
        sources: List[BatchDataSource] = [],
        views: List['BatchFeatureView'] = [],
        function: Callable = None,
        json_output: str = "",
        check_values: Dict[str, str] = {},
    ):  
        """
            Initializes a BatchIngestionJob instance.
        
        Args:
            name (str): The name of the job.
            sources (List[BatchDataSource], optional): A list of data sources to be ingested. Defaults to [].
            views (List[BatchFeatureView], optional): A list of feature views to be ingested. Defaults to [].
            function (Callable, optional): An optional transformation function that takes in a dictionary of
                features and outputs a dictionary of transformed features. Defaults to None.
            json_output (str, optional): A JSON string representing the expected output of the transformation
                function. Defaults to "".
            check_values (Dict[str, str], optional): A dictionary mapping feature names to their expected values.
                Defaults to {}.
        
        Raises:
            TypeError: If any of the arguments are not of the correct type.
        """
        self.name = name
        self.sources = sources
        self.views = views
        self.transformation = Transformation(function=function)
        self.json_output = json_output
        self.check_values = check_values

    def to_proto(self) -> batch_feature_view_pb2.Metrics:
        """
            将当前对象转换为 protobuf 格式的 Metrics 类型。
        
        Args:
            无参数，此函数不需要传入任何参数。
        
        Returns:
            batch_feature_view_pb2.Metrics (protobuf):
                Metrics类型，包含以下字段：
                1. name (str): 指标名称。
                2. sources (List[batch_feature_view_pb2.Source]): 来源列表，每个元素是一个 Source 类型的 protobuf 消息。
                3. views (List[batch_feature_view_pb2.View]): 视图列表，每个元素是一个 View 类型的 protobuf 消息。
                4. transformation (batch_feature_view_pb2.Transformation): 转换信息，是一个 Transformation 类型的 protobuf 消息。
                5. json_output (bool): 是否输出 JSON 格式结果。默认为 False。
                6. check_values (bool): 是否检查值。默认为 True。
        
        返回值是一个 protobuf 格式的 Metrics 类型，包含了当前对象中所有相关信息。
        """
        return batch_feature_view_pb2.Metrics(
            name=self.name,
            sources=[source.to_proto() for source in self.sources],
            views=[view.to_proto() for view in self.views],
            transformation=self.transformation.to_proto(),
            json_output=self.json_output,
            check_values=self.check_values
        )

    @classmethod
    def from_proto(cls, proto: batch_feature_view_pb2.Metrics) -> 'Metrics':
        """
            从 protobuf Metrics 对象创建 Metrics 实例。
        参数：
            proto (batch_feature_view_pb2.Metrics): protobuf Metrics 对象。
            返回值 (Metrics): Metrics 类的实例，包含从 protobuf 对象中提取的属性。
        """
        return cls(
            name=proto.name,
            sources=[BatchDataSource.from_proto(source) for source in proto.sources],
            views=[BatchFeatureView.from_proto(view) for view in proto.views],
            transformation=Transformation.from_proto(proto.transformation),
            json_output=proto.json_output,
            check_values=dict(proto.check_values)
        )

class Checker:
    """
    A class used to represent a checker which can be attached to a batch feature view."""
    def __init__(
        self,
        level: batch_feature_view_pb2.Level,
        alert: batch_feature_view_pb2.Alert,
        name: str,
        condition: List[str]
    ):
        """
            Initializes a BatchFeatureView object.
        
        Args:
            level (batch_feature_view_pb2.Level): The level of the feature view.
                Possible values are "BATCH" and "REALTIME".
            alert (batch_feature_view_pb2.Alert): The alert configuration for the feature view.
                Possible values are "NO_ALERT", "ERROR", and "WARNING".
            name (str): The name of the feature view.
            condition (List[str]): A list of conditions that must be met in order to trigger an alert.
                Each condition is a string representing a boolean expression.
                For example, "a > b" or "a == b".
                If any of these conditions evaluate to False, an alert will be triggered.
                Defaults to an empty list if not provided.
        
        Raises:
            ValueError: If `level` is not one of "BATCH" or "REALTIME".
            ValueError: If `alert` is not one of "NO_ALERT", "ERROR", or "WARNING".
        """
        self.level = level
        self.alert = alert
        self.name = name
        self.condition = condition

    def to_proto(self) -> batch_feature_view_pb2.Checker:
        """
            将当前对象转换为 protobuf 格式的 Checker 对象，用于序列化和网络传输。
        
        Returns:
            batch_feature_view_pb2.Checker (google.cloud.aiplatform.v1beta1.batch_feature_view_pb2.Checker):
                Checker类型的 protobuf 消息，包含了检查器的基本信息，如名称、条件等。
                - level (int): 检查器的级别，取值范围为0~3，分别代表严重性从高到低为WARNING、ERROR、CRITICAL和FATAL。
                - alert (int): 检查器的提醒方式，取值范围为0~2，分别代表不提醒、通过电子邮件提醒和通过电话提醒。
                - name (str): 检查器的名称，必须是唯一的。
                - condition (str): 检查器的条件，可以是任何字符串，例如 SQL 语句或者 Python 表达式。
        """
        return batch_feature_view_pb2.Checker(
            level=batch_feature_view_pb2.Level.Value(self.level.name),
            alert=batch_feature_view_pb2.Alert.Value(self.alert.name),
            name=self.name,
            condition=self.condition
        )

    @classmethod
    def from_proto(cls, proto: batch_feature_view_pb2.Checker) -> 'Checker':
        """
            从 protobuf 对象转换为 Checker 类实例。
        
        Args:
            proto (batch_feature_view_pb2.Checker): protobuf 对象，包含检查器的信息。
                level (str): 检查器级别，可选值为 "WARNING"、"ERROR"。
                alert (str): 警告等级，可选值为 "INFO"、"WARNING"、"ERROR"。
                name (str, optional): 检查器名称，默认为 None。
                condition (List[str], optional): 检查条件列表，默认为空列表。
        
        Returns:
            Checker (Checker): Checker 类实例，包含 protobuf 对象中的信息。
        """
        return cls(
            level=batch_feature_view_pb2.Level[batch_feature_view_pb2.Level.Name(proto.level)],
            alert=batch_feature_view_pb2.Alert[batch_feature_view_pb2.Alert.Name(proto.alert)],
            name=proto.name,
            condition=list(proto.condition)
        )
        

class FeatureView(BaseFestarObject):
    """
    A class representing a Festar object.
    """
    def __init__(
        self, 
        name: str, 
        id: str, 
        owner: str, 
        workspace: str, 
        description: Optional[str] = None,
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
    
    
class BatchFeatureView(FeatureView):
    """
    A class representing a Festar object.
    """
    def __init__(
        self,
        name: str,
        entities: List[Entity],
        sources: List[BatchDataSource],
        views: List['BatchFeatureView'],
        schema: List[Field],
        description: str,
        owner: str,
        workspace: str = "default",
        ttl: Optional[Duration] = None,
        offline_store: bool = False,
        partition_field: Optional[Field] = None,
        trigger: TriggerType = TriggerType.MANUAL,
        transformation_func: Optional[Callable] = None,
        transformation_mode: Optional[TransformationMode] = TransformationMode.PYTHON,
        metrics: List[Metrics] = None,
        checkers: List[Checker] = None,
        id: Optional[str] = None,
        source: ObjectSource = ObjectSource.LOCAL
    ):
        """
            Args:
            name (str): Feature group name.
            entities (List[Entity]): Entities that are part of the feature group.
            sources (List[BatchDataSource]): Data sources that are part of the feature group.
            views (List[BatchFeatureView]): Batch feature views that are part of the feature group.
            schema (List[Field]): Schema for the feature group.
            description (str, optional): Description of the feature group. Defaults to "".
            owner (str, optional): Owner of the feature group. Defaults to "".
            workspace (str, optional): Workspace where the feature group is located. Defaults to "default".
            ttl (Optional[Duration], optional): Time-to-live duration for the feature group. Defaults to None.
            offline_store (bool, optional): Whether the feature group has an offline store. Defaults to False.
            partition_field (Optional[Field], optional): Partition field for the feature group. Defaults to None.
            trigger (TriggerType, optional): Trigger type for the feature group. Defaults to TriggerType.MANUAL.
            transformation (Optional[Transformation], optional): Transformation for the feature group. Defaults to None.
            metrics (List[Metrics], optional): Metrics for the feature group. Defaults to [].
            checkers (List[Checker], optional): Checkers for the feature group. Defaults to [].
            id (Optional[str], optional): Feature group unique identifier. Defaults to None.
            source (ObjectSource, optional): Source of the object. Defaults to ObjectSource.LOCAL.
        Raises:
            ValueError: If the provided schema does not contain a primary key.
        """
        super().__init__(name, owner, workspace, description, id, source)
        self.entities = entities
        self.sources = sources
        self.views = views
        self.schema = schema
        self.ttl = ttl
        self.offline_store = offline_store
        self.partition_field = partition_field
        self.trigger = trigger
        self.transformation_func = transformation_func
        self.transformation_mode = transformation_mode
        self.metrics = metrics or []
        self.checkers = checkers or []


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
    def from_proto(cls, proto: custom_resource_pb2.CustomResource, source: ObjectSource) -> 'BatchFeatureView':
        """
            从 CustomResource protobuf 对象中创建 BatchFeatureView 实例。
        
        Args:
            proto (custom_resource_pb2.CustomResource): 包含 CustomResource 信息的 protobuf 对象。
            source (ObjectSource): 特征视图来源，包括数据湖、数据库等。
        
        Returns:
            BatchFeatureView (str): BatchFeatureView 类的实例，包含特征视图的名称、命名空间、所有者、工作区、描述、ID 等属性。
            **spec_dict (dict): 特征视图的配置字典，包括特征列、数据存储和时间窗口等信息。
        
        Raises:
            无。
        """
        spec_dict = cls._spec_from_proto(proto.spec)
        metadata = proto.metadata
        return cls(
            name=metadata.name,
            owner=metadata.labels.owner,
            workspace=metadata.labels.workspace,
            description=metadata.labels.description,
            id=metadata.labels.id,
            source=source,
            **spec_dict
        )

    def get_kind(self) -> str:
        """
            获取特征视图的类型，此处为"BatchFeatureView"。
        
        Returns:
            str - 返回一个字符串，值为"BatchFeatureView"。
        """
        return "BatchFeatureView"

    def _spec_to_proto(self) -> Struct:
        """
            将特征视图的规格转换为Protobuf结构体。
        
        Args:
            self (FeatureView): FeatureView实例，用于获取特征视图的属性。
        
        Returns:
            Struct (google.protobuf.struct_pb2.Struct): Protobuf结构体，包含特征视图的所有属性。
            其中，每个属性都是一个字典，键值对分别表示属性名和属性值。
        
        Raises:
            无。
        """
        transformation = Transformation(
            function=self.transformation_func,
            mode=self.transformation_mode
        ) if self.transformation_func else None
        
        spec = batch_feature_view_pb2.BatchFeatureViewSpec(
            ttl=self.ttl,
            offline_store=self.offline_store,
            entities=[entity.to_proto() for entity in self.entities],
            sources=[source.to_proto() for source in self.sources],
            views=[view.to_proto() for view in self.views],
            schema=[field.to_proto() for field in self.schema],
            partition_field=self.partition_field.to_proto() if self.partition_field else None,
            trigger=self.trigger.to_proto() if self.trigger else None,
            transformation=self.transformation.to_proto() if self.transformation else None,
            metrics=[metric.to_proto() for metric in self.metrics],
            checkers=[checker.to_proto() for checker in self.checkers]
        )
        return MessageToDict(spec, preserving_proto_field_name=True)

    @classmethod
    def _spec_from_proto(cls, spec: Struct) -> Dict[str, Any]:
        """
            将 protobuf 格式的 BatchFeatureViewSpec 转换为字典形式。
        字典中包含以下键值对：
            - ttl (int): 缓存时间，单位为秒。
            - offline_store (Union[OfflineStoreConfig, str]): 离线存储配置，可以是 OfflineStoreConfig 或者字符串类型。
            - entities (List[Entity]): 实体列表，每个元素都是 Entity 类型。
            - sources (List[BatchDataSource]): 数据源列表，每个元素都是 BatchDataSource 类型。
            - views (List[BatchFeatureView]): 批处理特征视图列表，每个元素都是 BatchFeatureView 类型。
            - schema (List[Field]): 字段列表，每个元素都是 Field 类型。
            - partition_field (Optional[Field]): 分区字段，如果有则是 Field 类型，否则为 None。
            - trigger (Optional[Trigger]): 触发器，如果有则是 Trigger 类型，否则为 None。
            - transformation (Optional[Transformation]): 变换，如果有则是 Transformation 类型，否则为 None。
            - metrics (List[Metrics]): 指标列表，每个元素都是 Metrics 类型。
            - checkers (List[Checker]): 检查器列表，每个元素都是 Checker 类型。
        
        Args:
            spec (Struct): protobuf 格式的 BatchFeatureViewSpec。
        
        Returns:
            Dict[str, Any]: 字典形式的 BatchFeatureViewSpec。
        """
        spec_proto = batch_feature_view_pb2.BatchFeatureViewSpec()
        ParseDict(spec, spec_proto)
        return {
            'ttl': spec_proto.ttl,
            'offline_store': spec_proto.offline_store,
            'entities': [Entity.from_proto(e) for e in spec_proto.entities],
            'sources': [BatchDataSource.from_proto(s) for s in spec_proto.sources],
            'views': [BatchFeatureView.from_proto(v) for v in spec_proto.views],
            'schema': [Field.from_proto(f) for f in spec_proto.schema],
            'partition_field': (
                Field.from_proto(spec_proto.partition_field) 
                if spec_proto.HasField('partition_field')
                else None
            ),
            'trigger': (
                TriggerType.from_proto(spec_proto.trigger)
                if spec_proto.HasField('trigger')
                else None
            ),
            'transformation': (
                Transformation.from_proto(spec_proto.transformation)
                if spec_proto.HasField('transformation')
                else None
            ),
            'metrics': [Metrics.from_proto(m) for m in spec_proto.metrics],
            'checkers': [Checker.from_proto(c) for c in spec_proto.checkers]
        }
    
    def get_dataframe(self) -> DataFrame:
        """
            获取batchfeatureview的数据。
        
        Returns:
            DataFrame: 特征视图的数据框架。
            
        Raises:
            无。
        """
        config = IcebergConfig(
            table=self.name,
            database=self.info.workspace,
        )
        data_source = BatchDataSource(
            name=self.name,
            owner=self.info.owner,
            workspace=self.info.workspace,
            description=self.info.description,
            id=self.info.id,
            source=self.info.source,
            config=config
        )
        return data_source.get_dataframe()
    
    
    def run_transformation(self) -> DataFrame:
        """
            运行转换函数，将所有数据源和视图合并为一个 DataFrame，然后返回结果。
        如果没有设置转换函数，则直接返回合并后的 DataFrame。
        
        Args:
            start_date (str): 起始日期字符串，格式为 'YYYY-MM-DD'。
            end_date (str): 终止日期字符串，格式为 'YYYY-MM-DD'。
        
        Returns:
            DataFrame: 经过转换函数处理后的 DataFrame，如果没有转换函数则与输入相同。
        """
        spark = FestarContext().get_spark_session()
        
        source_dfs = {source.name: source.get_dataframe() for source in self.sources}
        view_dfs = {view.name: view.get_dataframe() for view in self.views}
        
        if self.transformation_func:
            result_df = self._apply_transformation(spark, source_dfs, view_dfs)
        else:
            raise ValueError("Transformation function is not set.")

        return result_df

    def _apply_transformation(self, spark: SparkSession, df: DataFrame) -> DataFrame:
        """
            使用指定参数执行转换函数，并返回结果。"""
        func_params = {}
        for source in self.sources:
            func_params[source.name] = source_dfs[source.name]
        for view in self.views:
            func_params[view.name] = view_dfs[view.name]

        if self.transformation_mode == TransformationMode.PYTHON:
            # 对于 Python 模式，需要对每一行应用转换函数
            def map_func(row):
                row_dict = row.asDict()
                return self.transformation_func(**row_dict, **func_params)
            return spark.createDataFrame(spark.sparkContext.emptyRDD(), self.schema).rdd.map(map_func).toDF()
        
        elif self.transformation_mode == TransformationMode.PANDAS:
            # 对于 Pandas 模式，需要将 Spark DataFrame 转换为 Pandas DataFrame
            pandas_params = {k: v.toPandas() if isinstance(v, DataFrame) else v for k, v in func_params.items()}
            result = self.transformation_func(**pandas_params)
            return spark.createDataFrame(result)
        
        elif self.transformation_mode == TransformationMode.PYSPARK:
            # 对于 PySpark 模式，我们可以直接传递 Spark DataFrame
            return self.transformation_func(**func_params)
        
        else:
            raise ValueError(f"Unsupported transformation mode: {self.transformation_mode}")

    def run_transformation_and_save(self):
        """执行计算和存储
        """
        pass
    
    def run_transformation_save_and_calculate_metrics(self):
        """执行计算、存储和指标分析
        """
        pass
    
    def run_transformation_save_metrics_and_checker(self):
        """执行计算、存储、指标分析和检查
        """
        pass
    
    def _apply_checkers(self, df: DataFrame):
        """
            对DataFrame进行检查，并返回一个包含错误信息的字典。如果没有错误，则返回None。
        该函数会调用所有已注册的检查器，以确定是否存在任何问题。
        
        Args:
            df (DataFrame): 需要进行检查的DataFrame。
        
        Returns:
            Optional[Dict[str, str]]: 如果存在错误，则返回一个包含错误信息的字典；如果不存在错误，则返回None。
        """
        for checker in self.checkers:
            # 实现检查器逻辑
            pass

    def _calculate_metrics(self, df: DataFrame):
        """
            根据给定的DataFrame，对每个指标进行计算。
        该函数需要被子类重写以实现具体的指标计算逻辑。
        
        Args:
            df (DataFrame): 包含了所有样本的DataFrame，其中包括特征和目标值等信息。
        
        Returns:
            None，该函数不返回任何结果，而是直接在原Dataframe上修改指标列。
        """
        for metric in self.metrics:
            # 实现指标计算逻辑
            pass

def batch_feature_view(**kwargs):
    """
    装饰器函数，用于创建BatchFeatureView实例。"""
    def decorator(func):
        import inspect
        func_params = inspect.signature(func).parameters.keys()

        # 验证函数参数是否与 sources 和 views 匹配
        sources = kwargs.get('sources', [])
        views = kwargs.get('views', [])
        expected_params = set(s.name for s in sources) | set(v.name for v in views)
        if not expected_params.issubset(func_params):
            missing_params = expected_params - set(func_params)
            raise ValueError(f"Transformation function is missing parameters: {', '.join(missing_params)}")

        feature_view = BatchFeatureView(
            name=kwargs['name'],
            entities=kwargs['entities'],
            sources=kwargs['sources'],
            views=kwargs.get('views', []),
            schema=kwargs['schema'],
            description=kwargs['description'],
            owner=kwargs['owner'],
            workspace=kwargs.get('workspace', festar_config.get('default_workspace')),
            ttl=kwargs.get('ttl'),
            offline_store=kwargs.get('offline_store', False),
            partition_field=kwargs.get('partition_field'),
            trigger=kwargs.get('trigger'),
            transformation_mode=transformation_mode,
            transformation_func=func,
            metrics=kwargs.get('metrics', []),
            checkers=kwargs.get('checkers', []),
            id=kwargs.get('id'),
            source=ObjectSource.LOCAL
        )
        return feature_view
    return decorator