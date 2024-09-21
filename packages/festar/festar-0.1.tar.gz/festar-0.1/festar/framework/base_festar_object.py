#!/usr/bin/env python
# coding=utf-8
########################################################################
#
# Copyright (C) Baidu Ltd. All rights reserved. 
#
########################################################################

"""
Author: chenxiaoyan07@baidu.com
Date: 2024-09-09 23:30:12
LastEditTime: 2024-09-12 17:10:44
LastEditors: chenxiaoyan07@baidu.com
Description: 
FilePath: /festar-sdk/src/festar/framework/base_festar_object.py
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from typing import TypeVar, Type, Set
from enum import Enum
from google.protobuf.struct_pb2 import Struct
from festar.proto.resource import custom_resource_pb2
from festar.core.conf import festar_config


T = TypeVar('T', bound='BaseFestarObject')

_LOCAL_FESTAR_OBJECTS: Set["BaseFestarObject"] = set()

class ObjectSource(Enum):
    """
    An enumeration that represents the source of an object in FESTAR."""
    LOCAL = 1
    REMOTE = 2

class FestarObjectInfo:
    """
    A class representing metadata about an object in FESTAR."""
    def __init__(
        self, 
        name: str, 
        id: str, 
        owner: str, 
        workspace: str, 
        description: Optional[str] = None
    ):
        """
            Initializes a Workspace object with the given parameters.
        
        Args:
            name (str): The name of the workspace.
            id (str): The unique identifier for the workspace.
            owner (str): The owner of the workspace.
            workspace (str): The workspace to which this object belongs.
            description (Optional[str], optional): A brief description of the workspace. Defaults to None.
        """
        self.name = name
        self.id = id
        self.owner = owner
        self.workspace = workspace
        self.description = description

    def to_proto(self) -> custom_resource_pb2.ObjectMetadata:
        """
            将当前对象转换为 protobuf 格式的 ObjectMetadata，用于在 Kubernetes CustomResourceDefinition 中使用。
        返回值类型为 custom_resource_pb2.ObjectMetadata。
        
        Args:
            无参数函数，不需要传入任何参数。
        
        Returns:
            custom_resource_pb2.ObjectMetadata (protobuf): 包含当前对象的名称、命名空间和标签信息的 protobuf 对象。
        """
        labels = custom_resource_pb2.Labels(
            id=self.id,
            name=self.name,
            owner=self.owner,
            workspace=self.workspace,
            description=self.description or ""
        )
        return custom_resource_pb2.ObjectMetadata(
            name=self.name,
            namespace=self.workspace,
            labels=labels
        )

    @classmethod
    def from_proto(cls, proto: custom_resource_pb2.ObjectMetadata) -> 'FestarObjectInfo':
        """
            从 protobuf 对象中创建 FestarObjectInfo 实例。
        
        Args:
            proto (custom_resource_pb2.ObjectMetadata): protobuf 对象，包含对象的元数据信息。
                name (str, optional): 对象名称，默认为 None。
                id (str, optional): 对象 ID，默认为 None。
                owner (str, optional): 所有者，默认为 None。
                workspace (str, optional): 工作区，默认为 None。
                description (str, optional): 描述，默认为 None。
        
        Returns:
            FestarObjectInfo (FestarObjectInfo): FestarObjectInfo 实例，包含从 protobuf 对象中提取出来的元数据信息。
        """
        return cls(
            name=proto.name,
            id=proto.labels.id,
            owner=proto.labels.owner,
            workspace=proto.labels.workspace,
            description=proto.labels.description
        )
        
        
class BaseFestarObject:
    """
    A base class that represents a generic FESTAR object."""
    def __init__(
        self, 
        name: str, 
        owner: str,
        workspace: str,
        description: Optional[str] = None,
        id: Optional[str] = None,
        source: ObjectSource = ObjectSource.LOCAL
    ):
        """
            初始化FestarObject对象，用于封装Festar对象的基本信息和操作。
        
        Args:
            name (str): 对象名称，不能为空。
            owner (str): 所有者，不能为空。
            workspace (str, optional): 工作区，默认使用配置文件中的默认工作区，可选参数。
            description (Optional[str], optional): 描述，默认为None，可选参数。
            id (Optional[str], optional): ID，默认根据其他参数自动生成，可选参数。
            source (ObjectSource, optional): 来源，默认为ObjectSource.LOCAL，可选参数。
        
        Raises:
            ValueError: 如果name、owner、workspace或id为空，则会引发ValueError异常。
            TypeError: 如果source不是ObjectSource类型，则会引发TypeError异常。
        """
        self.info = FestarObjectInfo(
            name=name,
            id=id or f"{self.get_kind().lower()}-{name}",  # 生成一个默认ID
            owner=owner,
            workspace=workspace or festar_config.get('default_workspace'),
            description=description
        )
        self.source = source
        if source == ObjectSource.LOCAL:
            self._register_local_object()

    def _register_local_object(self) -> None:
        """
            注册当前对象到全局的 FESTAR 对象集合中，用于统一管理和清理所有 FESTAR 对象。
        该函数只会在第一次使用对象时被调用，并且只会被调用一次。
        
        Args:
            None
        
        Returns:
            None: 无返回值，直接修改全局变量 _LOCAL_FESTAR_OBJECTS。
        """
        global _LOCAL_FESTAR_OBJECTS
        _LOCAL_FESTAR_OBJECTS.add(self)

    @staticmethod
    def get_local_objects() -> Set['BaseFestarObject']:
        """
            获取当前进程中的所有本地 Festar 对象。
        如果没有初始化，则返回一个空集合。
        
        Args:
            None
        
        Returns:
            Set(BaseFestarObject): 包含所有本地 Festar 对象的集合，元素类型为 BaseFestarObject。
        """
        global _LOCAL_FESTAR_OBJECTS
        return _LOCAL_FESTAR_OBJECTS

    @classmethod
    def get_object(cls: Type[T], name: str) -> Optional[T]:
        """
            获取指定名称的对象实例，如果不存在则返回None。
        该方法会遍历当前进程中所有已注册的Festar对象，并且只会返回与给定名称相同的第一个对象。
        
        Args:
            name (str): 需要查找的对象名称。
        
        Returns:
            Optional[T]: 返回一个类型为T的对象实例，如果不存在则返回None。
        """
        for obj in _LOCAL_FESTAR_OBJECTS:
            if isinstance(obj, cls) and obj.info.name == name:
                return obj
        return None

    @abstractmethod
    def to_proto(self) -> custom_resource_pb2.CustomResource:
        """
            将当前资源转换为 protobuf 格式的 CustomResource 对象。
        该方法必须被重写，返回一个包含自定义资源信息的 CustomResource 对象。
        
        Returns:
            custom_resource_pb2.CustomResource (protobuf): 包含自定义资源信息的 CustomResource 对象。
        
        Raises:
            NotImplementedError: 如果该方法没有被正确重写，则会引发 NotImplementedError 异常。
        """
        pass

    @classmethod
    @abstractmethod
    def from_proto(cls: Type[T], proto: custom_resource_pb2.CustomResource, source: ObjectSource) -> T:
        """
            从 CustomResource 对象中创建当前类的实例。
        该方法应该被子类重写，并返回一个当前类的实例。
        
        Args:
            cls (Type[T]): 当前类的类型。
            proto (custom_resource_pb2.CustomResource): CustomResource 对象。
            source (ObjectSource): 来源，包括 API 和 Kubernetes CRD。
        
        Returns:
            T: 当前类的实例。
        
        Raises:
            NotImplementedError: 如果没有重写该方法。
        """
        pass

    @abstractmethod
    def get_kind(self) -> str:
        """
            获取对象的类型，返回一个字符串。
        子类需要实现此方法。
        
        Args:
            None.
        
        Returns:
            str (str): 对象的类型，例如 "function"、"class" 等。
        
        Raises:
            None.
        """
        pass

    @abstractmethod
    def _spec_to_proto(self) -> Struct:
        """
            将当前规格转换为Protobuf的Struct对象，该方法需要被子类实现。
        返回值：Struct，一个包含当前规格信息的Protobuf结构体。
        
        Args:
            无参数，不需要传入任何参数。
        
        Returns:
            Struct (google.protobuf.struct_pb2.Struct): Protobuf的Struct对象，包含当前规格信息。
        
        Raises:
            无异常抛出。
        """
        pass

    @classmethod
    @abstractmethod
    def _spec_from_proto(cls, spec: Struct) -> Dict[str, Any]:
        """
            从 protobuf 结构体中解析出规格字典。该方法应由子类实现。
        子类需要提供一个能够将 protobuf 结构体转换为规格字典的实现。
        
        Args:
            spec (Struct): protobuf 结构体，包含了规格信息。
        
        Returns:
            Dict[str, Any]: 包含了规格信息的字典，键值对如下：
                - "name" (str): 规格名称。
                - "description" (Optional[str]): 规格描述，可选。
                - "fields" (List[Dict[str, Any]]): 规格字段列表，每个字段是一个包含以下键值对的字典：
                    - "name" (str): 字段名称。
                    - "type" (Union[Type, str]): 字段类型，可以是 Python 原生类型或者字符串类型。
                    - "description" (Optional[str]): 字段描述，可选。
                    - "optional" (bool): 是否是可选字段，默认为 False。
                    - "default" (Any): 默认值，可选。
        
        Raises:
            NotImplementedError: 当该方法未被子类实现时引发。
        """
        pass
