#!/usr/bin/env python
# coding=utf-8
########################################################################
#
# Copyright (C) Baidu Ltd. All rights reserved. 
#
########################################################################

"""
Author: chenxiaoyan07@baidu.com
Date: 2024-09-09 23:02:39
LastEditTime: 2024-09-12 17:03:36
LastEditors: chenxiaoyan07@baidu.com
Description: 
FilePath: /festar-sdk/src/festar/framework/entity.py
"""
from typing import List, Dict, Any, Optional
from google.protobuf.struct_pb2 import Struct
from google.protobuf.json_format import MessageToDict, ParseDict

from festar.framework.base_festar_object import BaseFestarObject, ObjectSource
from festar.core.conf import festar_config
from festar.proto.resource import custom_resource_pb2
from festar.proto.spec import entity_pb2

class Entity(BaseFestarObject):
    """
    实体类，继承自BaseFestarObject，主要用于存储和管理实体相关的信息。"""
    def __init__(self, name: str, 
                 join_keys: List[str], 
                 owner: str = "",
                 workspace: str = "default", 
                 description: Optional[str] = None,
                 id: Optional[str] = None, 
                 source: ObjectSource = ObjectSource.LOCAL):
        """
            初始化JoinTable对象。
        
        Args:
            name (str): 表名，不能为空。
            join_keys (List[str]): 用于连接的列名，不能为空。
            owner (str, optional): 所有者，默认为""。
            workspace (str, optional): 工作空间，默认为"default"。
            description (Optional[str], optional): 描述，默认为None。
            id (Optional[str], optional): ID，默认为None。
            source (ObjectSource, optional): 来源，默认为ObjectSource.LOCAL。
        
        Raises:
            ValueError: 当join_keys为空时会引发此异常。
        """
        super().__init__(name, owner, workspace, description, id, source)
        self.join_keys = join_keys

    def to_proto(self) -> custom_resource_pb2.CustomResource:
        """
            将 CustomResource 对象转换为 protobuf 格式的 CustomResource 消息。
        
        Args:
            None
        
        Returns:
            custom_resource_pb2.CustomResource (protobuf): CustomResource 对象的 protobuf 格式表示。包含以下字段：
                - api_version (str, required): API 版本，默认为 festar_config['api_version']。
                - kind (str, required): CustomResource 类型，由子类实现 get_kind() 方法指定。
                - metadata (custom_resource_metadata_pb2.ObjectMeta, required): 元数据信息，由 info 属性提供。
                - spec (google.protobuf.Any, optional): 资源配置信息，由子类实现 _spec_to_proto() 方法生成。
        
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
    def from_proto(cls, proto: custom_resource_pb2.CustomResource, source: ObjectSource) -> 'Entity':
        """
            从 CustomResource protobuf 对象中创建 Entity 实例。
        
        Args:
            proto (custom_resource_pb2.CustomResource): CustomResource protobuf 对象，包含了资源的信息。
            source (ObjectSource): 表示资源来自何处的 ObjectSource 枚举值，可选值为：LOCAL、REMOTE、UNKNOWN。
        
        Returns:
            Entity (str): Entity 类的实例，包含了资源的名称、关联键、命名空间、所有者、工作区、描述、ID 和来源等信息。
        
        Raises:
            无。
        """
        spec_dict = cls._spec_from_proto(proto.spec)
        metadata = proto.metadata
        return cls(
            name=metadata.name,
            join_keys=spec_dict['join_keys'],
            owner=metadata.labels.owner,
            workspace=metadata.labels.workspace,
            description=metadata.labels.description,
            id=metadata.labels.id,
            source=source
        )

    def get_kind(self) -> str:
        """
            获取实体类型，返回值为字符串类型，固定为"Entity"。
        
        Args:
            None
        
        Returns:
            str (str): 返回一个字符串类型的实体类型，固定为"Entity"。
        """
        return "Entity"

    def _spec_to_proto(self) -> Struct:
        """
            将实体的规格转换为 Protobuf 结构体。
        
        Args:
            self (Entity): Entity 对象本身。
        
        Returns:
            Struct (google.protobuf.struct_pb2.Struct): Protobuf 结构体，包含实体的 join_keys。
        """
        entity_spec = entity_pb2.EntitySpec(
            join_keys=self.join_keys
        )
        spec_dict = MessageToDict(entity_spec, preserving_proto_field_name=True)
        result = Struct()
        result.update(spec_dict)
        return result

    @classmethod
    def _spec_from_proto(cls, spec: Struct) -> Dict[str, Any]:
        """
            将 protobuf 格式的 EntitySpec 转换为字典形式。
        返回值是一个包含以下键值对的字典：
            - "join_keys" (List[str])：实体的 join key 列表。
        
        Args:
            spec (Struct): protobuf 格式的 EntitySpec，其中包含了实体的 join keys。
        
        Returns:
            Dict[str, Any]: 包含以下键值对的字典：
                - "join_keys" (List[str])：实体的 join key 列表。
        
        Raises:
            无。
        """
        entity_spec = ParseDict(spec, entity_pb2.EntitySpec())
        return {
            'join_keys': list(entity_spec.join_keys)
        }