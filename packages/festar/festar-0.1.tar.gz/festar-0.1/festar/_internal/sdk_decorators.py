#!/usr/bin/env python
# coding=utf-8
########################################################################
#
# Copyright (C) Baidu Ltd. All rights reserved. 
#
########################################################################

"""
Author: chenxiaoyan07@baidu.com
Date: 2024-09-02 14:34:19
LastEditTime: 2024-09-12 16:49:14
LastEditors: chenxiaoyan07@baidu.com
Description: 
FilePath: /festar-sdk/src/festar/_internal/sdk_decorators.py
"""
from functools import wraps
from typing import Callable, Any, Optional
from typing import Type, TypeVar
import logging

logger = logging.getLogger(__name__)


def sdk_public_method(
    func: Optional[Callable] = None,
    *,
    requires_validation: bool = False,
    supports_skip_validation: bool = False
):
    """
    用于标记SDK公共方法的装饰器，该方法需要进行参数验证和日志记录。
    
    Args:
        func (Optional[Callable], optional): 被装饰的函数，默认为None。 Defaults to None.
        requires_validation (bool, optional): 是否需要进行参数验证，默认为False。 Defaults to False.
        supports_skip_validation (bool, optional): 是否支持跳过参数验证，默认为False。 Defaults to False.
    
    Returns:
        Union[Callable, Callable[[Callable], Callable]]: 如果传入了func，则返回修改后的func；否则返回一个修改后的decorator函数。
        
        1. 如果传入了func，则直接返回修改后的func，即在func上添加了前后处理和错误处理功能。
        2. 如果未传入func，则返回一个修改后的decorator函数，可以使用@sdk_public_method来对函数进行装饰。
    
    Raises:
        None
    """
    def decorator(f: Callable):
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # 前置处理
            if requires_validation:
                # 这里可以添加验证逻辑
                pass
            
            # 日志记录
            logger.debug(f"Calling {f.__name__} with args: {args}, kwargs: {kwargs}")
            
            try:
                result = f(*args, **kwargs)
                
                # 后置处理
                logger.debug(f"{f.__name__} returned: {result}")
                
                return result
            except Exception as e:
                # 错误处理
                logger.error(f"Error in {f.__name__}: {str(e)}")
                raise
        
        return wrapper
    
    if func is None:
        return decorator
    else:
        return decorator(func)


def sdk_object(cls):
    """
    包装一个类，并在其中添加一些通用的功能。
     包括：
      1. 注册对象到全局注册表；
      2. 添加通用的验证逻辑；
      3. 从字典创建对象的通用方法；
      4. 将对象转换为字典的通用方法。
    
    返回值是一个新的包装类，该类继承自原始类，并添加了上述所有功能。
    
    Args:
        cls (type): 需要被包装的类。
    
    Returns:
        type: 包装后的类，继承自原始类，并添加了上述所有功能。
    """
    class Wrapper(cls):
        """类的装饰器
        """
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._register_object()

        def _register_object(self):
            # 这里可以添加将对象注册到某个全局注册表的逻辑
            # 例如：global_registry.register(self)
            pass

        def validate(self):
            """添加通用的验证逻辑"""
            print(f"Validating {self.__class__.__name__}: {self.name}")
            # 这里可以添加更多的验证逻辑

        @classmethod
        def from_dict(cls, data: dict):
            """从字典创建对象的通用方法"""
            return cls(**data)

        def to_dict(self):
            """将对象转换为字典的通用方法"""
            return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}

    # 复制原始类的属性
    for attr in ['__module__', '__name__', '__qualname__', '__doc__']:
        setattr(Wrapper, attr, getattr(cls, attr, None))

    # 复制原始类的类方法和静态方法
    for attr, value in cls.__dict__.items():
        if isinstance(value, (classmethod, staticmethod)):
            setattr(Wrapper, attr, value)

    return Wrapper